from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, HttpUrl, Field


# Schemas para Cadastro de Empresa ou Profissional Autônomo
class CompanyCreate(BaseModel):
    entity_type: str = Field(default="company", description="'company' para Empresa/Clínica ou 'autonomous' para Profissional Autônomo")
    name: str = Field(..., description="Nome da Empresa ou do Profissional", min_length=2)
    url: str = Field(..., description="URL do site, landing page, LinkedIn ou Instagram profissional")
    niche: str = Field(..., description="Nicho ou Especialidade (ex: Advogado Trabalhista, Psicóloga TCC, Escritório Contábil)")
    city_region: str = Field(..., description="Cidade e Estado ou Região (ex: São Paulo - SP)")
    professional_registry: Optional[str] = Field(default="", description="Registro de classe opcional (ex: OAB/SP, CRP, CRC, CRM, CRO, CREA)")
    photo_url: Optional[str] = Field(default="", description="URL ou caminho local da foto de perfil ou logotipo")
    rating_value: Optional[float] = Field(default=None, description="Nota média de avaliação dos clientes/Google (ex: 4.9)")
    review_count: Optional[int] = Field(default=None, description="Quantidade de avaliações recebidas (ex: 48)")
    services_list: Optional[str] = Field(default="", description="Principais serviços ou procedimentos separados por vírgula (ex: Consulta, Clareamento, Implante)")
    whatsapp: Optional[str] = Field(default="", description="WhatsApp com DDD do cliente/lead para contato comercial")
    email: Optional[str] = Field(default="", description="E-mail do cliente/lead")
    competitors: Optional[str] = Field(default="", description="Até 3 concorrentes ou outros profissionais separados por vírgula")
    language: Optional[str] = Field(default="pt", description="Idioma do visitante: pt, en ou es")


class PhotoUploadRequest(BaseModel):
    image_base64: str = Field(..., description="Imagem codificada em base64 (data:image/jpeg;base64,...)")
    filename: Optional[str] = Field(default="perfil.jpg", description="Nome original do arquivo")


class CompanyResponse(BaseModel):
    id: int
    entity_type: Optional[str] = "company"
    name: str
    url: str
    niche: str
    city_region: str
    professional_registry: Optional[str] = None
    photo_url: Optional[str] = None
    rating_value: Optional[float] = None
    review_count: Optional[int] = None
    services_list: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    competitors: Optional[str] = None
    scraped_title: Optional[str] = None
    is_paid: bool = False
    payment_plan: Optional[str] = None
    payment_amount: Optional[float] = 197.0
    payment_method: Optional[str] = "pix"
    paid_at: Optional[datetime] = None
    access_token: Optional[str] = None
    sprint_status: Optional[str] = "pending"
    sprint_day_current: Optional[int] = 0
    sprint_started_at: Optional[datetime] = None
    sprint_last_run_at: Optional[datetime] = None
    sprint_logs: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas para Auditoria
class AuditRunResponse(BaseModel):
    id: int
    company_id: int
    model_provider: str
    prompt_category: str
    prompt_text: str
    response_text: str
    is_cited: bool
    rank_position: Optional[int] = None
    sentiment: str
    sources: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


# Schemas para Ativos Gerados
class GeneratedAssetResponse(BaseModel):
    id: int
    company_id: int
    asset_type: str
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# Schema para Sugestões Estratégicas na Consulta Gratuita
class StrategicSuggestion(BaseModel):
    title: str
    problem: str
    impact: str
    solution_preview: str


# Schema para Dashboard / Diagnóstico Completo
class DiagnosticMetrics(BaseModel):
    visibility_score: float  # 0 a 100%
    citation_rate: float     # 0 a 100%
    average_sentiment: str   # Positivo, Neutro, Negativo, Ausente
    total_prompts: int
    cited_count: int
    top_rank_achieved: Optional[int] = None


class FullDiagnosticResponse(BaseModel):
    company: CompanyResponse
    metrics: DiagnosticMetrics
    before_metrics: Optional[DiagnosticMetrics] = None
    suggestions: List[StrategicSuggestion] = []
    audits: List[AuditRunResponse]
    before_audits: List[AuditRunResponse] = []
    assets: List[GeneratedAssetResponse] = []
    published_url: Optional[str] = None


class CheckoutRequest(BaseModel):
    plan_name: str = "Plano Dominância IA (GEO + AIO Autônomo)"
    payment_method: str = "pix"  # pix, credit_card ou mercadopago
    amount: float = 197.0


class AdminLoginRequest(BaseModel):
    password: str


# Configurações de API Keys + Pagamento Mercado Pago / PIX
class ApiKeysUpdate(BaseModel):
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    mistral_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    tavily_api_key: Optional[str] = None
    devto_api_key: Optional[str] = None
    medium_api_token: Optional[str] = None
    openai_api_key: Optional[str] = None
    perplexity_api_key: Optional[str] = None
    spark_webhook_url: Optional[str] = None
    mercadopago_access_token: Optional[str] = None
    mercadopago_public_key: Optional[str] = None
    pix_key: Optional[str] = None
    pix_beneficiary: Optional[str] = None
    plan_price: Optional[str] = None


class ApiKeysStatus(BaseModel):
    gemini_configured: bool = False
    groq_configured: bool = False
    openrouter_configured: bool = False
    mistral_configured: bool = False
    huggingface_configured: bool = False
    tavily_configured: bool = False
    devto_configured: bool = False
    medium_configured: bool = False
    openai_configured: bool = False
    perplexity_configured: bool = False
    spark_configured: bool = False
    mercadopago_configured: bool = False
    mercadopago_public_key: Optional[str] = None
    pix_key: str = "contato@geopulse.ai"
    pix_beneficiary: str = "GeoPulse AI Tecnologia"
    plan_price: float = 197.0
    spark_webhook_url: Optional[str] = None
    configured_count: int = 0
    active_providers: List[str] = []
    active_mode: str = "simulation"  # "live" ou "simulation"


# Schemas da Área Administrativa (Vendas, Clientes e Histórico)
class AdminCustomerRecord(BaseModel):
    id: int
    entity_type: str
    name: str
    url: str
    niche: str
    city_region: str
    professional_registry: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    competitors: Optional[str] = None
    is_paid: bool
    payment_plan: Optional[str] = None
    payment_amount: float = 197.0
    payment_method: Optional[str] = "pix"
    paid_at: Optional[datetime] = None
    access_token: Optional[str] = None
    payment_ref: Optional[str] = None
    sprint_status: Optional[str] = "pending"
    sprint_day_current: Optional[int] = 0
    sprint_started_at: Optional[datetime] = None
    created_at: datetime
    initial_score: float
    current_score: float
    audits_count: int = 0
    assets_count: int = 0
    published_url: Optional[str] = None


class AdminFinancialSummary(BaseModel):
    total_revenue: float
    total_sales_count: int
    total_consultations: int
    pending_leads_count: int
    captured_leads_count: int = 0
    conversion_rate: float
    average_ticket: float
    autonomous_count: int
    company_count: int
    pix_sales_count: int
    card_sales_count: int


class AdminOverviewResponse(BaseModel):
    financials: AdminFinancialSummary
    api_status: ApiKeysStatus
    sales: List[AdminCustomerRecord]
    customers: List[AdminCustomerRecord]


# Schemas para Captura de Leads (Dossiê PDF por E-mail/WhatsApp)
class LeadCaptureCreate(BaseModel):
    company_id: Optional[int] = None
    company_name: str
    contact_name: Optional[str] = ""
    contact_email: Optional[str] = ""
    contact_phone: Optional[str] = ""
    niche: Optional[str] = ""
    city_region: Optional[str] = ""
    score: Optional[float] = 0.0


class LeadCaptureResponse(BaseModel):
    id: int
    company_id: Optional[int] = None
    company_name: str
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    niche: Optional[str] = None
    city_region: Optional[str] = None
    score: float = 0.0
    status: str = "Novo Lead"
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LeadStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = None


# Schema para Modo Agência (Proposta Comercial & Scripts de Venda)
class ProposalGenerateRequest(BaseModel):
    company_name: str
    niche: str
    city_region: str
    competitors: Optional[str] = ""
    score: float = 0.0
    top_rank: Optional[int] = None
    agency_name: Optional[str] = "Sua Agência / Consultoria GEO"
    consultant_name: Optional[str] = "Especialista em IA"
    consultant_whatsapp: Optional[str] = ""
    proposal_price: Optional[float] = 1970.0
    monthly_retainer: Optional[float] = 490.0




# Schemas do Plano Sprint de 14 Dias
class SprintDayLog(BaseModel):
    day: int
    date: str
    title: str
    details: str
    status: str  # completed, in_progress, pending


class SprintInfoResponse(BaseModel):
    company_id: int
    company_name: str
    sprint_status: str
    sprint_day_current: int
    sprint_days_total: int = 14
    progress_percent: float
    sprint_started_at: Optional[datetime] = None
    sprint_last_run_at: Optional[datetime] = None
    logs: List[SprintDayLog] = []
    current_score: float
    initial_score: float


# Schemas para o Robô de Vendas Inteligente (AI Closer & Sales Hunter)
class SalesBotChatRequest(BaseModel):
    message: str
    company_name: Optional[str] = None
    niche: Optional[str] = None
    city_region: Optional[str] = None
    score: Optional[float] = None
    top_competitor: Optional[str] = None
    language: Optional[str] = 'pt'
    conversation_history: Optional[List[dict]] = None
    report_id: Optional[int] = None


class SalesBotHuntRequest(BaseModel):
    niche: str
    city_region: str
    quantity: Optional[int] = 5
    auto_audit: Optional[bool] = True
    auto_email: Optional[bool] = False
