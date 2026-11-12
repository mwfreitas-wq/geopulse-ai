import json
import zlib
import base64
from sqlalchemy import text

SEED_B64 = """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"""

async def restore_seed_vault(conn):
    try:
        raw = zlib.decompress(base64.b64decode(SEED_B64.strip())).decode("utf-8")
        data = json.loads(raw)

        # 1. System Settings
        for s in data.get("system_settings", []):
            k, v = s.get("key"), s.get("value")
            if k:
                await conn.execute(
                    text("INSERT OR REPLACE INTO system_settings (key, value) VALUES (:k, :v)"),
                    {"k": k, "v": v or ""}
                )

        # 2. Companies
        for c in data.get("companies", []):
            await conn.execute(
                text("""INSERT OR IGNORE INTO companies (
                    id, name, url, niche, city_region, entity_type, whatsapp, email,
                    competitors, is_paid, payment_amount, access_token, sprint_status, created_at
                ) VALUES (
                    :id, :name, :url, :niche, :city_region, :entity_type, :whatsapp, :email,
                    :competitors, 0, :payment_amount, :access_token, :sprint_status, :created_at
                )"""),
                {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "url": c.get("url") or "",
                    "niche": c.get("niche") or "",
                    "city_region": c.get("city_region") or "",
                    "entity_type": c.get("entity_type") or "company",
                    "whatsapp": c.get("whatsapp") or "",
                    "email": c.get("email") or "",
                    "competitors": c.get("competitors") or "",
                    "payment_amount": c.get("payment_amount") or 197.0,
                    "access_token": c.get("access_token"),
                    "sprint_status": c.get("sprint_status") or "pending",
                    "created_at": c.get("created_at")
                }
            )

        # 3. Leads
        for l in data.get("leads", []):
            await conn.execute(
                text("""INSERT OR IGNORE INTO lead_captures (
                    id, company_id, company_name, contact_name, contact_email, contact_phone,
                    niche, city_region, score, status, notes, created_at
                ) VALUES (
                    :id, :company_id, :company_name, :contact_name, :contact_email, :contact_phone,
                    :niche, :city_region, :score, :status, :notes, :created_at
                )"""),
                {
                    "id": l.get("id"),
                    "company_id": l.get("company_id"),
                    "company_name": l.get("company_name"),
                    "contact_name": l.get("contact_name") or "Diretoria",
                    "contact_email": l.get("contact_email") or "",
                    "contact_phone": l.get("contact_phone") or "",
                    "niche": l.get("niche") or "",
                    "city_region": l.get("city_region") or "",
                    "score": l.get("score") or 32.5,
                    "status": l.get("status") or "Novo Lead",
                    "notes": l.get("notes") or "Restaurado via Cofre",
                    "created_at": l.get("created_at")
                }
            )
    except Exception as e:
        pass
