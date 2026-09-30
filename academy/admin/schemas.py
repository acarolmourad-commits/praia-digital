"""
Pydantic schemas para o módulo administrativo Praia Digital.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# ──────────────────────────────────────────────
# ENUMS (repete os do model para o schema)
# ──────────────────────────────────────────────

class TipoCliente(str, Enum):
    PF = "PF"
    PJ = "PJ"


class TipoProduto(str, Enum):
    PRODUTO = "PRODUTO"
    SERVICO = "SERVICO"


class PerfisUsuario(str, Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    FINANCEIRO    = "FINANCEIRO"
    COMPRAS       = "COMPRAS"
    COMERCIAL     = "COMERCIAL"
    OPERACIONAL   = "OPERACIONAL"
    CONSULTA      = "CONSULTA"


class StatusSolicitacao(str, Enum):
    SOLICITADA  = "SOLICITADA"
    COTACAO     = "COTACAO"
    APROVADA    = "APROVADA"
    REJEITADA   = "REJEITADA"
    COMPRA_OK   = "COMPRA_OK"
    PAGA        = "PAGA"
    RECEBIDA    = "RECEBIDA"
    FINALIZADA  = "FINALIZADA"
    CANCELADA   = "CANCELADA"


class TipoLancamento(str, Enum):
    DESPESA      = "DESPESA"
    RECEITA      = "RECEITA"
    TRANSFERENCIA = "TRANSFERENCIA"


class StatusLancamento(str, Enum):
    PREVISTO  = "PREVISTO"
    FATURADO  = "FATURADO"
    PAGO      = "PAGO"
    RECEBIDO  = "RECEBIDO"


class StatusRecebimento(str, Enum):
    RECEBIDO   = "RECEBIDO"
    PARCIAL    = "PARCIAL"
    DIVERGENTE = "DIVERGENTE"
    RECUSADO   = "RECUSADO"
    CONFERIDO  = "CONFERIDO"


# ──────────────────────────────────────────────
# USUÁRIOS
# ──────────────────────────────────────────────

class UsuarioBase(BaseModel):
    username: str
    nome: str
    email: str
    perfil: PerfisUsuario
    ativo: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str
    cpf: Optional[str] = None


class UsuarioOut(UsuarioBase):
    id: int
    cpf: Optional[str] = None
    criado_em: Optional[datetime] = None
    ultimo_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# CLIENTES
# ──────────────────────────────────────────────

class ClienteBase(BaseModel):
    tipo: TipoCliente
    nome: str
    cpf_cnpj: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    origem: Optional[str] = None
    status: str = "ativo"
    observacao: Optional[str] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteOut(ClienteBase):
    id: int
    criado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# PRODUTOS
# ──────────────────────────────────────────────

class ProdutoBase(BaseModel):
    sku: Optional[str] = None
    nome: str
    tipo: TipoProduto = TipoProduto.SERVICO
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    unidade: Optional[str] = None
    custo: Decimal = Decimal("0.00")
    preco: Decimal = Decimal("0.00")
    tem_estoque: bool = False
    estoque_atual: int = 0
    estoque_min: int = 0
    ativo: bool = True
    fornecedor_id: Optional[int] = None


class ProdutoCreate(BaseModel):
    sku: Optional[str] = None
    nome: str
    tipo: TipoProduto = TipoProduto.SERVICO
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    unidade: Optional[str] = None
    custo: Decimal = Decimal("0.00")
    preco: Decimal = Decimal("0.00")
    tem_estoque: bool = False
    estoque_atual: int = 0
    estoque_min: int = 0
    fornecedor_id: Optional[int] = None


class ProdutoOut(ProdutoBase):
    id: int
    criado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# FORNECEDORES
# ──────────────────────────────────────────────

class FornecedorBase(BaseModel):
    razao_social: str
    cnpj: Optional[str] = None
    contato_nome: Optional[str] = None
    contato_telefone: Optional[str] = None
    contato_email: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    condicoes_comerciais: Optional[str] = None
    ativo: bool = True


class FornecedorCreate(FornecedorBase):
    pass


class FornecedorOut(FornecedorBase):
    id: int
    criado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# SOLICITAÇÃO DE COMPRA
# ──────────────────────────────────────────────

class SolicitacaoCreate(BaseModel):
    solicitante_id: int
    cliente_id: Optional[int] = None
    centro_custo_id: Optional[int] = None
    produto_id: int
    quantidade: Decimal
    finalidade: Optional[str] = None
    orcamento: Optional[Decimal] = None
    observacao: Optional[str] = None


class SolicitacaoOut(BaseModel):
    id: int
    numero: str
    solicitante_id: int
    cliente_id: Optional[int]
    centro_custo_id: Optional[int]
    produto_id: int
    quantidade: Decimal
    finalidade: Optional[str]
    orcamento: Optional[Decimal]
    status: StatusSolicitacao
    observacao: Optional[str]
    criado_em: Optional[datetime]
    atualizado_em: Optional[datetime]

    # nested
    solicitante: Optional[UsuarioOut] = None
    cliente: Optional[ClienteOut] = None
    produto: Optional[ProdutoOut] = None
    cotacoes: List["CotacaoOut"] = []
    ordens: List["OrdemOut"] = []

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# COTAÇÕES
# ──────────────────────────────────────────────

class CotacaoCreate(BaseModel):
    solicitacao_id: int
    fornecedor_id: int
    preco_unitario: Decimal
    quantidade: Decimal
    frete: Decimal = Decimal("0.00")
    taxas: Decimal = Decimal("0.00")
    desconto: Decimal = Decimal("0.00")
    valor_total: Decimal
    prazo_entrega: Optional[str] = None
    condicoes: Optional[str] = None
    validade: Optional[date] = None
    observacao: Optional[str] = None
    docstring_url: Optional[str] = None


class CotacaoOut(BaseModel):
    id: int
    solicitacao_id: int
    fornecedor_id: int
    preco_unitario: Decimal
    quantidade: Decimal
    frete: Decimal
    taxas: Decimal
    desconto: Decimal
    valor_total: Decimal
    prazo_entrega: Optional[str]
    condicoes: Optional[str]
    validade: Optional[date]
    observacao: Optional[str]
    docstring_url: Optional[str]
    criado_em: Optional[datetime]

    fornecedor: Optional[FornecedorOut] = None

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# APROVAÇÃO
# ──────────────────────────────────────────────

class AprovacaoCreate(BaseModel):
    solicitacao_id: int
    aprovador_id: int
    valor_aprovado: Decimal
    justificativa: Optional[str] = None
    limite_configurado: Optional[Decimal] = None


class AprovacaoOut(BaseModel):
    id: int
    solicitacao_id: int
    aprovador_id: int
    valor_aprovado: Decimal
    data_hora: Optional[datetime]
    justificativa: Optional[str]
    limite_configurado: Optional[Decimal]

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# ORDEM DE COMPRA
# ──────────────────────────────────────────────

class OrdemCreate(BaseModel):
    numero: str
    solicitacao_id: int
    fornecedor_id: int
    cotacao_id: Optional[int] = None
    aprovacao_id: Optional[int] = None
    valor: Decimal
    quantidade: Decimal
    condicoes: Optional[str] = None
    documento_url: Optional[str] = None
    status: str = "COMPRA_OK"


class OrdemOut(BaseModel):
    id: int
    numero: str
    solicitacao_id: int
    fornecedor_id: int
    cotacao_id: Optional[int]
    aprovacao_id: Optional[int]
    valor: Decimal
    quantidade: Decimal
    condicoes: Optional[str]
    documento_url: Optional[str]
    status: str
    criado_em: Optional[datetime]

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# RECEBER
# ──────────────────────────────────────────────

class RecebimentoCreate(BaseModel):
    ordem_id: int
    quantidade_solicitada: Decimal
    quantidade_recebida: Decimal
    divergencia: Optional[str] = None
    responsavel: Optional[str] = None
    documento_url: Optional[str] = None
    fotos: Optional[str] = None
    observacao: Optional[str] = None
    status: StatusRecebimento = StatusRecebimento.PARCIAL


class RecebimentoOut(BaseModel):
    id: int
    ordem_id: int
    quantidade_solicitada: Decimal
    quantidade_recebida: Decimal
    divergencia: Optional[str]
    data_recebimento: Optional[datetime]
    responsavel: Optional[str]
    documento_url: Optional[str]
    fotos: Optional[str]
    observacao: Optional[str]
    status: StatusRecebimento

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# FINANCEIRO
# ──────────────────────────────────────────────

class LancamentoCreate(BaseModel):
    ordem_id: Optional[int] = None
    cliente_id: Optional[int] = None
    tipo: TipoLancamento
    categoria: Optional[str] = None
    descricao: str
    valor_previsto: Decimal
    valor_faturado: Decimal = Decimal("0.00")
    valor_pago: Decimal = Decimal("0.00")
    data_prevista: Optional[date] = None
    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None
    forma_pagamento: Optional[str] = None
    status: StatusLancamento = StatusLancamento.PREVISTO
    documento_url: Optional[str] = None
    observacao: Optional[str] = None


class LancamentoOut(BaseModel):
    id: int
    ordem_id: Optional[int]
    cliente_id: Optional[int]
    tipo: TipoLancamento
    categoria: Optional[str]
    descricao: str
    valor_previsto: Decimal
    valor_faturado: Decimal
    valor_pago: Decimal
    data_prevista: Optional[date]
    data_vencimento: Optional[date]
    data_pagamento: Optional[date]
    forma_pagamento: Optional[str]
    status: StatusLancamento
    documento_url: Optional[str]
    observacao: Optional[str]
    criado_em: Optional[datetime]
    atualizado_em: Optional[datetime]

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# AUDITORIA
# ──────────────────────────────────────────────

class AuditoriaOut(BaseModel):
    id: int
    usuario_id: Optional[int]
    acao: str
    entidade: str
    registro_id: Optional[int]
    ip_origem: Optional[str]
    user_agent: Optional[str]
    valor_anterior: Optional[str]
    valor_novo: Optional[str]
    timestamp: Optional[datetime]

    class Config:
        from_attributes = True


# ──────────────────────────────────────────────
# FILTERS
# ──────────────────────────────────────────────

class SolicitacaoFilter(BaseModel):
    status: Optional[StatusSolicitacao] = None
    cliente_id: Optional[int] = None
    solicitante_id: Optional[int] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    produto_id: Optional[int] = None


class LancamentoFilter(BaseModel):
    tipo: Optional[TipoLancamento] = None
    status: Optional[StatusLancamento] = None
    categoria: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    cliente_id: Optional[int] = None
    fornecedor_id: Optional[int] = None
