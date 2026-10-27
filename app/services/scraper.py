import re
import asyncio
import httpx
from typing import Dict, Any, Optional


class JinaScraperService:
    """
    Serviço de extração de conteúdo web usando o Jina Reader (r.jina.ai).
    Converte qualquer URL em Markdown limpo estruturado sem requerer API key paga.
    Otimizado com execução 100% paralela (asyncio.gather) e timeouts rápidos.
    """

    @staticmethod
    def normalize_url(url: str) -> str:
        url = url.strip()
        if url.startswith("@"):
            return f"https://www.instagram.com/{url[1:].strip('/')}"
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        return url

    @classmethod
    async def _fetch_jina_markdown(cls, normalized: str) -> Dict[str, Any]:
        jina_url = f"https://r.jina.ai/{normalized}"
        headers = {
            "User-Agent": "GeoPulseAI/1.0 (Audit Bot; Contact: info@geopulse.ai)",
            "Accept": "text/markdown",
            "X-With-Generated-Alt": "true"
        }
        try:
            async with httpx.AsyncClient(timeout=4.5, follow_redirects=True, verify=False) as client:
                response = await client.get(jina_url, headers=headers)
                if response.status_code == 200:
                    markdown_content = response.text
                    title_match = re.search(r"^#\s+(.+)$", markdown_content, re.MULTILINE)
                    if not title_match:
                        title_match = re.search(r"Title:\s*(.+)", markdown_content)
                    title = title_match.group(1).strip() if title_match else normalized
                    clean_content = markdown_content[:12000] if len(markdown_content) > 12000 else markdown_content
                    return {"success": True, "title": title, "content": clean_content, "error": None}
                return {"success": False, "title": normalized, "content": "", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "title": normalized, "content": "", "error": str(e)}

    @classmethod
    async def _fetch_raw_html(cls, normalized_url: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=3.5, follow_redirects=True, verify=False) as client:
                res = await client.get(normalized_url, headers={"User-Agent": "Mozilla/5.0 (compatible; GeoPulseAudit/2.0)"})
                if res.status_code < 400:
                    return res.text
        except Exception:
            pass
        return ""

    @classmethod
    async def _check_llms_txt(cls, base_domain: str) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.5, follow_redirects=True, verify=False) as client:
                res = await client.get(f"{base_domain}/llms.txt")
                if res.status_code == 200 and len(res.text) > 40 and "<html" not in res.text.lower()[:200]:
                    return True
        except Exception:
            pass
        return False

    @classmethod
    async def scrape_url(cls, target_url: str) -> Dict[str, Any]:
        normalized = cls.normalize_url(target_url)
        base_domain = re.sub(r"(https?://[^/]+).*", r"\1", normalized)

        # Executa as 3 inspeções de rede simultaneamente (leva no máximo 4.5s no total!)
        jina_res, html_text, has_llms_txt = await asyncio.gather(
            cls._fetch_jina_markdown(normalized),
            cls._fetch_raw_html(normalized),
            cls._check_llms_txt(base_domain)
        )

        markdown_content = jina_res.get("content", "")
        site_reachable = bool(html_text) or jina_res.get("success", False)
        raw_html_len = len(html_text)
        lower_html = html_text.lower() if html_text else ""

        has_json_ld = "application/ld+json" in lower_html or "schema.org" in lower_html
        has_faq_structure = any(k in lower_html for k in ["faq", "perguntas frequentes", "duvidas", "frequently asked", "preguntas frecuentes", "questions"])
        social_links_count = sum(
            1 for soc in ["linkedin.com", "instagram.com", "facebook.com", "youtube.com", "wa.me", "whatsapp.com"]
            if soc in lower_html
        )

        md_len = len(markdown_content) if markdown_content else 0
        headings_count = len(re.findall(r"^#{1,3}\s+", markdown_content or "", re.MULTILINE))

        signals = {
            "site_reachable": site_reachable,
            "has_json_ld": has_json_ld,
            "has_llms_txt": has_llms_txt,
            "has_faq_structure": has_faq_structure,
            "social_links_count": social_links_count,
            "markdown_length": md_len,
            "raw_html_length": raw_html_len,
            "headings_count": headings_count
        }

        return {
            "success": jina_res.get("success", False),
            "title": jina_res.get("title", normalized),
            "content": markdown_content or f"Perfil auditado a partir dos dados cadastrados ({normalized}).",
            "url": normalized,
            "signals": signals,
            "error": jina_res.get("error")
        }

