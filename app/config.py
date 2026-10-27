from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DATABASE_URL: str = "sqlite+aiosqlite:///./geopulse.db"

    # API Keys & Webhooks (Gratuitas e Pagas)
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    OPENROUTER_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    HUGGINGFACE_API_KEY: Optional[str] = None
    TAVILY_API_KEY: Optional[str] = None
    DEVTO_API_KEY: Optional[str] = None
    MEDIUM_API_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    PERPLEXITY_API_KEY: Optional[str] = None
    SPARK_WEBHOOK_URL: Optional[str] = None

    # Pagamentos (Mercado Pago + PIX) & Segurança Admin
    MERCADOPAGO_ACCESS_TOKEN: Optional[str] = None
    MERCADOPAGO_PUBLIC_KEY: Optional[str] = None
    PIX_KEY: str = "contato@geopulse.ai"
    PIX_BENEFICIARY: str = "GeoPulse AI Tecnologia"
    PLAN_PRICE: float = 197.0
    ADMIN_PASSWORD: str = "mcga12345"

    # Domínio público oficial (usado em links de e-mail, sitemap, WhatsApp e CORS)
    SITE_URL: str = "https://geopulseai.store"
    ALLOWED_ORIGINS: str = ""  # Origens extras separadas por vírgula (opcional)

    # E-mail transacional (Resend: https://resend.com) e notificações para o proprietário
    RESEND_API_KEY: Optional[str] = None
    MAIL_FROM: str = "GeoPulse AI <onboarding@resend.dev>"
    OWNER_EMAIL: Optional[str] = "mwfreitas@gmail.com"
    NTFY_TOPIC: str = "geopulse_leads_mwfreitas"

    # Proteção contra abuso e custos de API
    DIAG_RATE_PER_HOUR: int = 6        # Diagnósticos por IP por hora
    UPLOAD_RATE_PER_HOUR: int = 20     # Uploads de foto por IP por hora
    LEAD_RATE_PER_HOUR: int = 15       # Capturas de lead / chat por IP por hora
    MAX_CONCURRENT_AUDITS: int = 3     # Auditorias simultâneas (as demais aguardam na fila)
    UPLOAD_MAX_MB: int = 5

    # Backup automático do banco SQLite
    BACKUP_DIR: str = "backups"
    BACKUP_KEEP: int = 14              # Quantidade de backups diários mantidos
    MONITOR_INTERVAL_DAYS: int = 30    # Reauditoria automática de clientes pagos

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
