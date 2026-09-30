"""
Módulo Administrativo — Praia Digital

Entidades: Cliente, Produto/Servico, Fornecedor, SolicitacaoCompra, Cotacao,
OrdemCompra, Recebimento, Financeiro (Contas pagar/receber), CentroCusto,
Auditoria, AccessLog

Todas as alterações geram histórico (nunca sobrescrita silenciosa).
Toda compra vincula: solicitante + cliente/projeto + produto + fornecedor +
cotacao + aprovacao + valor + pagamento + documento + recebimento.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Enum, ForeignKey,
    Numeric, Boolean, Date, func, UniqueConstraint
)
from sqlalchemy.orm import relationship
from academy.core.database import Base
from datetime import datetime
import enum


# ──────────────────────────────────────────────
# PERMISSÕES E ACESSOS
# ──────────────────────────────────────────────

class PerfisUsuario(str, enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    FINANCEIRO     = "FINANCEIRO"
    COMPRAS        = "COMPRAS"
    COMERCIAL      = "COMERCIAL"
    OPERACIONAL    = "OPERACIONAL"
    CONSULTA       = "CONSULTA"


class Usuario(Base):
    __tablename__ = "admin_usuarios"

    id          = Column(Integer, primary_key=True, index=True)
    username    = Column(String(60), unique=True, nullable=False, index=True)
    nome        = Column(String(200), nullable=False)
    email       = Column(String(200), unique=True, nullable=False)
    cpf         = Column(String(14), unique=True, nullable=True)   # <-- dado sensível
    senha_hash  = Column(String(255), nullable=False)             # <-- hash, nunca plain
    perfil      = Column(Enum(PerfilUsuario), nullable=False)
    ativo       = Column(Boolean, default=True)
    criado_em   = Column(DateTime(timezone=True), server_default=func.now())
    ultimo_login = Column(DateTime(timezone=True), nullable=True)


# ──────────────────────────────────────────────
# CLIENTES (pessoas físicas ou jurídicas)
# ──────────────────────────────────────────────

class TipoCliente(str, enum.Enum):
    PF = "PF"
    PJ = "PJ"


class Cliente(Base):
    __tablename__ = "admin_clientes"

    id          = Column(Integer, primary_key=True, index=True)
    tipo        = Column(Enum(TipoCliente), nullable=False)
    nome        = Column(String(200), nullable=False)
    cpf_cnpj    = Column(String(20), unique=True, index=True)    # <-- dado sensível
    email       = Column(String(200), nullable=True)
    telefone    = Column(String(40), nullable=True)
    endereco    = Column(Text, nullable=True)
    cidade      = Column(String(120), nullable=True)
    estado      = Column(String(2), nullable=True)
    cep         = Column(String(12), nullable=True)
    origem      = Column(String(120), nullable=True)
    status      = Column(String(40), default="ativo")
    observacao  = Column(Text, nullable=True)
    criado_em   = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("tipo", "cpf_cnpj", name="uq_cliente_tipo_doc"),
    )


# ──────────────────────────────────────────────
# PRODUTOS / SERVIÇOS
# ──────────────────────────────────────────────

class TipoProduto(str, enum.Enum):
    PRODUTO  = "PRODUTO"
    SERVICO  = "SERVICO"


class Produto(Base):
    __tablename__ = "admin_produtos"

    id           = Column(Integer, primary_key=True, index=True)
    sku          = Column(String(60), unique=True, index=True)
    nome         = Column(String(200), nullable=False)
    tipo         = Column(Enum(TipoProduto), nullable=False, default=TipoProduto.SERVICO)
    categoria    = Column(String(120), nullable=True)
    descricao    = Column(Text, nullable=True)
    unidade      = Column(String(20), nullable=True)
    custo        = Column(Numeric(12, 2), default=0)
    preco        = Column(Numeric(12, 2), default=0)
    tem_estoque  = Column(Boolean, default=False)
    estoque_atual = Column(Integer, default=0)
    estoque_min   = Column(Integer, default=0)
    ativo        = Column(Boolean, default=True)
    fornecedor_id = Column(Integer, ForeignKey("admin_fornecedores.id"), nullable=True)
    criado_em    = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ──────────────────────────────────────────────
# FORNECEDORES
# ──────────────────────────────────────────────

class Fornecedor(Base):
    __tablename__ = "admin_fornecedores"

    id         = Column(Integer, primary_key=True, index=True)
    razao_social = Column(String(200), nullable=False)
    cnpj       = Column(String(20), unique=True, index=True)   # <-- dado sensível
    contato_nome = Column(String(200), nullable=True)
    contato_telefone = Column(String(40), nullable=True)
    contato_email = Column(String(200), nullable=True)
    endereco   = Column(Text, nullable=True)
    cidade     = Column(String(120), nullable=True)
    estado     = Column(String(2), nullable=True)
    condicoes_comerciais = Column(Text, nullable=True)
    ativo      = Column(Boolean, default=True)
    criado_em  = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ──────────────────────────────────────────────
# CENTRO DE CUSTO (vinculado a cliente/projeto)
# ──────────────────────────────────────────────

class CentroCusto(Base):
    __tablename__ = "admin_centros_custo"

    id          = Column(Integer, primary_key=True, index=True)
    codigo      = Column(String(40), unique=True, nullable=False)
    nome        = Column(String(200), nullable=False)
    cliente_id  = Column(Integer, ForeignKey("admin_clientes.id"), nullable=True)
    orcamento   = Column(Numeric(14, 2), default=0)
    ativo       = Column(Boolean, default=True)


# ──────────────────────────────────────────────
# SOLICITAÇÃO DE COMPRA (abre o fluxo)
# ──────────────────────────────────────────────

class StatusSolicitacao(str, enum.Enum):
    SOLICITADA   = "SOLICITADA"
    COTACAO      = "COTACAO"
    APROVADA     = "APROVADA"
    REJEITADA    = "REJEITADA"
    COMPRA_OK    = "COMPRA_OK"
    PAGA         = "PAGA"
    RECEBIDA     = "RECEBIDA"
    FINALIZADA   = "FINALIZADA"
    CANCELADA    = "CANCELADA"


class SolicitacaoCompra(Base):
    __tablename__ = "admin_solicitacoes_compra"

    id             = Column(Integer, primary_key=True, index=True)
    numero         = Column(String(40), unique=True, nullable=False)
    solicitante_id = Column(Integer, ForeignKey("admin_usuarios.id"), nullable=False)
    cliente_id     = Column(Integer, ForeignKey("admin_clientes.id"), nullable=True)
    centro_custo_id = Column(Integer, ForeignKey("admin_centros_custo.id"), nullable=True)
    produto_id     = Column(Integer, ForeignKey("admin_produtos.id"), nullable=False)
    quantidade     = Column(Numeric(12, 4), nullable=False)
    finalidade     = Column(Text, nullable=True)
    orcamento      = Column(Numeric(14, 2), nullable=True)
    status         = Column(Enum(StatusSolicitacao), default=StatusSolicitacao.SOLICITADA)
    observacao     = Column(Text, nullable=True)
    criado_em      = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    solicitante  = relationship("Usuario", foreign_keys=[solicitante_id])
    cliente      = relationship("Cliente", foreign_keys=[cliente_id])
    centro_custo = relationship("CentroCusto", foreign_keys=[centro_custo_id])
    produto      = relationship("Produto", foreign_keys=[produto_id])
    cotacoes     = relationship("Cotacao", back_populates="solicitacao", cascade="all, delete-orphan")
    ordens       = relationship("OrdemCompra", back_populates="solicitacao", cascade="all, delete-orphan")


# ──────────────────────────────────────────────
# COTAÇÕES (múltiplas por solicitação)
# ──────────────────────────────────────────────

class Cotacao(Base):
    __tablename__ = "admin_cotacoes"

    id              = Column(Integer, primary_key=True, index=True)
    solicitacao_id  = Column(Integer, ForeignKey("admin_solicitacoes_compra.id"), nullable=False)
    fornecedor_id   = Column(Integer, ForeignKey("admin_fornecedores.id"), nullable=False)
    preco_unitario  = Column(Numeric(14, 2), nullable=False)
    quantidade      = Column(Numeric(12, 4), nullable=False)
    frete           = Column(Numeric(14, 2), default=0)
    taxas           = Column(Numeric(14, 2), default=0)
    desconto        = Column(Numeric(14, 2), default=0)
    valor_total     = Column(Numeric(14, 2), nullable=False)
    prazo_entrega   = Column(String(120), nullable=True)
    condicoes       = Column(Text, nullable=True)  # ex: "30 dias"
    validade        = Column(Date, nullable=True)
    observacao      = Column(Text, nullable=True)
    docstring_url   = Column(String(500), nullable=True)  # link da proposta
    criado_em       = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    solicitacao = relationship("SolicitacaoCompra", back_populates="cotacoes")
    fornecedor  = relationship("Fornecedor", foreign_keys=[fornecedor_id])


# ──────────────────────────────────────────────
# APROVAÇÃO
# ──────────────────────────────────────────────

class Aprovacao(Base):
    __tablename__ = "admin_aprovacoes"

    id              = Column(Integer, primary_key=True, index=True)
    solicitacao_id  = Column(Integer, ForeignKey("admin_solicitacoes_compra.id"), nullable=False)
    aprovador_id    = Column(Integer, ForeignKey("admin_usuarios.id"), nullable=False)
    valor_aprovado  = Column(Numeric(14, 2), nullable=False)
    data_hora       = Column(DateTime(timezone=True), server_default=func.now())
    justificativa   = Column(Text, nullable=True)
    limite_configurado = Column(Numeric(14, 2), nullable=True)

    # Relacionamentos
    aprovador = relationship("Usuario", foreign_keys=[aprovador_id])


# ──────────────────────────────────────────────
# ORDEM / REGISTRO DE COMPRA
# ──────────────────────────────────────────────

class OrdemCompra(Base):
    __tablename__ = "admin_ordens_compra"

    id              = Column(Integer, primary_key=True, index=True)
    numero          = Column(String(40), unique=True, nullable=False)
    solicitacao_id  = Column(Integer, ForeignKey("admin_solicitacoes_compra.id"), nullable=False)
    fornecedor_id   = Column(Integer, ForeignKey("admin_fornecedores.id"), nullable=False)
    cotacao_id      = Column(Integer, ForeignKey("admin_cotacoes.id"), nullable=True)
    aprovacao_id    = Column(Integer, ForeignKey("admin_aprovacoes.id"), nullable=True)
    valor           = Column(Numeric(14, 2), nullable=False)
    quantidade      = Column(Numeric(12, 4), nullable=False)
    condicoes       = Column(Text, nullable=True)
    documento_url   = Column(String(500), nullable=True)
    status          = Column(String(40), default="COMPRA_OK")
    criado_em       = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relacionamentos
    solicitacao = relationship("SolicitacaoCompra", back_populates="ordens")
    fornecedor  = relationship("Fornecedor", foreign_keys=[fornecedor_id])


# ──────────────────────────────────────────────
# RECEBER (entrada de mercadorias)
# ──────────────────────────────────────────────

class StatusRecebimento(str, enum.Enum):
    RECEBIDO     = "RECEBIDO"
    PARCIAL      = "PARCIAL"
    DIVERGENTE   = "DIVERGENTE"
    RECUSADO     = "RECUSADO"
    CONFERIDO    = "CONFERIDO"


class Recebimento(Base):
    __tablename__ = "admin_recebimentos"

    id              = Column(Integer, primary_key=True, index=True)
    ordem_id        = Column(Integer, ForeignKey("admin_ordens_compra.id"), nullable=False)
    quantidade_solicitada = Column(Numeric(12, 4), nullable=False)
    quantidade_recebida   = Column(Numeric(12, 4), nullable=False)
    divergencia     = Column(Text, nullable=True)
    data_recebimento = Column(DateTime(timezone=True), server_default=func.now())
    responsavel     = Column(String(200), nullable=True)
    documento_url   = Column(String(500), nullable=True)
    fotos           = Column(Text, nullable=True)  # JSON array de URLs
    observacao      = Column(Text, nullable=True)
    status          = Column(Enum(StatusRecebimento), default=StatusRecebimento.PARCIAL)

    # Relacionamentos
    ordem = relationship("OrdemCompra", foreign_keys=[ordem_id])


# ──────────────────────────────────────────────
# FINANCEIRO (contas a pagar / receber)
# ──────────────────────────────────────────────

class TipoLancamento(str, enum.Enum):
    DESPESA      = "DESPESA"
    RECEITA      = "RECEITA"
    TRANSFERENCIA = "TRANSFERENCIA"


class StatusLancamento(str, enum.Enum):
    PREVISTO   = "PREVISTO"     # orçado
    FATURADO   = "FATURADO"     # emitido NF
    PAGO       = "PAGO"         # dinheiro saiu/entrou
    RECEBIDO   = "RECEBIDO"     # dinheiro efetivamente recebido


class LancamentoFinanceiro(Base):
    __tablename__ = "admin_lancamentos"

    id            = Column(Integer, primary_key=True, index=True)
    ordem_id      = Column(Integer, ForeignKey("admin_ordens_compra.id"), nullable=True)
    cliente_id    = Column(Integer, ForeignKey("admin_clientes.id"), nullable=True)
    tipo          = Column(Enum(TipoLancamento), nullable=False)
    categoria     = Column(String(120), nullable=True)
    descricao     = Column(Text, nullable=False)
    valor_previsto = Column(Numeric(14, 2), nullable=False)   # sempre preenchido
    valor_faturado = Column(Numeric(14, 2), default=0)
    valor_pago     = Column(Numeric(14, 2), default=0)        # separado do faturado
    data_prevista  = Column(Date, nullable=True)
    data_vencimento = Column(Date, nullable=True)
    data_pagamento = Column(Date, nullable=True)
    forma_pagamento = Column(String(80), nullable=True)
    status         = Column(Enum(StatusLancamento), default=StatusLancamento.PREVISTO)
    documento_url  = Column(String(500), nullable=True)     # comprovante/DOC/PIX
    observacao     = Column(Text, nullable=True)
    criado_em      = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em  = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ──────────────────────────────────────────────
# AUDITORIA TOTAL
# ──────────────────────────────────────────────

class AuditoriaLog(Base):
    __tablename__ = "admin_auditoria"

    id              = Column(Integer, primary_key=True, index=True)
    usuario_id      = Column(Integer, ForeignKey("admin_usuarios.id"), nullable=True)
    acao            = Column(String(120), nullable=False)          # "create", "update", "delete", "approve", "login"
    entidade        = Column(String(80), nullable=False)           # ex: "SolicitacaoCompra"
    registro_id     = Column(Integer, nullable=True)
    ip_origem       = Column(String(60), nullable=True)
    user_agent      = Column(Text, nullable=True)
    valor_anterior  = Column(Text, nullable=True)                  # JSON snapshot
    valor_novo      = Column(Text, nullable=True)                  # JSON snapshot
    timestamp       = Column(DateTime(timezone=True), server_default=func.now())

    # Relacionamentos
    usuario = relationship("Usuario", foreign_keys=[usuario_id])
