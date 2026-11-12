import logging
import httpx
from typing import Dict, Any, Optional, List

logger = logging.getLogger("geopulse.lemonsqueezy")


class LemonSqueezyService:
    BASE_URL = "https://api.lemonsqueezy.com/v1"

    @classmethod
    def _headers(cls, api_key: str) -> Dict[str, str]:
        return {
            "Accept": "application/vnd.api+json",
            "Content-Type": "application/vnd.api+json",
            "Authorization": f"Bearer {api_key.strip()}"
        }

    @classmethod
    async def get_current_user(cls, api_key: str) -> Dict[str, Any]:
        """Valida a chave de API consultando o usuário autenticado."""
        if not api_key:
            return {"success": False, "error": "Chave de API não informada."}
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(f"{cls.BASE_URL}/users/me", headers=cls._headers(api_key))
                if res.status_code == 200:
                    data = res.json().get("data", {})
                    attrs = data.get("attributes", {})
                    return {
                        "success": True,
                        "user_id": data.get("id"),
                        "name": attrs.get("name"),
                        "email": attrs.get("email")
                    }
                return {"success": False, "error": f"Erro Lemon Squeezy HTTP {res.status_code}: {res.text[:200]}"}
        except Exception as e:
            logger.error(f"[LemonSqueezy] Erro ao validar usuário: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    async def list_stores(cls, api_key: str) -> Dict[str, Any]:
        """Lista todas as lojas vinculadas à conta do Lemon Squeezy."""
        if not api_key:
            return {"success": False, "error": "Chave de API não informada."}
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(f"{cls.BASE_URL}/stores", headers=cls._headers(api_key))
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    stores = []
                    for item in data:
                        attrs = item.get("attributes", {})
                        stores.append({
                            "id": str(item.get("id")),
                            "name": attrs.get("name"),
                            "slug": attrs.get("slug"),
                            "currency": attrs.get("currency"),
                            "url": attrs.get("url")
                        })
                    return {"success": True, "stores": stores}
                return {"success": False, "error": f"Erro ao listar lojas ({res.status_code}): {res.text[:200]}"}
        except Exception as e:
            logger.error(f"[LemonSqueezy] Erro ao listar lojas: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    async def list_products(cls, api_key: str, store_id: Optional[str] = None) -> Dict[str, Any]:
        """Lista os produtos cadastrados na loja Lemon Squeezy."""
        if not api_key:
            return {"success": False, "error": "Chave de API não informada."}
        try:
            params = {}
            if store_id:
                params["filter[store_id]"] = str(store_id)
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(f"{cls.BASE_URL}/products", headers=cls._headers(api_key), params=params)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    products = []
                    for item in data:
                        attrs = item.get("attributes", {})
                        products.append({
                            "id": str(item.get("id")),
                            "store_id": str(attrs.get("store_id")),
                            "name": attrs.get("name"),
                            "slug": attrs.get("slug"),
                            "status": attrs.get("status"),
                            "price_formatted": attrs.get("price_formatted"),
                            "buy_now_url": attrs.get("buy_now_url"),
                            "thumb_url": attrs.get("thumb_url")
                        })
                    return {"success": True, "products": products}
                return {"success": False, "error": f"Erro HTTP {res.status_code}: {res.text[:200]}"}
        except Exception as e:
            logger.error(f"[LemonSqueezy] Erro ao listar produtos: {e}")
            return {"success": False, "error": str(e)}

    @classmethod
    async def create_checkout(
        cls,
        api_key: str,
        store_id: str,
        variant_id: str,
        custom_price_usd: Optional[float] = None,
        product_name: Optional[str] = None,
        custom_description: Optional[str] = None,
        redirect_url: Optional[str] = None,
        customer_email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cria uma sessão de checkout customizada no Lemon Squeezy para vender o produto principal ou e-books.
        """
        if not api_key or not store_id or not variant_id:
            return {"success": False, "error": "Parâmetros obrigatórios ausentes (api_key, store_id ou variant_id)."}

        payload: Dict[str, Any] = {
            "data": {
                "type": "checkouts",
                "attributes": {
                    "checkout_data": {}
                },
                "relationships": {
                    "store": {
                        "data": {"type": "stores", "id": str(store_id)}
                    },
                    "variant": {
                        "data": {"type": "variants", "id": str(variant_id)}
                    }
                }
            }
        }

        attrs = payload["data"]["attributes"]
        if custom_price_usd is not None:
            attrs["custom_price"] = int(custom_price_usd * 100)  # Lemon Squeezy usa centavos em USD
        if product_name:
            attrs["product_options"] = attrs.get("product_options", {})
            attrs["product_options"]["name"] = product_name
        if custom_description:
            attrs["product_options"] = attrs.get("product_options", {})
            attrs["product_options"]["description"] = custom_description
        if redirect_url:
            attrs["product_options"] = attrs.get("product_options", {})
            attrs["product_options"]["redirect_url"] = redirect_url
        if customer_email:
            attrs["checkout_data"]["email"] = customer_email

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                res = await client.post(f"{cls.BASE_URL}/checkouts", headers=cls._headers(api_key), json=payload)
                if res.status_code in (200, 201):
                    data = res.json().get("data", {})
                    checkout_url = data.get("attributes", {}).get("url")
                    return {
                        "success": True,
                        "checkout_id": data.get("id"),
                        "checkout_url": checkout_url
                    }
                return {"success": False, "error": f"Erro checkout ({res.status_code}): {res.text[:300]}"}
        except Exception as e:
            logger.error(f"[LemonSqueezy] Erro ao criar checkout: {e}")
            return {"success": False, "error": str(e)}
