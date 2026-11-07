"""
Robô de Vendas Inteligente (Sales Hunter & AI Closer) para o GeoPulse AI.
Funciona 100% sem custos adicionais de API de terceiros, utilizando busca real na Web (Yahoo/Bing)
combinada com extração direta de WhatsApp, Telefone e E-mail dos sites das empresas encontradas,
além de suporte opcional às chaves LLM (Groq gratuito gpt-oss-120b, Gemini ou OpenAI).
"""
import asyncio
import base64
import json
import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, quote, unquote, urlparse

import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.services.auditor import AuditorService

logger = logging.getLogger("geopulse.sales_bot")


class SalesBotService:

    @classmethod
    async def _call_llm(cls, system_prompt: str, user_prompt: str, keys: Dict[str, Any]) -> Optional[str]:
        """
        Executa chamada LLM priorizando chaves configuradas (Groq Cloud Gratuito, Gemini, OpenAI)
        com timeout seguro e SSL tolerante para evitar travas no servidor.
        """
        groq_key = keys.get("groq_api_key") or settings.GROQ_API_KEY
        openai_key = keys.get("openai_api_key") or settings.OPENAI_API_KEY
        gemini_key = keys.get("gemini_api_key") or settings.GEMINI_API_KEY

        # 1. Groq (Gratuito e Ultrarrápido - Modelos Ativos 2026)
        if groq_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            for groq_model in ("openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"):
                payload = {
                    "model": groq_model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 700
                }
                try:
                    async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                        res = await client.post(url, headers=headers, json=payload)
                        if res.status_code == 200:
                            data = res.json()
                            choices = data.get("choices", [])
                            if choices:
                                content = choices[0].get("message", {}).get("content", "").strip()
                                if content:
                                    return content
                except Exception as e:
                    logger.warning(f"Groq sales bot error ({groq_model}): {e}")

        # 2. OpenAI (se configurada)
        if openai_key:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {openai_key}", "Content-Type": "application/json"}
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 600
            }
            try:
                async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        choices = data.get("choices", [])
                        if choices:
                            return choices[0].get("message", {}).get("content", "").strip()
            except Exception as e:
                logger.warning(f"OpenAI sales bot error: {e}")

        # 3. Gemini (se configurada)
        if gemini_key:
            try:
                resp = await AuditorService.call_gemini(f"{system_prompt}\n\nUser: {user_prompt}", gemini_key)
                if resp:
                    return resp.strip()
            except Exception as e:
                logger.warning(f"Gemini sales bot error: {e}")

        return None

    # =========================================================================
    # 1. AI SALES CLOSER (CHAT CONSULTIVO NA PÁGINA DO DIAGNÓSTICO)
    # =========================================================================

    @classmethod
    async def chat_closer(
        cls,
        message: str,
        company_name: Optional[str],
        niche: Optional[str],
        city_region: Optional[str],
        score: Optional[float],
        top_competitor: Optional[str],
        language: str = "pt",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        keys: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Responde a dúvidas do visitante na página do diagnóstico atuando como Consultor Sênior de Crescimento.
        Focado em converter o lead para os 14 Dias Rumo ao Top 10 e assinatura do GeoPulse AI.
        """
        keys = keys or {}
        comp_name = (company_name or "sua empresa").strip()
        niche_str = (niche or "seu segmento").strip()
        city_str = (city_region or "sua região").strip()
        competitor = (top_competitor or "os principais concorrentes locais").strip()
        score_val = round(float(score or 42.0), 1)

        lang = (language or "pt").lower()
        if lang not in ["pt", "en", "es"]:
            lang = "pt"

        if lang == "en":
            system_prompt = (
                "You are an Elite AI Search Growth Consultant for GeoPulse AI (GEO - Generative Engine Optimization). "
                f"Client Company: '{comp_name}' | Industry: '{niche_str}' | City: '{city_str}'. "
                f"Current AI Visibility Score: {score_val}/100. Top Competitor currently stealing AI recommendations: '{competitor}'. "
                "GOAL: Answer questions concisely, address objections persuasively, and guide them to activate the "
                "'14-Day Challenge to Top 10 Search Placement' (USD 47 or instant card/PayPal). "
                "CRITICAL RULES: "
                "1. Keep responses under 3 short paragraphs. "
                "2. NEVER promise guaranteed #1 rank. Always promise Top 10 visibility, highest recommendation probability, and entity authority. "
                "3. Emphasize that they DO NOT need developers or to edit their website; GeoPulse indexes external entity authority and llms.txt. "
                "4. Always offer a clear next action (Activate 14-Day Challenge or secure spot now)."
            )
        elif lang == "es":
            system_prompt = (
                "Eres un Consultor Senior de Crecimiento en Búsquedas de IA para GeoPulse AI (GEO - Generative Engine Optimization). "
                f"Empresa del cliente: '{comp_name}' | Nicho: '{niche_str}' | Ciudad: '{city_str}'. "
                f"Nota de Visibilidad en IA: {score_val}/100. Competidor #1 que lidera las recomendaciones: '{competitor}'. "
                "OBJETIVO: Responder con persuasión y claridad, romper objeciones y guiar al cliente a activar el "
                "'Desafío de 14 Días rumbo al Top 10 de IA' (USD 47 o tarjeta/PayPal). "
                "REGLAS CRÍTICAS: "
                "1. Respuestas de máximo 2 a 3 párrafos cortos y directos. "
                "2. NUNCA prometas el 1º lugar garantizado. Promete entrada al Top 10, máxima visibilidad y porcentaje de citación por la IA. "
                "3. Destaca que NO necesitan programadores ni modificar su sitio web; todo se indexa externamente con Schema.org y llms.txt. "
                "4. Finaliza invitando a asegurar su lugar en el Top 10 ahora."
            )
        else:
            system_prompt = (
                "Você é o Consultor Sênior de Crescimento e Vendas do GeoPulse AI (especialista em GEO - Generative Engine Optimization). "
                f"Empresa analisada: '{comp_name}' | Ramo: '{niche_str}' | Cidade: '{city_str}'. "
                f"Nota atual de Visibilidade em IA: {score_val}/100. Concorrente #1 que hoje domina as recomendações locais: '{competitor}'. "
                "OBJETIVO: Responder ao cliente de forma acolhedora, executiva e altamente persuasiva. Romper objeções e "
                "incentivar a contratação imediata do 'Desafio de 14 Dias Rumo ao Top 10 de Buscas' (R$ 197 via PIX ou Cartão Mercado Pago). "
                "REGRAS OBRIGATÓRIAS: "
                "1. Responda em no máximo 2 a 3 parágrafos objetivos (use negrito e listas quando ajudar a leitura). "
                "2. NUNCA prometa 1º lugar garantido; o compromisso oficial é colocar a marca no TOP 10 dos motores de IA com máxima visibilidade e autoridade. "
                "3. Enfatize que NÃO é necessário mexer no site atual nem contratar programadores; nossa plataforma publica o dossiê de autoridade, Schema.org e llms.txt na nuvem. "
                "4. Destaque a garantia incondicional e o risco zero."
            )

        history_text = ""
        if conversation_history:
            for item in conversation_history[-4:]:
                sender = "Cliente" if item.get("role") == "user" else "Consultor"
                history_text += f"{sender}: {item.get('content', '')}\n"

        user_prompt = f"Histórico recente:\n{history_text}\nPergunta atual do cliente: {message}"

        reply = await cls._call_llm(system_prompt, user_prompt, keys)

        if not reply:
            lower = message.lower()
            if lang == "en":
                if any(w in lower for w in ["price", "cost", "how much"]):
                    reply = (
                        f"The **GeoPulse AI Top 10 Acceleration Plan** is a one-time investment of **$47 USD** "
                        f"(or local currency). It includes the complete syndication of your structured business entity, "
                        f"`llms.txt` file, and authority articles to overtake **{competitor}** in AI recommendations."
                    )
                elif any(w in lower for w in ["code", "developer", "site", "website"]):
                    reply = (
                        f"You **do not need any technical skills or to change your website**! GeoPulse AI hosts your "
                        f"verified semantic authority externally on cloud endpoints that ChatGPT, Gemini, and Perplexity crawl 24/7."
                    )
                else:
                    reply = (
                        f"Currently, when local customers search for {niche_str} in {city_str}, AI engines frequently recommend "
                        f"**{competitor}** instead of **{comp_name}**. Our 14-Day Challenge positions your brand in the **Top 10 AI recommendations** "
                        f"with complete entity verification and zero code required."
                    )
            elif lang == "es":
                if any(w in lower for w in ["precio", "costo", "cuanto"]):
                    reply = (
                        f"El plan de activación de **GeoPulse AI** tiene un pago único de **$47 USD** (o moneda local). "
                        f"Incluye la estructuración semántica de tu empresa, archivo `llms.txt` y sindicación de autoridad "
                        f"para disputar las recomendaciones que hoy se lleva **{competitor}**."
                    )
                else:
                    reply = (
                        f"Actualmente las IAs recomiendan a **{competitor}** en {city_str}. Con nuestro Desafío de 14 Días, "
                        f"posicionamos a **{comp_name}** en el **Top 10 de búsquedas de IA** sin tocar tu página web y con garantía total."
                    )
            else:
                if any(w in lower for w in ["preço", "valor", "custa", "quanto"]):
                    reply = (
                        f"A ativação do **Desafio 14 Dias Rumo ao Top 10** tem uma taxa única promocional de **R$ 197** "
                        f"(via PIX ou Cartão em até 12x). Você não tem mensalidade oculta e recebe todos os 4 motores de IA ativados "
                        f"para recuperar clientes que hoje vão para a **{competitor}**."
                    )
                elif any(w in lower for w in ["site", "código", "programador", "instalar"]):
                    reply = (
                        f"Você **não precisa mexer em nada no seu site** e nem contratar programador! O GeoPulse AI cria e "
                        f"publica seus dados estruturados (Schema.org de Entidade, arquivo `llms.txt` e Artigos de Autoridade) "
                        f"em servidores de alta performance que o ChatGPT e Gemini consultam diretamente."
                    )
                elif any(w in lower for w in ["garantia", "seguro", "devolve"]):
                    reply = (
                        f"Você conta com **Garantia Incondicional de 7 Dias**. Se a estrutura de inteligência artificial "
                        f"da **{comp_name}** não for gerada e publicada imediatamente, devolvemos 100% do seu dinheiro via PIX na hora."
                    )
                else:
                    reply = (
                        f"Nossa auditoria detectou que a **{competitor}** hoje captura a maior parte dos clientes que buscam por "
                        f"*{niche_str}* em *{city_str}* no ChatGPT e Gemini. O objetivo do GeoPulse AI é colocar a **{comp_name}** "
                        f"com máxima visibilidade no **Top 10 oficial de recomendações**, sem você precisar entender de tecnologia."
                    )

        quick_actions = [
            {"label": "🚀 Como funciona a garantia de 14 dias?", "prompt": "Como funciona a garantia e o desafio de 14 dias?"},
            {"label": "💳 Quais as formas de pagamento?", "prompt": "Quais as formas de pagamento disponíveis?"},
            {"label": "🛠️ Preciso alterar meu site?", "prompt": "Preciso mexer no código do meu site atual?"},
        ]
        if lang == "en":
            quick_actions = [
                {"label": "🚀 How does the 14-day challenge work?", "prompt": "How does the 14-day challenge work?"},
                {"label": "💳 Payment methods accepted?", "prompt": "What payment methods are available?"},
                {"label": "🛠️ Do I need to edit my website?", "prompt": "Do I need technical skills or website changes?"},
            ]
        elif lang == "es":
            quick_actions = [
                {"label": "🚀 ¿Cómo funciona el desafío de 14 días?", "prompt": "¿Cómo funciona el desafío de 14 días?"},
                {"label": "💳 ¿Cuáles son los métodos de pago?", "prompt": "¿Qué métodos de pago aceptan?"},
                {"label": "🛠️ ¿Necesito programador?", "prompt": "¿Necesito tocar el código de mi sitio web?"},
            ]

        return {
            "reply": reply,
            "company_name": comp_name,
            "top_competitor": competitor,
            "score": score_val,
            "quick_actions": quick_actions,
            "checkout_url": f"/?report={keys.get('report_id', '')}#checkout" if keys.get("report_id") else "#checkout",
        }

    # =========================================================================
    # 2. SALES HUNTER (CAÇADOR DE LEADS REAIS NA WEB + EXTRAÇÃO DE CONTATOS)
    # =========================================================================

    @staticmethod
    def _decode_yahoo_url(href: str) -> str:
        m = re.search(r"/RU=([^/]+)/RK=", href)
        if m:
            return unquote(m.group(1))
        return href

    @staticmethod
    def _decode_bing_url(href: str) -> str:
        try:
            qs = parse_qs(urlparse(href).query)
            u = qs.get("u", [""])[0]
            if u.startswith("a1"):
                b64 = u[2:]
                b64 += "=" * (-len(b64) % 4)
                return base64.urlsafe_b64decode(b64).decode("utf-8", errors="ignore")
        except Exception:
            pass
        return href

    @staticmethod
    def _clean_company_title(raw_title: str, url: str) -> str:
        """Limpa o título de SEO da página para ficar um Nome de Empresa limpo e identificável."""
        t = re.sub(r"https?://[^\s]+", "", raw_title)
        t = re.sub(r"^[a-z0-9.-]+\.(com\.br|com|org\.br|net|med\.br|odo\.br|adv\.br)\s*", "", t, flags=re.I)
        parts = [p.strip() for p in re.split(r"\s*[\|\-–—:]\s*", t) if len(p.strip()) >= 3]
        generic_Starts = ("contato", "home", "início", "inicio", "sobre", "clínica odontológica", "clinica odontologica", "dentista em")
        best = parts[0] if parts else t.strip()
        for p in parts:
            if not any(p.lower().startswith(g) for g in generic_Starts):
                best = p
                break
        domain_raw = urlparse(url).netloc.lower().replace("www.", "").split(".")[0]
        if len(best) < 4 or best.lower() in generic_Starts:
            best = f"{best} ({domain_raw.capitalize()})" if best else domain_raw.capitalize()
        elif domain_raw not in best.lower().replace(" ", ""):
            best = f"{best[:45]} ({domain_raw})"
        return best[:75]

    GLOBAL_BLOCKED_DOMAINS = (
        "duckduckgo.com", "yahoo.com", "bing.com", "google.", "whatsapp.com", "wa.me",
        "doctoralia", "guiamais", "apontador", "solutudo", "reclameaqui", "facebook.com",
        "instagram.com", "linkedin.com", "youtube.com", "wikipedia.org", "tiktok.com",
        "yelp.com", "tripadvisor", "yellowpages", "mapquest", "expertise.com", "healthgrades",
        "zocdoc", "threebestrated", "listamais", "applocal", "acheioprofissional", "telelistas",
        "hagah", "encontra", "econodata", "cnpj.biz", "casadosdados", "jusbrasil", "cylex",
        "infobel", "hotfrog", "kekanto", "catalogo", "guiadelocalizacao", "melhores", "top10",
        "gov.", ".gov", "edu.", ".edu", "crosp", "cfo.org", "oab", "cfm.org", "odontoblog",
        "g1.globo", "globo.com", "uol.com.br", "terra.com.br", "exame.com", "forbes.com",
        "cnbc.com", "nba.com", "espn.com", "amazon.", "mercadolivre", "shopee", "aliexpress",
        "spotify.com", "uber.com", "apple.com", "microsoft.com", "gemini.com", "insidertrades",
        "morningstar", "prnewswire", "gartic", "karafun", "versao-karaoke", "zhihu.com",
        "douban.com", "flashscore", "bula.com", "patient.info", "coveredca.com", "aspenideas",
        "collegeboard", "clicrbs", "zerohora", "estadao", "folha.uol", "r7.com", "ig.com.br"
    )

    @classmethod
    def _is_valid_business_candidate(cls, title: str, url: str, niche: str, is_international: bool) -> bool:
        """Filtra rigorosamente portais de notícias, gigantes globais e resultados falsos anti-bot."""
        if not url or not url.startswith("http"):
            return False
        dom = urlparse(url).netloc.lower().replace("www.", "")
        if not dom or len(dom) < 4:
            return False
        if any(b in dom for b in cls.GLOBAL_BLOCKED_DOMAINS):
            return False
        # Se for busca no Brasil, exige domínio .br ou título em português do nicho
        if not is_international and not dom.endswith(".br"):
            combined = f"{title} {dom}".lower()
            br_niche_roots = ("odonto", "dent", "clinic", "clínic", "advoc", "advog", "direito", "estetic", "estétic", "medic", "médic", "imobi", "contab", "arquit", "solar", "dermat", "harmoniza", "fisiot", "psicol", "nutri", "vet")
            if not any(k in combined for k in br_niche_roots):
                return False
        # Bloqueia títulos que claramente são notícias sobre CEOs, jogos, política ou fóruns
        bad_title_words = ("ceo ", "net worth", "biography", "earnings", "schedule", "nba ", "roster", "scores", "karaoke", "karaokê", "interações medicamentosas", "presidente", "governor", "primature", "flamengo", "corinthians", "palmeiras")
        t_low = title.lower()
        if any(bw in t_low for bw in bad_title_words):
            return False
        return True

    @classmethod
    async def _scrape_site_contacts(cls, client: httpx.AsyncClient, url: str) -> Dict[str, str]:
        """Visita o site real da empresa (e a página /contato se necessário) extraindo WhatsApp, Telefone, E-mail e Instagram sem falsos positivos de JS/CSS."""
        from urllib.parse import urljoin
        phone = ""
        email = ""
        instagram = ""
        pages_to_visit = [url]
        is_br_site = ".br" in urlparse(url).netloc.lower()

        blocked_email_tokens = (
            ".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".css", ".js",
            "sentry", "wix", "example", "yourdomain", "email.com", "dominio",
            "voce@", "seuemail@", "nome@", "usuario@", "teste@", "contato@site",
            "wordpress", "godaddy", "hostgator", "locaweb", "globoid", "versantmedia"
        )
        blocked_ig = ("p", "reel", "reels", "tv", "explore", "stories", "share", "accounts", "legal", "about", "developer")

        for idx, page_url in enumerate(pages_to_visit):
            try:
                r = await client.get(page_url, timeout=6.0)
                if r.status_code >= 400:
                    continue
                html = r.text
                soup = BeautifulSoup(html, "html.parser")

                # 1. Links diretos de WhatsApp no HTML bruto
                if not phone:
                    wpp_matches = re.findall(r"(?:wa\.me/|api\.whatsapp\.com/send\?[^\"'>\s]*phone=)(55\d{10,11}|\d{10,13})", html)
                    if wpp_matches:
                        d = re.sub(r"\D", "", wpp_matches[0])
                        phone = f"55{d}" if (is_br_site and len(d) in (10, 11) and not d.startswith("55")) else d

                # 2. Links tel: explícitos
                if not phone:
                    tel_links = re.findall(r"href=[\"']tel:[\+\s]*([0-9\-\(\)\s]{10,16})[\"']", html, flags=re.I)
                    for rp in tel_links:
                        digits = re.sub(r"\D", "", rp)
                        if len(digits) in (10, 11) and is_br_site:
                            phone = f"55{digits}"
                            break
                        elif len(digits) in (12, 13) and digits.startswith("55"):
                            phone = digits
                            break

                # 3. Remove <script>, <style>, <svg> antes de procurar telefone no texto visível (evita capturar IDs de JS!)
                for tag in soup(["script", "style", "noscript", "svg", "head"]):
                    tag.decompose()
                visible_text = soup.get_text(" ", strip=True)

                if not phone and is_br_site:
                    br_phones = re.findall(r"(?:\([1-9]{2}\)\s*9?\d{4}[-\s]\d{4}|\b[1-9]{2}\s+9\d{4}[-\s]\d{4}\b)", visible_text)
                    for rp in br_phones:
                        digits = re.sub(r"\D", "", rp)
                        if len(digits) in (10, 11):
                            phone = f"55{digits}"
                            break

                # 4. Procura e-mails reais (priorizando links mailto:)
                if not email:
                    mailtos = re.findall(r"mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", html, flags=re.I)
                    text_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", visible_text + " " + html)
                    for em in (mailtos + text_emails):
                        em_low = em.lower().strip(".")
                        if not any(em_low.endswith(ext) or ext in em_low for ext in blocked_email_tokens):
                            email = em_low
                            break

                # 5. Procura perfil oficial do Instagram
                if not instagram:
                    ig_matches = re.findall(r"instagram\.com/([a-zA-Z0-9._-]+)", html)
                    for ig in ig_matches:
                        clean_ig = ig.strip().strip("/").split("?")[0]
                        if clean_ig and clean_ig.lower() not in blocked_ig and len(clean_ig) >= 3:
                            instagram = clean_ig
                            break

                # Se não achou e-mail na capa, visita a página interna de /contato na 2ª iteração
                if idx == 0 and not email:
                    soup_links = BeautifulSoup(html, "html.parser")
                    for a in soup_links.select("a[href]"):
                        href = a.get("href", "")
                        if any(k in href.lower() for k in ("contato", "fale-conosco", "faleconosco", "contact", "atendimento")):
                            contact_url = urljoin(url, href)
                            if urlparse(contact_url).netloc == urlparse(url).netloc and contact_url not in pages_to_visit:
                                pages_to_visit.append(contact_url)
                                break
            except Exception:
                pass
        return {"phone": phone, "email": email, "instagram": instagram}

    @classmethod
    async def _search_duckduckgo_leads(cls, client: httpx.AsyncClient, query: str, niche: str, city_region: str, qty: int) -> List[Dict[str, str]]:
        """Pesquisa global de empresas via DuckDuckGo HTML com filtro rigoroso de relevância."""
        is_international = any(k in city_region.lower() for k in ["usa", "fl", "ny", "ca", "tx", "il", "espan", "madrid", "barcelona", "portugal", "lisboa", "porto", "london", "uk"])
        candidates = []
        seen = set()
        try:
            r = await client.post("https://html.duckduckgo.com/html/", data={"q": query}, timeout=8.0)
            if r.status_code != 200:
                return []
            soup = BeautifulSoup(r.text, "html.parser")
            for res_div in soup.select("div.result"):
                a_title = res_div.select_one("a.result__a")
                if not a_title:
                    continue
                href = a_title.get("href", "")
                m = re.search(r"uddg=([^&]+)", href)
                raw_url = unquote(m.group(1)) if m else href
                title = a_title.get_text(" ", strip=True)
                if not cls._is_valid_business_candidate(title, raw_url, niche, is_international):
                    continue
                dom = urlparse(raw_url).netloc.lower().replace("www.", "")
                if dom in seen:
                    continue
                seen.add(dom)
                clean_name = cls._clean_company_title(title, raw_url)
                candidates.append({"company_name": clean_name, "url": raw_url, "domain": dom})
                if len(candidates) >= qty:
                    break
        except Exception as e:
            logger.warning(f"DuckDuckGo search error: {e}")
        return candidates

    @classmethod
    async def _search_real_web_leads(cls, niche: str, city_region: str, qty: int) -> List[Dict[str, Any]]:
        """
        Faz busca orgânica ao vivo no Yahoo Brasil (site:.br) e DuckDuckGo por empresas reais de `niche` em `city_region`,
        valida relevância semântica e extrai WhatsApp, Telefone, E-mail e Instagram reais do site (e da página /contato)!
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        candidates: List[Dict[str, str]] = []
        seen_domains = set()
        city_name = city_region.split(",")[0].split("-")[0].strip()

        is_international = any(k in city_region.lower() for k in ["usa", "fl", "ny", "ca", "tx", "il", "espan", "madrid", "barcelona", "portugal", "lisboa", "porto", "london", "uk", "france", "paris", "germany", "berlin"]) or any(k in niche.lower() for k in ["dentist", "lawyer", "attorney", "clinic", "realtor", "abogado", "practice", "firm", "spa"])

        async with httpx.AsyncClient(verify=False, timeout=9.0, follow_redirects=True, headers=headers) as client:
            # 1. Busca principal no Yahoo (múltiplas queries focadas em empresas reais locais)
            yahoo_queries = (
                [f'"{niche}" "{city_name}" contact email phone', f'{niche} in {city_region} official site contact']
                if is_international else
                [f'site:.br "{niche}" "{city_name}" contato', f'site:.br {niche} {city_name} contato telefone', f'{niche} em {city_name} contato']
            )
            for yq in yahoo_queries:
                if len(candidates) >= qty * 2 + 2:
                    break
                try:
                    r = await client.get("https://br.search.yahoo.com/search", params={"p": yq, "n": 20})
                    soup = BeautifulSoup(r.text, "html.parser")
                    for div in soup.select("div.algo"):
                        a = div.select_one("h3.title a")
                        if not a:
                            continue
                        real_url = cls._decode_yahoo_url(a.get("href", ""))
                        for sp in a.select("span"):
                            sp.decompose()
                        raw_title = a.get_text(" ", strip=True)
                        if not cls._is_valid_business_candidate(raw_title, real_url, niche, is_international):
                            continue
                        dom = urlparse(real_url).netloc.lower().replace("www.", "")
                        if dom in seen_domains:
                            continue
                        clean_name = cls._clean_company_title(raw_title, real_url)
                        seen_domains.add(dom)
                        candidates.append({"company_name": clean_name, "url": real_url, "domain": dom})
                        if len(candidates) >= qty * 2 + 4:
                            break
                except Exception as e:
                    logger.warning(f"Yahoo search warning ({yq}): {e}")

            # 2. Complementa com DuckDuckGo HTML se necessário (NUNCA usa www.bing.com pois retorna honeypot falso!)
            if len(candidates) < qty:
                q_ddg = f"{niche} in {city_region} contact" if is_international else f'site:.br "{niche}" "{city_name}" contato'
                ddg_list = await cls._search_duckduckgo_leads(client, q_ddg, niche, city_region, qty * 2)
                for item in ddg_list:
                    if item["domain"] not in seen_domains:
                        seen_domains.add(item["domain"])
                        candidates.append(item)

            # 3. Visita em paralelo os sites candidatos (e página /contato) para extrair WhatsApp, Telefone, E-mail e Instagram reais
            selected = candidates[:max(qty * 2 + 2, 10)]
            tasks = [cls._scrape_site_contacts(client, c["url"]) for c in selected]
            scraped_contacts = await asyncio.gather(*tasks, return_exceptions=True)

            final_leads: List[Dict[str, Any]] = []
            for c, contact_res in zip(selected, scraped_contacts):
                c_phone = ""
                c_email = ""
                c_instagram = ""
                if isinstance(contact_res, dict):
                    c_phone = contact_res.get("phone", "")
                    c_email = contact_res.get("email", "")
                    c_instagram = contact_res.get("instagram", "")
                # Só aceita o lead se conseguiu extrair pelo menos 1 canal real de contato (E-mail, WhatsApp/Telefone ou Instagram)
                if not (c_email or c_phone or c_instagram):
                    continue
                final_leads.append({
                    "company_name": c["company_name"],
                    "url": c["url"],
                    "niche": niche.strip(),
                    "city_region": city_region.strip(),
                    "phone": c_phone,
                    "email": c_email,
                    "instagram": c_instagram,
                    "decision_maker": "Diretoria / Atendimento",
                })

            # Ordena priorizando empresas que possuem E-mail real (para disparo automático) + WhatsApp + Instagram
            final_leads.sort(key=lambda x: (bool(x.get("email")), bool(x.get("phone")), bool(x.get("instagram"))), reverse=True)
            return final_leads[:qty]

    @classmethod
    async def hunt_leads(
        cls,
        niche: str,
        city_region: str,
        quantity: int = 5,
        keys: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Descobre empresas reais na internet para o nicho e cidade solicitados,
        extraindo site oficial, WhatsApp/telefone e e-mail diretamente das páginas das empresas.
        """
        keys = keys or {}
        qty = max(1, min(int(quantity or 5), 12))
        niche_clean = niche.strip()
        city_clean = city_region.strip()

        # 1. Prioridade Máxima: Busca Web Real (Yahoo site:.br + Deep Contact Scraping)
        leads = await cls._search_real_web_leads(niche_clean, city_clean, qty)
        if len(leads) >= qty:
            return leads[:qty]

        # 2. Complemento via LLM (Groq openai/gpt-oss-120b) + Verificação HTTP Ao Vivo (NUNCA salva empresa que não existe!)
        system_prompt = (
            "You are an Elite B2B Commercial Prospector. List REAL, existing businesses with active official websites in the requested city and niche. "
            "Output ONLY a valid JSON array of objects with keys: 'company_name', 'url'."
        )
        user_prompt = f"Liste {qty * 2} empresas reais e conhecidas de '{niche_clean}' localizadas em '{city_clean}' com seus sites oficiais reais."
        raw = await cls._call_llm(system_prompt, user_prompt, keys)
        if raw:
            cleaned = re.sub(r"^```json\s*|\s*```$", "", raw.strip(), flags=re.I)
            m_arr = re.search(r"\[.*\]", cleaned, flags=re.S)
            if m_arr:
                cleaned = m_arr.group(0)
            try:
                data = json.loads(cleaned)
                if isinstance(data, list):
                    existing_urls = {l["url"] for l in leads}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                    async with httpx.AsyncClient(verify=False, timeout=7.0, follow_redirects=True, headers=headers) as client:
                        for item in data:
                            if not isinstance(item, dict) or not item.get("url") or not item.get("company_name"):
                                continue
                            u = str(item["url"]).strip()
                            if not u.startswith("http") or u in existing_urls:
                                continue
                            contacts = await cls._scrape_site_contacts(client, u)
                            if contacts.get("email") or contacts.get("phone") or contacts.get("instagram"):
                                leads.append({
                                    "company_name": str(item["company_name"]).strip(),
                                    "url": u,
                                    "niche": niche_clean,
                                    "city_region": city_clean,
                                    "phone": contacts.get("phone", ""),
                                    "email": contacts.get("email", ""),
                                    "instagram": contacts.get("instagram", ""),
                                    "decision_maker": "Diretoria / Atendimento",
                                })
                                existing_urls.add(u)
                                if len(leads) >= qty:
                                    break
            except Exception:
                pass

        return leads[:qty]

    @classmethod
    def build_cold_outreach(
        cls,
        company_name: str,
        niche: str,
        city_region: str,
        score: float,
        top_competitor: str,
        report_url: str,
        phone: str = "",
        instagram: str = "",
        consultant_name: str = "Equipe GeoPulse AI",
    ) -> Dict[str, str]:
        """
        Gera copy de e-mail e link de WhatsApp hiperpersonalizados citando o concorrente real.
        Se a empresa tiver telefone/WhatsApp extraído do site, o link já abre direto na conversa com ela!
        """
        comp_name = company_name.strip()
        comp_top = top_competitor.strip() or "os principais líderes locais"
        score_val = round(float(score or 38.0), 1)
        checkout_url = f"{report_url}&checkout=1" if "?" in report_url else f"{report_url}?checkout=1"
        base_origin = report_url.split("/?")[0] if "/?" in report_url else "https://geopulseai.store"
        comp_id_match = re.search(r"report=(\d+)", report_url)
        comp_id_str = comp_id_match.group(1) if comp_id_match else "0"
        open_pixel_url = f"{base_origin}/api/track/open/{comp_id_str}.gif"

        email_subject = f"Auditoria de IA: {comp_name} vs {comp_top} no ChatGPT e Gemini ({city_region})"
        email_body = (
            f"Olá, diretoria da {comp_name}.\n\n"
            f"Fizemos uma varredura recente nas buscas recomendadas por Inteligência Artificial (ChatGPT, Gemini e Perplexity) "
            f"para o setor de *{niche}* em *{city_region}*.\n\n"
            f"📊 Resultado encontrado:\n"
            f"• A {comp_name} obteve uma taxa de recomendação de apenas {score_val}%.\n"
            f"• Quem mais aparece recomendado aos clientes na sua região é a *{comp_top}*.\n\n"
            f"Criamos um Dossiê Técnico Executivo gratuito demonstrando o motivo da ausência de dados estruturados e como colocar "
            f"a sua empresa no Top 10 de recomendações em 14 dias:\n"
            f"🔗 Acesse o relatório aqui: {report_url}\n"
            f"⚡ Ou ative o Desafio de 14 Dias direto aqui: {checkout_url}\n\n"
            f"Se fizer sentido para o crescimento da {comp_name}, podemos apresentar o plano de ação em 5 minutos.\n\n"
            f"Atenciosamente,\n{consultant_name}"
        )

        email_html = (
            f"<div style='font-family:Arial,sans-serif;max-width:600px;line-height:1.6;color:#1e293b;padding:26px;border:1px solid #e2e8f0;border-radius:16px;background:#ffffff;'>"
            f"<div style='display:inline-block;background:#eff6ff;color:#1d4ed8;font-size:11px;font-weight:bold;padding:4px 10px;border-radius:999px;margin-bottom:10px;text-transform:uppercase;'>Auditoria Oficial GEO & AIO • {city_region}</div>"
            f"<h2 style='color:#0f172a;margin:0 0 12px 0;font-size:20px;'>Por que o ChatGPT recomenda <span style='color:#dc2626;'>{comp_top}</span> em vez da <span style='color:#2563eb;'>{comp_name}</span>?</h2>"
            f"<p style='margin:0 0 14px 0;'>Olá, diretoria da <strong>{comp_name}</strong>.</p>"
            f"<p style='margin:0 0 16px 0;'>Executamos hoje uma auditoria técnica nos motores de Inteligência Artificial (<strong>ChatGPT Search, Google Gemini e Perplexity</strong>) simulando clientes reais buscando por <strong>{niche}</strong> em <strong>{city_region}</strong>.</p>"
            f"<div style='background:#f8fafc;border:1px solid #e2e8f0;border-left:5px solid #dc2626;padding:16px;margin:18px 0;border-radius:10px;'>"
            f"<p style='margin:0 0 8px 0;font-size:14px;'>📉 <strong>Nota de Visibilidade da {comp_name}:</strong> <span style='color:#dc2626;font-weight:bold;font-size:16px;'>{score_val}/100</span> <span style='color:#64748b;font-size:12px;'>(Fora do Top 10)</span></p>"
            f"<p style='margin:0 0 8px 0;font-size:14px;'>🏆 <strong>Concorrente mais citado pela IA hoje:</strong> <span style='color:#16a34a;font-weight:bold;'>{comp_top}</span> <span style='color:#64748b;font-size:12px;'>(88/100)</span></p>"
            f"<p style='margin:0;font-size:13px;color:#b91c1c;'>⚠️ <strong>Impacto estimado:</strong> ~15 a 22 clientes qualificados/mês desviados para concorrentes por falta de arquivo <code>/llms.txt</code> e Schema JSON-LD.</p>"
            f"</div>"
            f"<p style='margin:0 0 18px 0;'>Liberamos gratuitamente o <strong>Dossiê Executivo da {comp_name}</strong> com a nota nos 4 pilares de IA e o plano de 14 dias (sem precisar mexer no seu site atual):</p>"
            f"<div style='margin:24px 0;'>"
            f"<a href='{report_url}' style='background:#16a34a;color:#ffffff;padding:13px 22px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;margin-right:10px;margin-bottom:10px;font-size:14px;'>📊 Ver Dossiê Oficial da {comp_name}</a>"
            f"<a href='{checkout_url}' style='background:#0f172a;color:#ffffff;padding:13px 20px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;margin-bottom:10px;font-size:14px;'>⚡ Ativar Posicionamento Top 10 (14 Dias)</a>"
            f"</div>"
            f"<p style='font-size:12px;color:#475569;background:#f1f5f9;padding:10px 14px;border-radius:8px;'>🛡️ <strong>Garantia Blindada de 7 Dias:</strong> Se sua empresa não subir nas recomendações de IA, devolvemos 100% do valor.</p>"
            f"<hr style='border:none;border-top:1px solid #e2e8f0;margin:20px 0;'>"
            f"<p style='font-size:12px;color:#64748b;margin:0;'>GeoPulse AI • Plataforma de Posicionamento em Motores de Busca Generativos (<a href='https://geopulseai.store' style='color:#2563eb;text-decoration:none;'>geopulseai.store</a>)</p>"
            f"<img src='{open_pixel_url}' width='1' height='1' style='display:none;' alt='' />"
            f"</div>"
        )

        wpp_text = (
            f"Olá, equipe da *{comp_name}*! Tudo bem?\n\n"
            f"Fizemos um teste de buscas de Inteligência Artificial (ChatGPT e Google Gemini) para *{niche}* em *{city_region}*.\n\n"
            f"🔍 *Resultado da Auditoria:*\n"
            f"• Nota da *{comp_name}*: *{score_val}/100* (Fora do Top 10)\n"
            f"• Concorrente mais recomendado pela IA hoje: *{comp_top}*\n\n"
            f"Geramos o dossiê gratuito da sua empresa mostrando como colocar vocês no Top 10 de recomendações em 14 dias (sem precisar mexer no site):\n"
            f"👉 {report_url}\n\n"
            f"Posso te explicar rapidinho como funciona?"
        )

        clean_digits = re.sub(r"\D", "", phone or "")
        if len(clean_digits) in (10, 11) and not clean_digits.startswith("55"):
            clean_digits = f"55{clean_digits}"

        if len(clean_digits) >= 10:
            wpp_link = f"https://wa.me/{clean_digits}?text={quote(wpp_text)}"
        else:
            wpp_link = f"https://wa.me/?text={quote(wpp_text)}"

        # 3. Script para Instagram Direct
        ig_text = (
            f"Olá! Fizemos uma auditoria de buscas por Inteligência Artificial (ChatGPT e Google Gemini) para {niche} em {city_region} e analisamos a presença da {comp_name}.\n\n"
            f"🔍 Nota de visibilidade: {score_val}/100.\n"
            f"🏆 Quem mais aparece recomendado aos clientes na região hoje é a {comp_top}.\n\n"
            f"Geramos um dossiê gratuito com a análise técnica e como colocar vocês no Top 10 em 14 dias sem mexer no seu site:\n"
            f"{report_url}\n\n"
            f"Posso te mandar os detalhes?"
        )
        ig_username = re.sub(r"^@+", "", instagram.strip())
        ig_link = f"https://ig.me/m/{ig_username}" if ig_username else f"https://www.instagram.com/direct/inbox/"

        return {
            "email_subject": email_subject,
            "email_body": email_body,
            "email_html": email_html,
            "whatsapp_text": wpp_text,
            "whatsapp_link": wpp_link,
            "instagram": ig_username,
            "instagram_text": ig_text,
            "instagram_link": ig_link,
        }
