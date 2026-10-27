"""E-mails transacionais (Resend), push notifications (ntfy.sh) e webhooks ao proprietário."""
import html
from typing import Any, Dict, Optional

import httpx

from app.config import settings


async def send_email(to: str, subject: str, html_body: str, api_key: Optional[str] = None) -> bool:
    key = (api_key or settings.RESEND_API_KEY or "").strip()
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


async def notify_owner(
    title: str,
    text: str,
    spark_webhook: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Avisa o proprietário a cada novo lead quente ou venda:
    1) E-mail HTML com botão 1-Clique para chamar o lead no WhatsApp (via Resend, se configurado)
    2) Push Notification em tempo real no celular/PC via ntfy.sh (100% gratuito e sem cadastro)
    3) Webhook JSON (Make / n8n / Zapier / Evolution API) com link de abordagem pronto
    """
    extra = extra or {}
    wpp_pitch_url = extra.get("whatsapp_pitch_url", "")
    report_url = extra.get("report_url", "")

    # 1. E-mail HTML Rico (Resend)
    if settings.OWNER_EMAIL:
        cta_html = ""
        if wpp_pitch_url:
            cta_html += (
                f'<p style="margin-top:16px;">'
                f'<a href="{html.escape(wpp_pitch_url)}" style="background:#16a34a;color:#ffffff;padding:12px 20px;'
                f'border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;">'
                f'💬 Chamar Lead no WhatsApp Agora (Mensagem Pronta)</a></p>'
            )
        if report_url:
            cta_html += (
                f'<p style="margin-top:8px;font-size:13px;">'
                f'🔗 Relatório do cliente: <a href="{html.escape(report_url)}">{html.escape(report_url)}</a></p>'
            )
        html_body = (
            f'<div style="font-family:Arial,sans-serif;max-width:600px;padding:20px;border:1px solid #e2e8f0;border-radius:14px;">'
            f'<h3 style="color:#0f172a;margin-top:0;">{html.escape(title)}</h3>'
            f'<p style="color:#334155;line-height:1.6;">{html.escape(text).replace(chr(10), "<br>")}</p>'
            f'{cta_html}'
            f'<hr style="border:none;border-top:1px solid #e2e8f0;margin:16px 0;">'
            f'<p style="font-size:11px;color:#64748b;">Painel Admin: <a href="{settings.SITE_URL}/admin">{settings.SITE_URL}/admin</a></p>'
            f'</div>'
        )
        await send_email(settings.OWNER_EMAIL, f"[GeoPulse AI] {title}", html_body)

    # 2. Push Instantâneo Gratuito via ntfy.sh (funciona no navegador e app Android/iOS sem chave)
    ntfy_topic = getattr(settings, "NTFY_TOPIC", "geopulse_leads_mwfreitas")
    if ntfy_topic:
        try:
            headers = {
                "Title": title.encode("ascii", "ignore").decode("ascii").strip() or "Novo Lead GeoPulse AI",
                "Priority": "high",
                "Tags": "fire,rocket",
            }
            if wpp_pitch_url:
                headers["Click"] = wpp_pitch_url
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                await client.post(
                    f"https://ntfy.sh/{ntfy_topic}",
                    content=text.encode("utf-8"),
                    headers=headers,
                )
        except Exception:
            pass

    # 3. Webhook Externo (Make / n8n / Zapier / Evolution API)
    if spark_webhook:
        try:
            payload = {
                "event": "geopulse.owner_notification",
                "title": title,
                "text": text,
                **extra,
            }
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                await client.post(spark_webhook, json=payload)
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
