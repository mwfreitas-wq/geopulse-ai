"""E-mails transacionais (Resend) e avisos ao proprietário. Tudo é opcional: sem chave configurada, nada quebra."""
import html
from typing import Optional

import httpx

from app.config import settings


async def send_email(to: str, subject: str, html_body: str) -> bool:
    key = (settings.RESEND_API_KEY or "").strip()
    if not key or not to or "@" not in to:
        return False
    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            res = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={"from": settings.MAIL_FROM, "to": [to], "subject": subject, "html": html_body},
            )
            return res.status_code in (200, 201, 202)
    except Exception:
        return False


async def notify_owner(title: str, text: str, spark_webhook: Optional[str] = None) -> None:
    """Avisa o proprietário a cada novo lead/venda por e-mail e pelo webhook (Make/n8n -> WhatsApp)."""
    if settings.OWNER_EMAIL:
        await send_email(
            settings.OWNER_EMAIL,
            f"[GeoPulse AI] {title}",
            f"<h3>{html.escape(title)}</h3><p>{html.escape(text).replace(chr(10), '<br>')}</p>",
        )
    if spark_webhook:
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                await client.post(spark_webhook, json={"event": "geopulse.owner_notification", "title": title, "text": text})
        except Exception:
            pass


async def send_delivery_email(company, client_area_url: str, published_url: Optional[str]) -> bool:
    if not company.email:
        return False
    name = html.escape(company.name)
    pub = (
        f'<p>📄 <a href="{html.escape(published_url)}">Seu artigo de autoridade publicado</a></p>' if published_url else ""
    )
    body = f"""
    <div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;color:#0f172a">
      <h2 style="color:#047857">🚀 {name}, sua presença nas IAs foi ativada!</h2>
      <p>Seus ativos de GEO/AIO (Schema.org JSON-LD, llms.txt, FAQ e artigo de autoridade) já estão prontos e sendo indexados por ChatGPT, Gemini e Perplexity.</p>
      <p>🔐 <a href="{html.escape(client_area_url)}"><b>Acessar minha Área do Cliente</b></a> (guarde este link: é seu acesso pessoal)</p>
      {pub}
      <p style="color:#64748b;font-size:12px">Você receberá um relatório de evolução periodicamente. Dúvidas? Responda este e-mail.</p>
    </div>"""
    return await send_email(company.email, "Sua presença nas IAs foi ativada ✅", body)
