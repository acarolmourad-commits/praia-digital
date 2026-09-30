"""
Router administrativo — Praia Digital

Endpoints para CRUD completo de:
  Clientes, Produtos, Fornecedores, Usuários, Centros de Custo
  Solicitações → Cotações → Aprovações → Ordens → Recebimentos → Financeiro

Todas as operações são auditáveis. Conflitos de dados são prevenidos
com UniqueConstraints no nível da base.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date
from academy.core.database import get_db
from academy.core.security import get_current_user, hash_password, verify_password
from academy.core.auth import create_access_token


router = APIRouter(prefix="/admin", tags=["admin"])


def admin_required(user=Depends(get_current_user)):
    """Requer role admin ou ADMINISTRADOR."""
    role = user.get("role", "").upper()
    if role not in ("ADMIN", "ADMINISTRADOR"):
        raise HTTPException(status_code=403, detail="Admin access required.")
    return user
from academy.admin.models import (
    Usuario, Cliente, Produto, Fornecedor, CentroCusto,
    SolicitacaoCompra, Cotacao, Aprovacao, OrdemCompra,
    Recebimento, LancamentoFinanceiro, AuditoriaLog,
    StatusSolicitacao, StatusLancamento, TipoLancamento,
    TipoCliente, TipoProduto, StatusRecebimento,
)
from academy.admin.schemas import (
    ClienteCreate, ClienteOut,
    ProdutoCreate, ProdutoOut,
    FornecedorCreate, FornecedorOut,
    UsuarioCreate, UsuarioOut,
    SolicitacaoCreate, SolicitacaoOut,
    CotacaoCreate, CotacaoOut,
    AprovacaoCreate, AprovacaoOut,
    OrdemCreate, OrdemOut,
    RecebimentoCreate, RecebimentoOut,
    LancamentoCreate, LancamentoOut, LancamentoPatch,
    AuditoriaOut,
    SolicitacaoFilter, LancamentoFilter,
)
import json as json_lib


# Login simples para o painel admin (bypass de email-based auth)
@router.post("/login")
def admin_login(payload: dict, db: Session = Depends(get_db)):
    """
    Login via password. Cria um usuário admin padrão se não existir
    (para o primeiro uso). O token JWT é retornado para uso no frontend.
    """
    password = payload.get("password", "")
    if not password:
        raise HTTPException(400, "Password required")

    from academy.core.auth import create_access_token

    admin_user = db.query(Usuario).filter(Usuario.username == "admin").first()
    if not admin_user:
        admin_user = Usuario(
            username="admin",
            nome="Administrador Praia Digital",
            email="admin@praia.digital",
            senha_hash=hash_password(password),
            perfil="ADMINISTRADOR",
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
    else:
        if not verify_password(password, admin_user.senha_hash):
            raise HTTPException(401, "Senha inválida")

    token = create_access_token({"sub": str(admin_user.id), "role": admin_user.perfil.value})
    return {"token": token, "role": admin_user.perfil.value}


def log_audit(db: Session, user_id: Optional[int], acao: str,
              entidade: str, registro_id: Optional[int],
              valor_anterior: dict = None, valor_novo: dict = None):
    """Grava entrada de auditoria (preservando histórico)."""
    db.add(AuditoriaLog(
        usuario_id=user_id,
        acao=acao,
        entidade=entidade,
        registro_id=registro_id,
        valor_anterior=json_lib.dumps(valor_anterior, default=str),
        valor_novo=json_lib.dumps(valor_novo, default=str),
    ))


# ──────────────────────────────────────────────
# CLIENTES
# ──────────────────────────────────────────────

@router.get("/clientes", response_model=List[ClienteOut])
def list_clientes(skip: int = 0, limit: int = 100,
                  search: Optional[str] = None,
                  db: Session = Depends(get_db),
                  admin=Depends(admin_required)):
    q = db.query(Cliente)
    if search:
        q = q.filter(Cliente.nome.ilike(f"%{search}%"))
    return q.offset(skip).limit(limit).all()


@router.post("/clientes", response_model=ClienteOut)
def create_cliente(payload: ClienteCreate,
                    db: Session = Depends(get_db),
                    admin=Depends(admin_required)):
    # previne duplicidade por CPF/CNPJ + tipo
    existing = db.query(Cliente).filter(
        Cliente.tipo == payload.tipo,
        Cliente.cpf_cnpj == payload.cpf_cnpj
    ).first()
    if existing:
        raise HTTPException(409, f"Já existe cliente com CPF/CNPJ {payload.cpf_cnpj}")
    c = Cliente(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    log_audit(db, admin.get("id"), "create", "Cliente", c.id)
    db.commit()
    return c


@router.get("/clientes/{cliente_id}", response_model=ClienteOut)
def get_cliente(cliente_id: int, db: Session = Depends(get_db),
                admin=Depends(admin_required)):
    c = db.get(Cliente, cliente_id)
    if not c:
        raise HTTPException(404, "Cliente não encontrado")
    return c


@router.patch("/clientes/{cliente_id}", response_model=ClienteOut)
def update_cliente(cliente_id: int, payload: ClienteCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(admin_required)):
    c = db.get(Cliente, cliente_id)
    if not c:
        raise HTTPException(404, "Cliente não encontrado")
    old_data = {k: getattr(c, k) for k in Cliente.__table__.columns.keys()}
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit()
    new_data = {k: getattr(c, k) for k in Cliente.__table__.columns.keys()}
    log_audit(db, admin.get("id"), "update", "Cliente", c.id, old_data, new_data)
    db.refresh(c)
    return c


# ──────────────────────────────────────────────
# PRODUTOS
# ──────────────────────────────────────────────

@router.get("/produtos", response_model=List[ProdutoOut])
def list_produtos(skip: int = 0, limit: int = 200,
                  search: Optional[str] = None,
                  categoria: Optional[str] = None,
                  db: Session = Depends(get_db),
                  admin=Depends(admin_required)):
    q = db.query(Produto)
    if search:
        q = q.filter(Produto.nome.ilike(f"%{search}%"))
    if categoria:
        q = q.filter(Produto.categoria == categoria)
    return q.offset(skip).limit(limit).all()


@router.post("/produtos", response_model=ProdutoOut)
def create_produto(payload: ProdutoCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(admin_required)):
    if payload.sku:
        existing = db.query(Produto).filter(Produto.sku == payload.sku).first()
        if existing:
            raise HTTPException(409, f"Já existe produto com SKU {payload.sku}")
    p = Produto(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    log_audit(db, admin.get("id"), "create", "Produto", p.id)
    db.commit()
    return p


# ──────────────────────────────────────────────
# FORNECEDORES
# ──────────────────────────────────────────────

@router.get("/fornecedores", response_model=List[FornecedorOut])
def list_fornecedores(skip: int = 0, limit: int = 100,
                      search: Optional[str] = None,
                      db: Session = Depends(get_db),
                      admin=Depends(admin_required)):
    q = db.query(Fornecedor)
    if search:
        q = q.filter(Fornecedor.razao_social.ilike(f"%{search}%"))
    return q.offset(skip).limit(limit).all()


@router.post("/fornecedores", response_model=FornecedorOut)
def create_fornecedor(payload: FornecedorCreate,
                      db: Session = Depends(get_db),
                      admin=Depends(admin_required)):
    if payload.cnpj:
        existing = db.query(Fornecedor).filter(Fornecedor.cnpj == payload.cnpj).first()
        if existing:
            raise HTTPException(409, f"Já existe fornecedor com CNPJ {payload.cnpj}")
    f = Fornecedor(**payload.model_dump())
    db.add(f)
    db.commit()
    db.refresh(f)
    log_audit(db, admin.get("id"), "create", "Fornecedor", f.id)
    db.commit()
    return f


# ──────────────────────────────────────────────
# USUÁRIOS
# ──────────────────────────────────────────────

@router.get("/usuarios", response_model=List[UsuarioOut])
def list_usuarios(db: Session = Depends(get_db),
                  admin=Depends(admin_required)):
    return db.query(Usuario).all()


@router.post("/usuarios", response_model=UsuarioOut)
def create_usuario(payload: UsuarioCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(admin_required)):
    if db.query(Usuario).filter(Usuario.username == payload.username).first():
        raise HTTPException(409, "Username já existe")
    from academy.core.security import hash_password as get_password_hash
    u = Usuario(
        username=payload.username,
        nome=payload.nome,
        email=payload.email,
        cpf=payload.cpf,
        senha_hash=get_password_hash(payload.senha),
        perfil=payload.perfil,
        ativo=payload.ativo,
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    log_audit(db, admin.get("id"), "create", "Usuario", u.id)
    db.commit()
    return u


# ──────────────────────────────────────────────
# SOLICITAÇÕES DE COMPRA
# ──────────────────────────────────────────────

@router.get("/solicitacoes", response_model=List[SolicitacaoOut])
def list_solicitacoes(
    skip: int = 0, limit: int = 100,
    status: Optional[StatusSolicitacao] = None,
    cliente_id: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    q = db.query(SolicitacaoCompra)
    if status:
        q = q.filter(SolicitacaoCompra.status == status)
    if cliente_id:
        q = q.filter(SolicitacaoCompra.cliente_id == cliente_id)
    if data_inicio:
        q = q.filter(SolicitacaoCompra.criado_em >= data_inicio)
    if data_fim:
        q = q.filter(SolicitacaoCompra.criado_em <= data_fim)
    return q.order_by(SolicitacaoCompra.criado_em.desc()).offset(skip).limit(limit).all()


@router.post("/solicitacoes", response_model=SolicitacaoOut)
def create_solicitacao(payload: SolicitacaoCreate,
                       db: Session = Depends(get_db),
                       admin=Depends(admin_required)):
    # Valida integridade referencial
    if not db.get(Usuario, payload.solicitante_id):
        raise HTTPException(400, "Solicitante (usuário) inválido")
    if not db.get(Produto, payload.produto_id):
        raise HTTPException(400, "Produto inválido")
    if payload.cliente_id and not db.get(Cliente, payload.cliente_id):
        raise HTTPException(400, "Cliente inválido")
    if payload.centro_custo_id and not db.get(CentroCusto, payload.centro_custo_id):
        raise HTTPException(400, "Centro de custo inválido")

    # Gera número único
    today = datetime.utcnow().strftime("%Y%m%d")
    count = db.query(SolicitacaoCompra).filter(
        SolicitacaoCompra.criado_em >= datetime.utcnow().replace(hour=0, minute=0, second=0)
    ).count() + 1
    numero = f"SC-{today}-{count:04d}"

    s = SolicitacaoCompra(
        numero=numero,
        status=StatusSolicitacao.SOLICITADA,
        **payload.model_dump(),
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    log_audit(db, admin.get("id"), "create", "SolicitacaoCompra", s.id,
              valor_novo={"numero": numero, **payload.model_dump()})
    db.commit()
    return s


@router.get("/solicitacoes/{solicitacao_id}", response_model=SolicitacaoOut)
def get_solicitacao(solicitacao_id: int, db: Session = Depends(get_db),
                    admin=Depends(admin_required)):
    s = db.get(SolicitacaoCompra, solicitacao_id)
    if not s:
        raise HTTPException(404, "Solicitação não encontrada")
    return s


@router.post("/solicitacoes/{solicitacao_id}/status")
def update_solicitacao_status(solicitacao_id: int,
                              status: StatusSolicitacao,
                              db: Session = Depends(get_db),
                              admin=Depends(admin_required)):
    s = db.get(SolicitacaoCompra, solicitacao_id)
    if not s:
        raise HTTPException(404, "Solicitação não encontrada")
    old_status = s.status.value
    s.status = status
    s.atualizado_em = datetime.utcnow()
    db.commit()
    log_audit(db, admin.get("id"), "update_status", "SolicitacaoCompra", s.id,
              {"status": old_status}, {"status": status.value})
    db.commit()
    return {"status": "ok", "novo_status": status.value}


# ──────────────────────────────────────────────
# COTAÇÕES
# ──────────────────────────────────────────────

@router.get("/solicitacoes/{solicitacao_id}/cotacoes", response_model=List[CotacaoOut])
def list_cotacoes(solicitacao_id: int, db: Session = Depends(get_db),
                  admin=Depends(admin_required)):
    if not db.get(SolicitacaoCompra, solicitacao_id):
        raise HTTPException(404, "Solicitação não encontrada")
    return db.query(Cotacao).filter(Cotacao.solicitacao_id == solicitacao_id).all()


@router.post("/cotacoes", response_model=CotacaoOut)
def create_cotacao(payload: CotacaoCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(admin_required)):
    if not db.get(SolicitacaoCompra, payload.solicitacao_id):
        raise HTTPException(400, "Solicitação inválida")
    if not db.get(Fornecedor, payload.fornecedor_id):
        raise HTTPException(400, "Fornecedor inválido")
    # Valida valor_total
    if payload.valor_total <= 0:
        raise HTTPException(400, "Valor total deve ser maior que zero")
    c = Cotacao(**payload.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    log_audit(db, admin.get("id"), "create", "Cotacao", c.id)
    db.commit()
    # Atualiza status da solicitação para COTACAO
    s = db.get(SolicitacaoCompra, payload.solicitacao_id)
    if s and s.status == StatusSolicitacao.SOLICITADA:
        s.status = StatusSolicitacao.COTACAO
        db.commit()
    return c


# ──────────────────────────────────────────────
# APROVAÇÕES
# ──────────────────────────────────────────────

@router.post("/aprovacoes", response_model=AprovacaoOut)
def create_aprovacao(payload: AprovacaoCreate,
                     db: Session = Depends(get_db),
                     admin=Depends(admin_required)):
    # Valida aprovador tem permissão
    approver = db.get(Usuario, payload.aprovador_id)
    if not approver:
        raise HTTPException(400, "Aprovador inválido")
    s = db.get(SolicitacaoCompra, payload.solicitacao_id)
    if not s:
        raise HTTPException(404, "Solicitação não encontrada")
    a = Aprovacao(**payload.model_dump())
    db.add(a)
    s.status = StatusSolicitacao.APROVADA
    s.atualizado_em = datetime.utcnow()
    db.commit()
    db.refresh(a)
    log_audit(db, admin.get("id"), "approve", "SolicitacaoCompra", s.id,
              {"status": "COTACAO"}, {"status": "APROVADA", "aprovacao_id": a.id})
    db.commit()
    return a


# ──────────────────────────────────────────────
# ORDENS DE COMPRA
# ──────────────────────────────────────────────

@router.get("/ordens", response_model=List[OrdemOut])
def list_ordens(db: Session = Depends(get_db),
                admin=Depends(admin_required)):
    return db.query(OrdemCompra).order_by(OrdemCompra.criado_em.desc()).all()


@router.post("/ordens", response_model=OrdemOut)
def create_ordem(payload: OrdemCreate,
                 db: Session = Depends(get_db),
                 admin=Depends(admin_required)):
    # Valida
    if db.query(OrdemCompra).filter(OrdemCompra.numero == payload.numero).first():
        raise HTTPException(409, f"Já existe ordem com número {payload.numero}")
    if not db.get(SolicitacaoCompra, payload.solicitacao_id):
        raise HTTPException(400, "Solicitação inválida")
    o = OrdemCompra(**payload.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    log_audit(db, admin.get("id"), "create", "OrdemCompra", o.id)
    db.commit()
    return o


# ──────────────────────────────────────────────
# RECEBMENTO
# ──────────────────────────────────────────────

@router.post("/recebimentos", response_model=RecebimentoOut)
def create_recebimento(payload: RecebimentoCreate,
                       db: Session = Depends(get_db),
                       admin=Depends(admin_required)):
    if not db.get(OrdemCompra, payload.ordem_id):
        raise HTTPException(400, "Ordem inválida")
    r = Recebimento(**payload.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    log_audit(db, admin.get("id"), "create", "Recebimento", r.id)
    db.commit()
    return r


# ──────────────────────────────────────────────
# FINANCEIRO
# ──────────────────────────────────────────────

@router.get("/financeiro/lancamentos", response_model=List[LancamentoOut])
def list_lancamentos(
    skip: int = 0, limit: int = 200,
    tipo: Optional[TipoLancamento] = None,
    status: Optional[StatusLancamento] = None,
    categoria: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    cliente_id: Optional[int] = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    q = db.query(LancamentoFinanceiro)
    if tipo:
        q = q.filter(LancamentoFinanceiro.tipo == tipo)
    if status:
        q = q.filter(LancamentoFinanceiro.status == status)
    if categoria:
        q = q.filter(LancamentoFinanceiro.categoria == categoria)
    if data_inicio:
        q = q.filter(LancamentoFinanceiro.data_prevista >= data_inicio)
    if data_fim:
        q = q.filter(LancamentoFinanceiro.data_prevista <= data_fim)
    if cliente_id:
        q = q.filter(LancamentoFinanceiro.cliente_id == cliente_id)
    return q.order_by(LancamentoFinanceiro.data_prevista.desc()).offset(skip).limit(limit).all()


@router.post("/financeiro/lancamentos", response_model=LancamentoOut)
def create_lancamento(payload: LancamentoCreate,
                      db: Session = Depends(get_db),
                      admin=Depends(admin_required)):
    # PREVISTO ≠ FATURADO ≠ PAGO ≠ RECEBIDO: o status controla o estágio
    l = LancamentoFinanceiro(**payload.model_dump())
    db.add(l)
    db.commit()
    db.refresh(l)
    log_audit(db, admin.get("id"), "create", "LancamentoFinanceiro", l.id)
    db.commit()
    return l


@router.patch("/financeiro/lancamentos/{lancamento_id}", response_model=LancamentoOut)
def update_lancamento(lancamento_id: int, payload: LancamentoPatch,
                      db: Session = Depends(get_db),
                      admin=Depends(admin_required)):
    """
    Atualiza um lançamento preservando histórico.
    Nunca apaga — sempre cria um novo registro de auditoria.
    """
    l = db.get(LancamentoFinanceiro, lancamento_id)
    if not l:
        raise HTTPException(404, "Lançamento não encontrado")
    old_data = {k: getattr(l, k) for k in LancamentoFinanceiro.__table__.columns.keys()}
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(l, k, v)
    db.commit()
    new_data = {k: getattr(l, k) for k in LancamentoFinanceiro.__table__.columns.keys()}
    log_audit(db, admin.get("id"), "update", "LancamentoFinanceiro", l.id, old_data, new_data)
    db.commit()
    db.refresh(l)
    return l


# ──────────────────────────────────────────────
# AUDITORIA
# ──────────────────────────────────────────────

@router.get("/auditoria", response_model=List[AuditoriaOut])
def list_auditoria(
    skip: int = 0, limit: int = 200,
    usuario_id: Optional[int] = None,
    entidade: Optional[str] = None,
    acao: Optional[str] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    q = db.query(AuditoriaLog)
    if usuario_id:
        q = q.filter(AuditoriaLog.usuario_id == usuario_id)
    if entidade:
        q = q.filter(AuditoriaLog.entidade == entidade)
    if acao:
        q = q.filter(AuditoriaLog.acao == acao)
    if data_inicio:
        q = q.filter(AuditoriaLog.timestamp >= data_inicio)
    if data_fim:
        q = q.filter(AuditoriaLog.timestamp <= data_fim)
    return q.order_by(AuditoriaLog.timestamp.desc()).offset(skip).limit(limit).all()


# ──────────────────────────────────────────────
# DASHBOARD RESUMO
# ──────────────────────────────────────────────

@router.get("/dashboard/resumo")
def get_resumo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db),
    admin=Depends(admin_required),
):
    """Dashboard executivo — saldo, receitas, despesas, DRE, alertas."""
    from sqlalchemy import func as sql_func, case as sqlalchemy_case
    from decimal import Decimal

    base = db.query(LancamentoFinanceiro)
    if data_inicio:
        base = base.filter(LancamentoFinanceiro.data_prevista >= data_inicio)
    if data_fim:
        base = base.filter(LancamentoFinanceiro.data_prevista <= data_fim)

    saldo_previsto = base.with_entities(
        sql_func.sum(
            sqlalchemy_case(
                (LancamentoFinanceiro.tipo == TipoLancamento.RECEITA,
                 LancamentoFinanceiro.valor_previsto),
                else_=(LancamentoFinanceiro.valor_previsto * -1)
            )
        )
    ).scalar() or Decimal("0")

    saldo_pago = base.with_entities(
        sql_func.sum(
            sqlalchemy_case(
                (LancamentoFinanceiro.tipo == TipoLancamento.RECEITA,
                 LancamentoFinanceiro.valor_pago),
                else_=(LancamentoFinanceiro.valor_pago * -1)
            )
        )
    ).scalar() or Decimal("0")

    receitas_previstas = base.filter(
        LancamentoFinanceiro.tipo == TipoLancamento.RECEITA
    ).with_entities(sql_func.sum(LancamentoFinanceiro.valor_previsto)).scalar() or Decimal("0")

    despesas_previstas = base.filter(
        LancamentoFinanceiro.tipo == TipoLancamento.DESPESA
    ).with_entities(sql_func.sum(LancamentoFinanceiro.valor_previsto)).scalar() or Decimal("0")

    # Alertas
    alertas = []
    # Contas vencidas e não pagas
    vencidas = base.filter(
        LancamentoFinanceiro.data_vencimento < date.today(),
        LancamentoFinanceiro.status != StatusLancamento.PAGO,
        LancamentoFinanceiro.status != StatusLancamento.RECEBIDO,
    ).all()
    for v in vencidas:
        alertas.append({
            "tipo": "conta_vencida",
            "mensagem": f"{v.descricao} venceu em {v.data_vencimento}",
            "registro_id": v.id,
        })

    # Solicitações sem aprovação atrasadas (>7 dias em COTACAO)
    from sqlalchemy import and_
    old_solic = db.query(SolicitacaoCompra).filter(
        SolicitacaoCompra.status == StatusSolicitacao.COTACAO,
        SolicitacaoCompra.criado_em < datetime.utcnow().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    ).all()
    for s in old_solic:
        alertas.append({
            "tipo": "solicitacao_sem_aprovacao",
            "mensagem": f"Solicitação {s.numero} aguarda aprovação há mais de 7 dias",
            "registro_id": s.id,
        })

    return {
        "saldo_previsto": float(saldo_previsto),
        "saldo_pago": float(saldo_pago),
        "receitas_previstas": float(receitas_previstas),
        "despesas_previstas": float(despesas_previstas),
        "dre": {
            "receitas": float(receitas_previstas),
            "despesas": float(despesas_previstas),
            "lucro_operacional": float(receitas_previstas - despesas_previstas),
        },
        "alertas": alertas,
    }
