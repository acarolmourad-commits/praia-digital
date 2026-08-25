from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from academy.core.database import get_db
from academy.core.security import get_current_user, admin_required
from academy.financeiro.models import RegistroFinanceiro, StatusPagamento, StatusEntrega
from academy.financeiro.schemas import RegistroFinanceiroIn, RegistroFinanceiroUpdate, RegistroFinanceiroOut
from datetime import datetime

router = APIRouter(prefix="/financeiro", tags=["financeiro"])

@router.post("/registros", response_model=RegistroFinanceiroOut)
def criar_registro_financeiro(payload: RegistroFinanceiroIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reg = RegistroFinanceiro(
        customer_name=payload.customer_name,
        customer_email=payload.customer_email,
        product_name=payload.product_name,
        order_id=payload.order_id,
        amount_expected=payload.amount_expected,
        payment_status=StatusPagamento.PAGAMENTO_PENDENTE,
        delivery_status=StatusEntrega.BLOQUEADA,
        revenue_confirmed=0,
    )
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg

@router.get("/registros", response_model=List[RegistroFinanceiroOut])
def listar_registros_financeiros(status: Optional[str] = None, db: Session = Depends(get_db), admin=Depends(admin_required)):
    q = db.query(RegistroFinanceiro)
    if status:
        q = q.filter(RegistroFinanceiro.payment_status == status)
    return q.order_by(RegistroFinanceiro.created_at.desc()).all()

@router.get("/registros/{registro_id}", response_model=RegistroFinanceiroOut)
def obter_registro_financeiro(registro_id: int, db: Session = Depends(get_db), admin=Depends(admin_required)):
    reg = db.query(RegistroFinanceiro).filter(RegistroFinanceiro.id == registro_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    return reg

@router.patch("/registros/{registro_id}", response_model=RegistroFinanceiroOut)
def atualizar_registro_financeiro(registro_id: int, payload: RegistroFinanceiroUpdate, db: Session = Depends(get_db), admin=Depends(admin_required)):
    reg = db.query(RegistroFinanceiro).filter(RegistroFinanceiro.id == registro_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(reg, field, value)

    if payload.payment_status == StatusPagamento.PAGAMENTO_CONFIRMADO:
        if payload.amount_paid is not None:
            reg.amount_paid = payload.amount_paid
        reg.revenue_confirmed = reg.amount_paid if reg.amount_paid is not None else reg.amount_expected
        reg.payment_verified_at = datetime.utcnow()
        reg.delivery_status = StatusEntrega.ENTREGUE
        reg.delivery_released_at = datetime.utcnow()
    elif payload.payment_status in {
        StatusPagamento.PAGAMENTO_REJEITADO,
        StatusPagamento.PAGAMENTO_NAO_ENCONTRADO,
        StatusPagamento.PAGAMENTO_ESTORNADO,
    }:
        reg.revenue_confirmed = 0
        reg.delivery_status = StatusEntrega.BLOQUEADA
        reg.amount_paid = None
        reg.delivery_released_at = None
        reg.delivery_released_by = None

    db.commit()
    db.refresh(reg)
    return reg

@router.post("/registros/{registro_id}/comprovante", response_model=RegistroFinanceiroOut)
def anexar_comprovante(registro_id: int, payload: RegistroFinanceiroUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reg = db.query(RegistroFinanceiro).filter(RegistroFinanceiro.id == registro_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    if not payload.payment_proof:
        raise HTTPException(status_code=400, detail="Comprovante não informado")
    reg.payment_proof = payload.payment_proof
    reg.payment_proof_source = payload.payment_proof_source or "upload"
    reg.payment_proof_received_at = datetime.utcnow()
    reg.payment_status = StatusPagamento.COMPROVANTE_RECEBIDO
    db.commit()
    db.refresh(reg)
    return reg

@router.post("/registros/{registro_id}/validar", response_model=RegistroFinanceiroOut)
def validar_pagamento(registro_id: int, payload: RegistroFinanceiroUpdate, db: Session = Depends(get_db), admin=Depends(admin_required)):
    reg = db.query(RegistroFinanceiro).filter(RegistroFinanceiro.id == registro_id).first()
    if not reg:
        raise HTTPException(status_code=404, detail="Registro financeiro não encontrado")
    if reg.payment_status not in {StatusPagamento.COMPROVANTE_RECEBIDO, StatusPagamento.PAGAMENTO_EM_VALIDACAO, StatusPagamento.PAGAMENTO_PENDENTE}:
        raise HTTPException(status_code=400, detail=f"Status atual não permite validação: {reg.payment_status}")
    if not payload.payment_verified_by:
        raise HTTPException(status_code=400, detail="Informe o responsável pela validação")
    reg.payment_status = StatusPagamento.PAGAMENTO_CONFIRMADO
    reg.payment_verified_at = datetime.utcnow()
    reg.payment_verified_by = payload.payment_verified_by
    if payload.amount_paid is not None:
        reg.amount_paid = payload.amount_paid
    reg.revenue_confirmed = reg.amount_paid if reg.amount_paid is not None else reg.amount_expected
    reg.delivery_status = StatusEntrega.ENTREGUE
    reg.delivery_released_at = datetime.utcnow()
    if payload.delivery_released_by:
        reg.delivery_released_by = payload.delivery_released_by
    db.commit()
    db.refresh(reg)
    return reg
