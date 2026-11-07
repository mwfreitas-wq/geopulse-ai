"""
Módulo de Integração com a API Oficial do Gumroad (v2).
Permite a criação, atualização e sincronização 100% autônoma de produtos com HTML Rico,
imagens embutidas de alta resolução, custom_summary e processamento de webhooks (Pings).
"""
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger("geopulse.gumroad")


class GumroadService:
    BASE_URL = "https://api.gumroad.com/v2"

    @classmethod
    def get_main_product_html_description(cls, site_url: str = "https://geopulseai.store") -> str:
        base = site_url.rstrip("/")
        return (
            f'<p><img src="{base}/api/ebooks/image/dental-clinics-implantology/cover.png" alt="GeoPulse AI — 14-Day AI Search Visibility Sprint" /></p>'
            f"<h2>GeoPulse AI — 14-Day AI Search Visibility Sprint (Top 10 on ChatGPT &amp; Google Gemini)</h2>"
            f"<p>Secure your business at the forefront of the <strong>Generative AI Search Revolution</strong>. When potential clients ask <strong>ChatGPT, Google Gemini, Copilot, or Perplexity</strong> for the top providers in your city and industry, ensure your brand gets recommended first.</p>"
            f'<p><img src="{base}/api/ebooks/image/dental-clinics-implantology/chart.png" alt="AI Search Conversion Data" /></p>'
            f"<h3>🚀 What is Included in Your 14-Day Autonomous Sprint:</h3>"
            f"<ul>"
            f"<li><strong>Official <code>/llms.txt</code> &amp; <code>/llms-full.txt</code> Entity Asset:</strong> Standardized machine-readable context file hosted for AI crawlers to accurately cite and prioritize your business.</li>"
            f"<li><strong>Verified Schema.org JSON-LD Knowledge Graph:</strong> Multi-type rich structured entity data for Google Gemini &amp; Microsoft Copilot.</li>"
            f"<li><strong>High-Authority AI Editorial Article &amp; FAQ:</strong> Optimized for retrieval-augmented generation (RAG) and direct conversational answers.</li>"
            f"<li><strong>Priority IndexNow Protocol Pings:</strong> Instant notifications sent to Microsoft Bing and ChatGPT Search indices within minutes.</li>"
            f"<li><strong>Live Visibility &amp; Sentiment Score (0–100):</strong> Real-time monitoring of your entity ranking across all major AI engines.</li>"
            f"<li><strong>Zero Tech Friction:</strong> No changes to your existing website codebase or expensive developer hours required.</li>"
            f"</ul>"
            f'<p><img src="{base}/api/ebooks/image/dental-clinics-implantology/architecture.png" alt="4-Pillar GEO Architecture" /></p>'
            f"<hr />"
            f"<h3>🛡️ Ironclad 7-Day Money-Back Guarantee</h3>"
            f"<p>Try <strong>GeoPulse AI</strong> 100% risk-free. Once your order is completed, our autonomous engine immediately activates your 7 entity assets and sends your private dashboard credentials to your email. If you are not completely satisfied within 7 days, request an immediate full refund—no questions asked.</p>"
        )

    @classmethod
    async def create_product(
        cls,
        access_token: str,
        name: str = "GeoPulse AI — 14-Day AI Search Visibility Sprint (Top 10 on ChatGPT & Gemini)",
        price_cents: int = 4700,
        currency: str = "usd",
        description: Optional[str] = None,
        custom_summary: Optional[str] = None,
        custom_receipt: Optional[str] = None,
        custom_permalink: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cria um produto 100% autônomo na conta Gumroad do usuário via API com HTML Rico e Imagens.
        """
        if not access_token or len(access_token.strip()) < 10:
            return {"success": False, "error": "Token de Acesso do Gumroad não configurado."}

        token = access_token.strip()

        if not description:
            description = cls.get_main_product_html_description()

        if not custom_summary:
            custom_summary = (
                "Instant Automated Activation: All 7 Generative AI Search Assets (/llms.txt, Schema.org Graph, "
                "Editorial Authority Article & IndexNow Pings) + 7-Day Money-Back Guarantee."
            )

        if not custom_receipt:
            custom_receipt = (
                "Thank you for your purchase! Your 14-Day AI Search Visibility Sprint is now active. "
                "Access your live dashboard and entity assets at: https://geopulseai.store"
            )

        payload: Dict[str, Any] = {
            "name": name,
            "price": str(price_cents),
            "currency": currency.lower(),
            "description": description,
            "custom_summary": custom_summary,
            "custom_receipt": custom_receipt,
        }
        if custom_permalink:
            payload["url"] = custom_permalink

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                res = await client.post(
                    f"{cls.BASE_URL}/products",
                    data=payload,
                    headers=headers,
                )
                if res.status_code in (200, 201):
                    data = res.json()
                    product = data.get("product", {})
                    pid = product.get("id")
                    # Garante via PUT que description HTML, custom_summary e custom_receipt fiquem 100% gravados
                    if pid:
                        try:
                            put_res = await client.put(
                                f"{cls.BASE_URL}/products/{pid}",
                                data={
                                    "description": description,
                                    "custom_summary": custom_summary,
                                    "custom_receipt": custom_receipt,
                                },
                                headers=headers,
                            )
                            if put_res.status_code in (200, 201):
                                product = put_res.json().get("product", product)
                        except Exception as put_e:
                            logger.warning(f"[Gumroad] Aviso PUT complementar: {put_e}")
                    short_url = product.get("short_url") or product.get("url") or f"https://gumroad.com/l/{product.get('permalink')}"
                    logger.info(f"[Gumroad] Produto criado com sucesso: {product.get('name')} -> {short_url}")
                    return {
                        "success": True,
                        "product_id": product.get("id"),
                        "name": product.get("name"),
                        "price": product.get("price"),
                        "currency": product.get("currency"),
                        "short_url": short_url,
                        "raw": product,
                    }
                else:
                    err_msg = f"Erro Gumroad HTTP {res.status_code}: {res.text[:300]}"
                    logger.warning(f"[Gumroad] {err_msg}")
                    return {"success": False, "error": err_msg}
        except Exception as e:
            logger.error(f"[Gumroad] Exceção na criação do produto: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    async def update_product(
        cls,
        access_token: str,
        product_id: str,
        name: Optional[str] = None,
        price_cents: Optional[int] = None,
        description: Optional[str] = None,
        custom_summary: Optional[str] = None,
        custom_receipt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Atualiza um produto existente no Gumroad via PUT /v2/products/{id}."""
        if not access_token or not product_id:
            return {"success": False, "error": "Token ou product_id ausente."}

        payload: Dict[str, Any] = {}
        if name is not None:
            payload["name"] = name
        if price_cents is not None:
            payload["price"] = str(price_cents)
        if description is not None:
            payload["description"] = description
        if custom_summary is not None:
            payload["custom_summary"] = custom_summary
        if custom_receipt is not None:
            payload["custom_receipt"] = custom_receipt

        headers = {
            "Authorization": f"Bearer {access_token.strip()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                res = await client.put(
                    f"{cls.BASE_URL}/products/{product_id}",
                    data=payload,
                    headers=headers,
                )
                if res.status_code in (200, 201):
                    data = res.json()
                    product = data.get("product", {})
                    return {
                        "success": True,
                        "product_id": product.get("id"),
                        "short_url": product.get("short_url"),
                        "raw": product,
                    }
                return {"success": False, "error": f"HTTP {res.status_code}: {res.text[:250]}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    async def delete_product(cls, access_token: str, product_id: str) -> Dict[str, Any]:
        """Remove um produto do Gumroad via DELETE /v2/products/{id}."""
        if not access_token or not product_id:
            return {"success": False, "error": "Token ou product_id ausente."}
        headers = {"Authorization": f"Bearer {access_token.strip()}"}
        try:
            async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
                res = await client.delete(f"{cls.BASE_URL}/products/{product_id}", headers=headers)
                if res.status_code in (200, 204):
                    return {"success": True}
                return {"success": False, "error": f"HTTP {res.status_code}: {res.text[:200]}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    async def upload_product_cover(
        cls,
        access_token: str,
        product_id: str,
        image_url: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
    ) -> Dict[str, Any]:
        """Adiciona a capa oficial do produto no Gumroad (seção 'Cobrir' / Cover image)."""
        if not access_token or not product_id:
            return {"success": False, "error": "Token ou product_id ausente."}
        headers = {
            "Authorization": f"Bearer {access_token.strip()}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        try:
            async with httpx.AsyncClient(timeout=35.0, verify=False) as client:
                # 1. Envio prioritário com URL pública (método oficial suportado pela Gumroad API v2)
                if image_url:
                    res_url = await client.post(
                        f"{cls.BASE_URL}/products/{product_id}/covers",
                        data={"url": image_url},
                        headers=headers,
                    )
                    if res_url.status_code in (200, 201):
                        d = res_url.json()
                        if d.get("success"):
                            logger.info(f"✅ [Gumroad] Capa enviada com sucesso via URL para {product_id}!")
                            return {"success": True, "data": d}

                # 2. Fallback com multipart se houver bytes
                if image_bytes:
                    mp_headers = {"Authorization": f"Bearer {access_token.strip()}"}
                    files = {"file": ("cover.png", image_bytes, "image/png")}
                    res_mp = await client.post(
                        f"{cls.BASE_URL}/products/{product_id}/covers",
                        files=files,
                        headers=mp_headers,
                    )
                    if res_mp.status_code in (200, 201):
                        d_mp = res_mp.json()
                        if d_mp.get("success"):
                            return {"success": True, "data": d_mp}

                return {"success": False, "error": f"Gumroad covers falhou: {res_url.text if image_url else 'Sem URL'}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    async def list_products(cls, access_token: str) -> Dict[str, Any]:
        """Consulta os produtos existentes na conta Gumroad."""
        if not access_token:
            return {"success": False, "error": "Token ausente."}
        headers = {"Authorization": f"Bearer {access_token.strip()}"}
        try:
            async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
                res = await client.get(f"{cls.BASE_URL}/products", headers=headers)
                if res.status_code == 200:
                    return {"success": True, "products": res.json().get("products", [])}
                return {"success": False, "error": res.text[:200]}
        except Exception as e:
            return {"success": False, "error": str(e)}
