import secrets

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON

from sqlalchemy.orm import relationship

from app.database import Base

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), default="company")
    name = Column(String(255), nullable=False, index=True)
    url = Column(String(500), nullable=False)
    niche = Column(String(255), nullable=False)
    city_region = Column(String(255), nullable=False)
    professional_registry = Column(String(120), nullable=True)
    photo_url = Column(String(500), nullable=True)
    rating_value = Column(Float, nullable=True)
    review_count = Column(Integer, nullable=True)
    services_list = Column(String(500), nullable=True)
    whatsapp = Column(String(60), nullable=True)
    email = Column(String(150), nullable=True)
    competitors = Column(String(500), nullable=True)
    scraped_content = Column(Text, nullable=True)
    scraped_title = Column(String(500), nullable=True)
    is_paid = Column(Boolean, default=False)
    payment_plan = Column(String(100), nullable=True)
    payment_amount = Column(Float, default=197.0)
    payment_method = Column(String(50), default="pix")
    paid_at = Column(DateTime, nullable=True)
    access_token = Column(String(64), nullable=True, index=True, default=lambda: secrets.token_urlsafe(24))
    payment_ref = Column(String(100), nullable=True)
    last_monitored_at = Column(DateTime, nullable=True)
    sprint_status = Column(String(50), default="pending", nullable=True)
    sprint_day_current = Column(Integer, default=0, nullable=True)
    sprint_started_at = Column(DateTime, nullable=True)
    sprint_last_run_at = Column(DateTime, nullable=True)
    sprint_logs = Column(Text, nullable=True)
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    audits = relationship("AuditRun", back_populates="company", cascade="all, delete-orphan")
    assets = relationship("GeneratedAsset", back_populates="company", cascade="all, delete-orphan")

class AuditRun(Base):
    __tablename__ = "audit_runs"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    model_provider = Column(String(50), nullable=False)
    prompt_category = Column(String(100), nullable=False)
    prompt_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=False)
    is_cited = Column(Boolean, default=False)
    rank_position = Column(Integer, nullable=True)
    sentiment = Column(String(50), default="Ausente")
    sources = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="audits")

class GeneratedAsset(Base):
    __tablename__ = "generated_assets"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    asset_type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    company = relationship("Company", back_populates="assets")

class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class LeadCapture(Base):
    __tablename__ = "lead_captures"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="SET NULL"), nullable=True)
    company_name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(60), nullable=True)
    niche = Column(String(255), nullable=True)
    city_region = Column(String(255), nullable=True)
    score = Column(Float, default=0.0)
    status = Column(String(50), default="Novo Lead")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ScoreHistory(Base):
    __tablename__ = "score_history"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    visibility_score = Column(Float, default=0.0)
    cited_count = Column(Integer, default=0)
    total_prompts = Column(Integer, default=0)
    source = Column(String(40), default="diagnostico")
    created_at = Column(DateTime, default=datetime.utcnow)

class SiteEvent(Base):
    __tablename__ = "site_events"
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String(40), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
