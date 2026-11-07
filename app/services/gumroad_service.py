"""
Módulo de Integração com a API Oficial do Gumroad (v2).
Permite a criação 100% autônoma de produtos e links de checkout globais
e processamento de webhooks de vendas (Pings).
"""
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger("geopulse.gumroad")


class GumroadService:
    BASE_URL = "https://api.gumroad.com/v2"

    @classmethod
    async def create_product(
        cls,
        access_token: str,
        name: str = "GeoPulse AI — Desafio 14 Dias Rumo ao Top 10 nas IAs",
        price_cents: int = 4700,
        currency: str = "usd",
        description: Optional[str] = None,
        custom_permalink: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cria um produto 100% autônomo na conta Gumroad do usuário via API.
        Retorna os dados do produto criado e o link oficial de checkout (short_url).
        """
        if not access_token or len(access_token.strip()) < 10:
            return {"success": False, "error": "Token de Acesso do Gumroad não configurado."}

        token = access_token.strip()

        if not description:
            description = (
                "## GeoPulse AI — Posicionamento de Entidade no ChatGPT, Gemini e Perplexity\n\n"
                "Garanta a presença da sua empresa ou consultório no **Top 10 de recomendações de Inteligência Artificial**.\n\n"
                "### O que está incluso no Desafio de 14 Dias:\n"
                "- Geração e Hospedagem de arquivo `/llms.txt` oficial da sua marca.\n"
                "- Grafo Semântico Schema.org JSON-LD verificado.\n"
                "- Publicação de Artigo Editorial de Autoridade Local.\n"
                "- Pings prioritários via protocolo IndexNow (Bing / ChatGPT Search).\n"
                "- Acompanhamento de nota de visibilidade (0 a 100).\n"
                "- **Garantia Blindada de 7 Dias:** risco zero.\n\n"
                "*(Não precisa alterar o código do seu site atual nem contratar programadores)*."
            )

        payload = {
            "name": name,
            "price": str(price_cents),
            "currency": currency.lower(),
            "description": description,
        }
        if custom_permalink:
            payload["url"] = custom_permalink

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
                res = await client.post(
                    f"{cls.BASE_URL}/products",
                    data=payload,
                    headers=headers,
                )
                if res.status_code in (200, 201):
                    data = res.json()
                    product = data.get("product", {})
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
    async def list_products(cls, access_token: str) -> Dict[str, Any]:
        """Consulta os produtos existentes na conta Gumroad."""
        if not access_token:
            return {"success": False, "error": "Token ausente."}
        headers = {"Authorization": f"Bearer {access_token.strip()}"}
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                res = await client.get(f"{cls.BASE_URL}/products", headers=headers)
                if res.status_code == 200:
                    return {"success": True, "products": res.json().get("products", [])}
                return {"success": False, "error": res.text[:200]}
        except Exception as e:
            return {"success": False, "error": str(e)}
