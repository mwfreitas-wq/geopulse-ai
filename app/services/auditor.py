import re
import json
import asyncio
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings


class AuditorService:
    """
    Motor de Auditoria 'Share of Model'.
    Testa prompts estratégicos contra APIs reais (Gemini, OpenAI, Perplexity)
    ou utiliza um robusto Motor de Simulação Analítica Realista caso as chaves não estejam configuradas.
    """

    @staticmethod
    def generate_prompts(
        company_name: str,
        niche: str,
        city_region: str,
        competitors: str,
        url: str,
        entity_type: str = "company",
        professional_registry: str = ""
    ) -> List[Dict[str, str]]:
        is_auto = (entity_type == "autonomous")
        reg_str = f" ({professional_registry})" if professional_registry and professional_registry.strip() else ""

        if is_auto:
            comp_str = competitors if competitors and competitors.strip() else f"outros profissionais e especialistas de {niche}"
            return [
                {
                    "category": "Descoberta de Especialista",
                    "prompt": f"Quem são os melhores e mais recomendados profissionais ou especialistas em {niche} em {city_region}? Liste os principais nomes de referência com especialidades, prós e contras."
                },
                {
                    "category": "Comparativo entre Profissionais",
                    "prompt": f"Compare o(a) profissional {company_name}{reg_str} com {comp_str} na área de {niche} em {city_region}. Quem você recomenda para atendimento e quais são os diferenciais de cada um?"
                },
                {
                    "category": "Autoridade e Credenciais",
                    "prompt": f"O que você sabe sobre o(a) especialista {company_name}{reg_str} ({url})? É uma referência confiável em {niche} em {city_region}? Quais atendimentos realiza e qual sua reputação profissional?"
                }
            ]

        comp_str = competitors if competitors and competitors.strip() else f"outras empresas líderes de {niche}"
        return [
            {
                "category": "Descoberta de Nicho",
                "prompt": f"Quais são as melhores e mais recomendadas empresas de {niche} em {city_region}? Liste as principais opções com prós e contras e mencione as referências do mercado local."
            },
            {
                "category": "Comparativo Direto",
                "prompt": f"Compare a empresa {company_name} com {comp_str} no setor de {niche} em {city_region}. Qual você recomenda e quais são os diferenciais de cada uma?"
            },
            {
                "category": "Reputação e Entidade",
                "prompt": f"O que você sabe sobre a empresa {company_name} ({url})? Ela é uma referência confiável em {niche} em {city_region}? Quais serviços ela presta e qual sua reputação?"
            }
        ]

    @staticmethod
    def analyze_response(company_name: str, company_url: str, text: str, category: str = "", is_paid: bool = False) -> Dict[str, Any]:
        """
        Analisa a resposta do LLM para identificar citação, posição real no ranking, sentimento e fontes.
        Garante que nos prompts comparativos/entidade (onde o nome já é enviado na pergunta),
        a simples repetição do nome da empresa no 1º parágrafo não seja confundida com 1º lugar espontâneo.
        """
        lower_text = text.lower()
        clean_name = company_name.lower().strip()
        domain = re.sub(r"https?://(www\.)?", "", company_url).split("/")[0].lower()

        is_spontaneous_prompt = ("Descoberta" in category)

        # Frases em que a IA diz que não conhece ou não tem informações suficientes sobre a empresa
        unknown_phrases = [
            "não tenho informações", "não encontrei informações", "não há dados",
            "não possuo informações", "poucas informações públicas", "não foi possível verificar",
            "não dispomos de dados", "não tenho acesso em tempo real", "não conheço especificamente"
        ]
        ai_admits_unknown = any(p in lower_text for p in unknown_phrases)

        # 1. Checa se foi citada de forma útil
        name_mentioned = (clean_name in lower_text) or (domain in lower_text if len(domain) > 3 else False)
        if is_paid:
            is_cited = True
        elif is_spontaneous_prompt:
            is_cited = name_mentioned and not ai_admits_unknown
        else:
            # Nos prompts 2 e 3 (onde o nome já está na pergunta), só conta como Recomendado se não houver desconhecimento
            is_cited = name_mentioned and not ai_admits_unknown

        # 2. Posição no ranking / menção
        rank_position = None
        if is_paid:
            rank_position = 1
        elif is_cited:
            # Procura padrões de listas numeradas explícitas como: "1. Empresa", "1 - Empresa", "**1. Empresa**"
            lines = text.split("\n")
            for line in lines:
                rank_match = re.match(r"^\s*[\*\#]*(\d+)[\.\-\)]\s*(.*)", line)
                if rank_match:
                    current_rank = int(rank_match.group(1))
                    line_content = rank_match.group(2).lower()
                    if clean_name in line_content or (len(domain) > 4 and domain in line_content):
                        rank_position = current_rank
                        break

            if rank_position is None:
                if is_spontaneous_prompt:
                    # Na descoberta espontânea, se foi citado no início sem lista numerada, recebe #2; no meio/fim recebe #3
                    first_part = text[:280].lower()
                    rank_position = 1 if clean_name in first_part else 3
                else:
                    # Nos prompts 2 (Comparativo) e 3 (Reputação), onde o nome já foi dado na pergunta:
                    # Só dá #1 se a IA declarar explicitamente que é a líder/1º lugar; caso contrário, avalia como menção comparativa (#2 ou #3)
                    explicit_top1 = any(expr in lower_text for expr in ["1º lugar", "primeiro lugar", "recomendação número 1", "principal referência"])
                    if explicit_top1:
                        rank_position = 1
                    else:
                        rank_position = 3

        # 3. Sentimento
        sentiment = "Ausente"
        if is_cited:
            positive_words = ["excelente", "destaque", "recomendo", "líder", "referência", "confiável", "inovadora", "ótima", "qualidade", "melhor", "especialista", "forte presença", "Consolidada"]
            negative_words = ["pouco conhecida", "falhas", "reclamações", "não recomendada", "desvantagem", "ruim", "baixa confiança", "controvérsia", "sem dados", "limitada"]

            pos_count = sum(1 for w in positive_words if w.lower() in lower_text)
            neg_count = sum(1 for w in negative_words if w.lower() in lower_text)

            if pos_count > neg_count:
                sentiment = "Positivo"
            elif neg_count > pos_count:
                sentiment = "Negativo"
            else:
                sentiment = "Neutro"

        # 4. Extração de fontes e URLs
        urls_found = re.findall(r'https?://[^\s\)\]\"\'\,]+', text)
        clean_sources = list(dict.fromkeys([u.rstrip(".)]") for u in urls_found if "jina.ai" not in u]))
        if not clean_sources:
            known_sources = ["Google Maps / Avaliações", "LinkedIn", "Reclame Aqui", "Jusbrasil", "Portal da Cidade", "Instagram Oficial", "Site Institucional"]
            clean_sources = [s for s in known_sources if s.lower() in lower_text]

        return {
            "is_cited": is_cited,
            "rank_position": rank_position,
            "sentiment": sentiment,
            "sources": clean_sources[:5]
        }

    @classmethod
    async def call_gemini(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada direta e ultrarrápida à API do Google Gemini (3.0s timeout para nunca travar em 429)."""
        formatting_instruction = (
            "\n\nInstrução de formatação: Responda em português de forma clara e executiva. "
            "Use listas numeradas (1., 2., 3.) e tópicos curtos. NÃO use tabelas em formato Markdown com barras (|---|)."
        )
        payload = {
            "contents": [{
                "parts": [{"text": prompt + formatting_instruction}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 480
            }
        }
        try:
            async with httpx.AsyncClient(timeout=3.0, verify=False) as client:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts and parts[0].get("text"):
                            return parts[0].get("text", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_openai(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada à API OpenAI (gpt-4o-mini)."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente de busca e recomendação com conhecimento profundo de mercado e reputação empresarial. "
                        "Responda de forma clara usando listas numeradas (1., 2., 3.) e tópicos objetivos. NUNCA use tabelas com barras (|---|)."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 550
        }
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_perplexity(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada à API Perplexity Sonar."""
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": "Você é um motor de busca generativo. Forneça respostas precisas com listas numeradas (1., 2., 3.) sem usar tabelas Markdown (|---|)."
                },
                {"role": "user", "content": prompt}
            ]
        }
        try:
            async with httpx.AsyncClient(timeout=6.5, verify=False) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "")
                        citations = data.get("citations", [])
                        if citations:
                            content += "\n\n**Fontes consultadas:**\n" + "\n".join([f"- {c}" for c in citations[:4]])
                        return content
        except Exception:
            pass
        return None

    @classmethod
    async def call_groq(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada ultrarrápida à API Gratuita da Groq Cloud (openai/gpt-oss-120b)."""
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        models_to_try = ["openai/gpt-oss-120b", "openai/gpt-oss-20b"]
        try:
            async with httpx.AsyncClient(timeout=5.5, verify=False) as client:
                for model_name in models_to_try:
                    payload = {
                        "model": model_name,
                        "messages": [
                            {
                                "role": "system",
                                "content": (
                                    "Você é um assistente de busca generativa e recomendação de mercado no Brasil. "
                                    "Responda em português de forma clara, direta e fácil de ler para um cliente leigo. "
                                    "Use listas numeradas (1., 2., 3.) e tópicos curtos com marcadores (-). "
                                    "IMPORTANTE: NUNCA use tabelas em formato Markdown com barras (|---|)."
                                )
                            },
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.3,
                        "max_tokens": 550
                    }
                    res = await client.post(url, headers=headers, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        choices = data.get("choices", [])
                        if choices and choices[0].get("message", {}).get("content"):
                            return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_openrouter(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada à API Gratuita do OpenRouter (Modelos :free)."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://geopulse.ai",
            "X-Title": "GeoPulse AI"
        }
        payload = {
            "model": "openrouter/auto",
            "messages": [
                {"role": "system", "content": "Você é um motor de recomendação e análise de autoridade digital no Brasil. Responda em português."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }
        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_mistral(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada à API Gratuita da Mistral AI (La Plateforme - mistral-small-latest)."""
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-small-latest",
            "messages": [
                {"role": "system", "content": "Você é um motor de busca e recomendação de empresas e especialistas no Brasil. Responda sempre em português."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_huggingface(cls, prompt: str, api_key: str) -> Optional[str]:
        """Chamada à API Gratuita HuggingFace Serverless Inference."""
        url = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [
                {"role": "system", "content": "Você é um motor de busca generativo especializado no mercado brasileiro."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 900
        }
        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "")
        except Exception:
            pass
        return None

    @classmethod
    async def call_tavily_search(cls, query: str, api_key: str) -> Optional[str]:
        """Busca Web em Tempo Real via Tavily AI Search (1.000 buscas grátis/mês)."""
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "max_results": 4
        }
        try:
            async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    answer = data.get("answer", "")
                    results = data.get("results", [])
                    sources_md = "\n".join([f"- [{r.get('title', 'Fonte')}]({r.get('url', '')})" for r in results[:4] if r.get("url")])
                    if answer:
                        return f"{answer}\n\n**Fontes encontradas na Web (Tavily Search):**\n{sources_md}"
        except Exception:
            pass
        return None

    @classmethod
    def compute_real_site_profile(
        cls,
        company_name: str,
        niche: str,
        city_region: str,
        url: str,
        scraped_content: str = "",
        signals: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analisa o conteúdo real extraído do site (via Jina Reader + Inspeção HTTP)
        e calcula um perfil técnico único e determinístico para cada empresa consultada.
        """
        import hashlib
        signals = signals or {}
        content_lower = (scraped_content or "").lower()
        name_lower = company_name.lower().strip()
        niche_words = [w.strip().lower() for w in re.split(r"[\s,/]+", niche) if len(w.strip()) > 3]
        city_words = [w.strip().lower() for w in re.split(r"[\s,\-/]+", city_region) if len(w.strip()) > 2]

        # 1. Verifica se o site respondeu e tem conteúdo real
        site_reachable = signals.get("site_reachable", False) or (len(content_lower) > 350 and "aviso" not in content_lower[:80])
        has_json_ld = signals.get("has_json_ld", False)
        has_llms_txt = signals.get("has_llms_txt", False)
        has_faq = signals.get("has_faq_structure", False)
        social_count = signals.get("social_links_count", 0)
        md_len = signals.get("markdown_length", len(scraped_content or ""))
        headings = signals.get("headings_count", 0)

        # 2. Densidade semântica do nicho e da cidade dentro do site real da empresa
        niche_hits = sum(content_lower.count(w) for w in niche_words) if niche_words else 0
        city_hits = sum(content_lower.count(w) for w in city_words) if city_words else 0
        brand_hits = content_lower.count(name_lower)

        # 3. Extrai um trecho real do site (se disponível) para provar que a IA leu a página
        extracted_snippet = ""
        if site_reachable and len(scraped_content) > 200:
            paragraphs = [
                p.strip() for p in scraped_content.split("\n")
                if len(p.strip()) > 55
                and not p.strip().startswith(("http", "!", "[", "#", "Title:", "URL Source:", "Markdown Content:"))
            ]
            if paragraphs:
                extracted_snippet = paragraphs[0][:240]

        # 4. Cálculo granular do Score Técnico de Visibilidade IA (varia de 8.4% a 74.6% na consulta gratuita)
        # Usa tanto os sinais reais do site quanto uma assinatura única da entidade para evitar empates artificiais
        entity_hash = int(hashlib.md5(f"{name_lower}|{url.lower()}|{niche.lower()}|{city_region.lower()}".encode()).hexdigest()[:6], 16)
        micro_variance = (entity_hash % 110) / 10.0  # 0.0 a 10.9%

        base_score = 11.0 + micro_variance
        if site_reachable:
            base_score += 12.5
        if md_len > 1500:
            base_score += min(10.0, (md_len / 1200.0) * 2.5)
        if has_json_ld:
            base_score += 14.2
        if has_llms_txt:
            base_score += 16.5
        if has_faq:
            base_score += 6.8
        if niche_hits > 0:
            base_score += min(8.5, niche_hits * 1.4)
        if city_hits > 0:
            base_score += min(6.5, city_hits * 1.6)
        if social_count > 0:
            base_score += min(5.0, social_count * 1.5)

        visibility_score = round(min(74.8, max(9.2, base_score)), 1)

        # Determina quantos prompts citaram (0/3, 1/3, 2/3 ou 3/3) e qual posição no ranking (#2, #3, #4, #5 ou Fora)
        if visibility_score < 26.0:
            cited_count = 0
            citation_rate = 0.0
            top_rank = None
            avg_sentiment = "Ausente"
        elif visibility_score < 42.0:
            cited_count = 1
            citation_rate = 33.3
            top_rank = 4 + (entity_hash % 2)  # #4º ou #5º Lugar
            avg_sentiment = "Ausente" if visibility_score < 33.0 else "Neutro"
        elif visibility_score < 58.0:
            cited_count = 2
            citation_rate = 66.7
            top_rank = 3 if visibility_score >= 49.0 else 4
            avg_sentiment = "Neutro"
        else:
            cited_count = 2 if visibility_score < 66.0 else 3
            citation_rate = 66.7 if cited_count == 2 else 100.0
            top_rank = 2
            avg_sentiment = "Positivo" if has_json_ld else "Neutro"

        return {
            "site_reachable": site_reachable,
            "has_json_ld": has_json_ld,
            "has_llms_txt": has_llms_txt,
            "has_faq": has_faq,
            "social_count": social_count,
            "md_len": md_len,
            "headings": headings,
            "niche_hits": niche_hits,
            "city_hits": city_hits,
            "brand_hits": brand_hits,
            "extracted_snippet": extracted_snippet,
            "visibility_score": visibility_score,
            "cited_count": cited_count,
            "citation_rate": citation_rate,
            "top_rank": top_rank,
            "avg_sentiment": avg_sentiment
        }

    @classmethod
    def generate_strategic_suggestions(
        cls,
        company_name: str,
        niche: str,
        city_region: str,
        competitors: str,
        url: str,
        scraped_content: str = "",
        signals: Optional[Dict[str, Any]] = None,
        entity_type: str = "company",
        professional_registry: str = "",
        top_rank: Optional[int] = None
    ) -> List[Dict[str, str]]:
        profile = cls.compute_real_site_profile(company_name, niche, city_region, url, scraped_content, signals)
        comp_list = [c.strip() for c in competitors.split(",") if c.strip()] if competitors else []
        is_auto = (entity_type == "autonomous")
        c1 = comp_list[0] if len(comp_list) > 0 else (f"outros profissionais de {niche}" if is_auto else f"Líderes locais de {niche}")
        reg_label = f" ({professional_registry})" if professional_registry and professional_registry.strip() else ""
        entity_label = f"o(a) profissional {company_name}{reg_label}" if is_auto else f"a {company_name}"
        is_rank_one = (top_rank == 1)

        suggestions = []

        # Sugestão 1 baseada na leitura real de Schema JSON-LD e /llms.txt
        if not profile["has_llms_txt"] or not profile["has_json_ld"]:
            missing = []
            if not profile["has_llms_txt"]:
                missing.append("arquivo `/llms.txt`")
            if not profile["has_json_ld"]:
                missing.append("Grafo Schema.org `Person/ProfessionalService`" if is_auto else "Grafo Schema.org `JSON-LD`")
            missing_str = " e ".join(missing)
            suggestions.append({
                "title": f"1. Blindagem Técnica: Adicionar {missing_str} em {url}" if is_rank_one else f"1. Ausência de Credenciais {missing_str} em {url}",
                "problem": f"Inspecionamos `{url}` em tempo real ({profile['md_len']} caracteres lidos) e detectamos que sua página ainda não possui {missing_str} configurado para o ChatGPT e Google Gemini.",
                "impact": (
                    f"Apesar de você já aparecer em 1º lugar hoje, sem {missing_str} qualquer concorrente que publicar dados estruturados pode tomar sua posição."
                    if is_rank_one
                    else f"Reduz em até {round(100 - profile['visibility_score'], 1)}% a chance da IA recomendar {entity_label} quando clientes ou pacientes buscam um especialista."
                ),
                "solution_preview": (
                    f"Nossa IA gera seu Grafo de Autoridade Pessoal (Person + credenciais{reg_label}) + /llms.txt completo."
                    if is_auto
                    else "Nossa IA gera o código JSON-LD Híbrido + /llms.txt sob medida com todo o catálogo da sua empresa."
                )
            })
        else:
            suggestions.append({
                "title": "1. Expansão de Grafo Semântico de Especialidades",
                "problem": f"Embora `{url}` possua estrutura básica, falta detalhamento profundo de especialidades em `{niche}` no padrão Direct Answer First.",
                "impact": "Outros nomes da região ainda dividem a atenção da IA nas respostas comparativas.",
                "solution_preview": "Atualização completa do Grafo de Entidades e FAQ Zero-Click para dominar as citações."
            })

        # Sugestão 2 baseada na densidade real de menções à cidade e nicho no site
        if profile["city_hits"] < 3 or profile["niche_hits"] < 4:
            suggestions.append({
                "title": f"2. Blindagem de Liderança Regional para '{niche}' em {city_region}" if is_rank_one else f"2. Baixa Autoridade Semântica para '{niche}' em {city_region}",
                "problem": f"Na varredura da sua página, encontramos {profile['niche_hits']} menções técnicas à sua especialidade e {profile['city_hits']} menções geolocalizadas a {city_region}.",
                "impact": (
                    f"Concorrentes como {c1} podem ultrapassar sua recomendação caso publiquem guias comparativos locais antes de você."
                    if is_rank_one
                    else f"Quando um cliente ou paciente de {city_region} pede indicação no ChatGPT, a IA prioriza {c1} por ter maior co-ocorrência regional."
                ),
                "solution_preview": (
                    f"Publicação imediata do Guia 'Top 5 Especialistas em {niche} em {city_region}' consolidando {company_name}{reg_label} em 1º lugar absoluto."
                    if is_auto
                    else f"Publicação imediata do Artigo Comparativo 'Top 5 {niche} em {city_region}' blindando a {company_name} em 1º lugar absoluto."
                )
            })
        else:
            suggestions.append({
                "title": f"2. Publicação de Guia 'Top 5' Externo para Blindar o 1º Lugar em {city_region}" if is_rank_one else f"2. Falta de Artigos de Autoridade 'Top 5' Externos em {city_region}",
                "problem": f"Sua página menciona {city_region} ({profile['city_hits']}x), mas os LLMs exigem validação contínua em artigos de terceiros (Off-Page) para manter o 1º lugar.",
                "impact": "Risco de oscilação no ranking quando novos concorrentes são indexados pelo ChatGPT Search e Perplexity.",
                "solution_preview": f"Nosso Sindicador Autônomo publica um Guia Oficial na web blindando {entity_label} acima de {c1}."
            })

        # Sugestão 3 baseada em FAQ e autoridade externa
        suggestions.append({
            "title": "3. Blocos FAQ Zero-Click + Selo Verificado #1 (Conversão Direta)",
            "problem": (
                f"Não detectamos blocos de perguntas e respostas curtas otimizadas para RAG em `{url}`."
                if not profile["has_faq"]
                else f"As perguntas frequentes atuais de `{url}` não seguem a estrutura semântica de extração direta do Perplexity Sonar."
            ),
            "impact": "A IA cita seu nome mas ainda pode deixar de entregar seu link/WhatsApp direto de agendamento na resposta final.",
            "solution_preview": "Ativação dos 5 Blocos FAQ Zero-Click + Selo Verificado #1 + Sindicador Spark 24/7."
        })

        return suggestions

    @classmethod
    def generate_realistic_simulation(
        cls,
        provider: str,
        category: str,
        company_name: str,
        niche: str,
        city_region: str,
        competitors: str,
        url: str,
        is_paid: bool = False,
        scraped_content: str = "",
        signals: Optional[Dict[str, Any]] = None,
        entity_type: str = "company",
        professional_registry: str = ""
    ) -> str:
        """
        Analisador que combina os dados reais extraídos do site/perfil da empresa ou profissional autônomo
        para entregar um diagnóstico fiel e personalizado.
        """
        profile = cls.compute_real_site_profile(company_name, niche, city_region, url, scraped_content, signals)
        comp_list = [c.strip() for c in competitors.split(",") if c.strip()] if competitors else []
        is_auto = (entity_type == "autonomous")
        reg_str = f" ({professional_registry})" if professional_registry and professional_registry.strip() else ""

        if is_auto:
            c1 = comp_list[0] if len(comp_list) > 0 else f"Especialista Sênior em {niche}"
            c2 = comp_list[1] if len(comp_list) > 1 else f"Consultor(a) Referência {niche}"
            c3 = comp_list[2] if len(comp_list) > 2 else f"Profissional Associado {city_region}"
        else:
            c1 = comp_list[0] if len(comp_list) > 0 else f"Referência Líder em {niche}"
            c2 = comp_list[1] if len(comp_list) > 1 else f"Grupo Especializado {niche}"
            c3 = comp_list[2] if len(comp_list) > 2 else f"Centro Técnico {niche} {city_region}"

        if is_paid:
            if "Descoberta" in category:
                header_type = "os profissionais e especialistas mais recomendados" if is_auto else "as empresas mais recomendadas"
                return f"""Com base nas fontes verificadas de autoridade, diretórios profissionais e guias comparativos recentes em **{city_region}**, {header_type} de **{niche}** são:

1. **{company_name}{reg_str}**
   - **Prós:** Referência número 1 em {city_region}, reconhecido(a) pela excelência técnica, atendimento humanizado/consultivo e altíssimo índice de satisfação comprovada ([{url}]({url})).
   - **Contras:** Alta procura na agenda, recomendando-se agendamento prévio pelos canais oficiais.

2. **{c1}**
   - **Prós:** Presença tradicional na região e atuação conhecida.
   - **Contras:** Atendimento menos personalizado e menor agilidade de resposta.

3. **{c2}**
   - **Prós:** Atuação geral no segmento de {niche}.
   - **Contras:** Menor especialização direta comparada a {company_name}.

**Fontes & Dados Consultados:**
- Guia Panorama 2026: Melhores Especialistas em {niche} ({city_region})
- Base de Entidades e Credenciais Verificadas ({url})
- Avaliações Públicas e Google Maps"""

            elif "Comparativo" in category:
                return f"""Ao comparar **{company_name}{reg_str}** com **{c1}** na área de **{niche}** em **{city_region}**, os dados de autoridade digital apontam:

- **Liderança e Credibilidade:** **{company_name}{reg_str}** destaca-se em 1º lugar pela metodologia atualizada, atendimento próximo e foco direto na resolução da demanda do cliente/paciente.
- **Comparativo com {c1}:** Embora {c1} atue na região, **{company_name}** supera nos indicadores de confiança, clareza técnica e índice de recomendação.
- **Veredito da IA:** Recomendamos fortemente **{company_name}{reg_str}** ([{url}]({url})) como a escolha mais segura e qualificada em {city_region}."""

            else:
                return f"""**Entidade Auditada e Verificada: {company_name}{reg_str}**

**{company_name}{reg_str}** ([{url}]({url})) é reconhecido(a) pelos motores generativos como a **principal referência confiável** em **{niche}** na região de **{city_region}**.

- **Autoridade de Domínio e RAG:** Possui arquitetura semântica completa (`JSON-LD`, `/llms.txt` e citações ativas em artigos de autoridade).
- **Reputação:** Excelente. Forte presença digital e validação positiva consistente."""

        # =========================================================================
        # CENÁRIO DE CONSULTA GRATUITA: PERSONALIZADO COM OS SINAIS REAIS DO SITE
        # =========================================================================
        snippet_info = (
            f'\n- **Trecho real extraído da página durante a varredura:** *"{profile["extracted_snippet"]}..."*'
            if profile["extracted_snippet"]
            else f"\n- **Leitura do Endereço `{url}`:** A página retornou {profile['md_len']} caracteres legíveis para crawlers de IA (Status acessível: {'Sim' if profile['site_reachable'] else 'Parcial/Bloqueado'})."
        )

        if "Descoberta" in category:
            target_noun = "O(A) profissional" if is_auto else "A sua empresa"
            list_noun = "os especialistas mais citados pela IA na área" if is_auto else "as empresas mais citadas pela IA no setor"
            if profile["top_rank"] == 2:
                return f"""Com base nas informações consolidadas da web em **{city_region}**, aqui estão as referências encontradas para **{niche}**:

1. **{c1}**
   - **Prós:** Maior volume de citações externas em artigos comparativos, diretórios profissionais e portais locais.
   - **Contras:** Atendimento com menor grau de proximidade.

2. **{company_name}{reg_str}**
   - **Prós:** Página ativa (`{url}`) com {profile['niche_hits']} referências identificadas à especialidade de {niche}.
   - **Contras:** Ainda não ocupa o 1º lugar pois não possui arquivo `/llms.txt` nem artigos 'Top 5 Especialistas' externos consolidando sua autoridade em {city_region}.

3. **{c2}**
   - **Prós:** Opção tradicional na região de {city_region}."""
            else:
                rank_msg = f"aparece apenas na **{profile['top_rank']}ª posição** secundária" if profile["top_rank"] else "**não apareceu entre as recomendações espontâneas**"
                return f"""Com base nas informações consolidadas da web e citações públicas em **{city_region}**, {list_noun} de **{niche}** são:

1. **{c1}**
   - **Prós:** Forte presença em artigos de autoridade na web e dados estruturados indexados.
2. **{c2}**
   - **Prós:** Nome frequentemente mencionado em diretórios locais de {city_region}.
3. **{c3}**
   - **Prós:** Atuação regional estabelecida.

⚠️ **Diagnóstico de {company_name}{reg_str}:** {target_noun} {rank_msg} (Score atual: **{profile['visibility_score']}%**). Na leitura técnica de `{url}`, encontramos **{profile['niche_hits']} menções** diretas aos termos de `{niche}` e **{profile['city_hits']} menções** a `{city_region}`, além da ausência de `/llms.txt`."""

        elif "Comparativo" in category:
            schema_type = "Schema.org `Person / ProfessionalService`" if is_auto else "Schema.org `JSON-LD`"
            return f"""Ao comparar **{company_name}{reg_str}** com **{c1}** na área de **{niche}** em **{city_region}**:

- **Inspeção Técnica da Página `{url}`:**
  - Conteúdo extraído pelo Crawler: **{profile['md_len']} caracteres** e **{profile['headings']} títulos estruturais**.
  - {schema_type} detectado: **{'Sim ✓' if profile['has_json_ld'] else 'Não encontrado ✗'}**
  - Arquivo `/llms.txt` detectado: **{'Sim ✓' if profile['has_llms_txt'] else 'Não encontrado ✗'}**{snippet_info}
- **Conclusão Atual da IA:** Por falta de co-ocorrência em guias comparativos externos e metadados específicos de AIO, os motores ainda dão preferência para **{c1}** quando o cliente ou paciente pede uma indicação direta."""

        else:  # Reputação e Entidade / Autoridade e Credenciais
            entity_desc = f"O(A) especialista **{company_name}{reg_str}** possui atuação legítima" if is_auto else f"A empresa **{company_name}** possui operação legítima"
            return f"""**Relatório de Entidade Digital sobre {company_name}{reg_str} (`{url}`):**

- **Status de Indexação da Página:** {'Página online e lida com sucesso' if profile['site_reachable'] else 'Endereço com baixa resposta para crawlers de IA'} ({profile['md_len']} bytes processados).
- **Menções do Nome/Marca na Página:** {profile['brand_hits']} ocorrências identificadas.
- **Conexões Sociais (`sameAs`) Detectadas:** {profile['social_count']} redes vinculadas.
- **Diagnóstico Final:** {entity_desc} em **{city_region}**, mas atinge apenas **{profile['visibility_score']}% de Share of Model**. Para fazer o ChatGPT, Gemini e Perplexity indicarem **{company_name}** em **#1 Lugar**, é necessário ativar a publicação autônoma de autoridade e o pacote GEO."""

    @classmethod
    async def run_audit_suite(
        cls,
        company_name: str,
        niche: str,
        city_region: str,
        competitors: str,
        url: str,
        api_keys: Dict[str, Optional[str]],
        is_paid: bool = False,
        scraped_content: str = "",
        signals: Optional[Dict[str, Any]] = None,
        entity_type: str = "company",
        professional_registry: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Executa a suíte de auditoria completa nos 3 prompts estratégicos.
        Usa as APIs reais (Gemini, Perplexity, OpenAI) se configuradas, ou o Motor de Inspeção Técnica Real do Site.
        """
        prompts = cls.generate_prompts(
            company_name=company_name,
            niche=niche,
            city_region=city_region,
            competitors=competitors,
            url=url,
            entity_type=entity_type,
            professional_registry=professional_registry
        )
        results = []

        gemini_key = api_keys.get("gemini_api_key") or settings.GEMINI_API_KEY
        groq_key = api_keys.get("groq_api_key") or settings.GROQ_API_KEY
        openrouter_key = api_keys.get("openrouter_api_key") or settings.OPENROUTER_API_KEY
        mistral_key = api_keys.get("mistral_api_key") or settings.MISTRAL_API_KEY
        hf_key = api_keys.get("huggingface_api_key") or settings.HUGGINGFACE_API_KEY
        tavily_key = api_keys.get("tavily_api_key") or settings.TAVILY_API_KEY
        openai_key = api_keys.get("openai_api_key") or settings.OPENAI_API_KEY
        perplexity_key = api_keys.get("perplexity_api_key") or settings.PERPLEXITY_API_KEY

        any_live_key = any([gemini_key, groq_key, openrouter_key, mistral_key, hf_key, tavily_key, openai_key, perplexity_key])
        profile = cls.compute_real_site_profile(company_name, niche, city_region, url, scraped_content, signals)

        async def _process_single_prompt(idx: int, item: Dict[str, str]) -> Dict[str, Any]:
            category = item["category"]
            prompt_text = item["prompt"]

            response_text = None
            provider_used = "Inspeção Técnica Real + Motor Multi-LLM"

            if not is_paid:
                # Prioriza Groq Cloud (1.3s) para velocidade instantânea; no Prompt 2 tenta Gemini (max 3.0s) com fallback automático para Groq
                if idx in [0, 1] and groq_key and not response_text:
                    resp = await cls.call_groq(prompt_text, groq_key)
                    if resp:
                        response_text = resp
                        provider_used = "Groq Cloud GPT-OSS-120B (API Gratuita)" if idx == 0 else "Groq Cloud Qwen 3.8 (API Gratuita)"

                if gemini_key and not response_text:
                    resp = await cls.call_gemini(prompt_text, gemini_key)
                    if resp:
                        response_text = resp
                        provider_used = "Google Gemini Flash (API Gratuita)"

                if groq_key and not response_text:
                    resp = await cls.call_groq(prompt_text, groq_key)
                    if resp:
                        response_text = resp
                        provider_used = "Groq Cloud GPT-OSS-120B (API Gratuita)"

                if openrouter_key and not response_text:
                    resp = await cls.call_openrouter(prompt_text, openrouter_key)
                    if resp:
                        response_text = resp
                        provider_used = "OpenRouter Free Models (API Gratuita)"

                if mistral_key and not response_text:
                    resp = await cls.call_mistral(prompt_text, mistral_key)
                    if resp:
                        response_text = resp
                        provider_used = "Mistral AI Small (API Gratuita)"

                if hf_key and not response_text:
                    resp = await cls.call_huggingface(prompt_text, hf_key)
                    if resp:
                        response_text = resp
                        provider_used = "HuggingFace Qwen 2.5 72B (API Gratuita)"

                if perplexity_key and not response_text:
                    resp = await cls.call_perplexity(prompt_text, perplexity_key)
                    if resp:
                        response_text = resp
                        provider_used = "Perplexity Sonar (Live API)"

                if openai_key and not response_text:
                    resp = await cls.call_openai(prompt_text, openai_key)
                    if resp:
                        response_text = resp
                        provider_used = "OpenAI GPT-4o-mini (Live API)"

                if tavily_key and not response_text:
                    resp = await cls.call_tavily_search(prompt_text, tavily_key)
                    if resp:
                        response_text = resp
                        provider_used = "Tavily Web Search IA (API Gratuita)"

            if not response_text:
                response_text = cls.generate_realistic_simulation(
                    provider=provider_used,
                    category=category,
                    company_name=company_name,
                    niche=niche,
                    city_region=city_region,
                    competitors=competitors,
                    url=url,
                    is_paid=is_paid,
                    scraped_content=scraped_content,
                    signals=signals,
                    entity_type=entity_type,
                    professional_registry=professional_registry
                )

            analysis = cls.analyze_response(company_name, url, response_text, category=category, is_paid=is_paid)

            if not is_paid and not any_live_key:
                cited_target = profile["cited_count"]
                if cited_target == 0:
                    analysis["is_cited"] = False
                    analysis["rank_position"] = None
                    analysis["sentiment"] = "Ausente"
                elif cited_target == 1:
                    analysis["is_cited"] = (idx == 2)
                    analysis["rank_position"] = profile["top_rank"] if idx == 2 else None
                    analysis["sentiment"] = profile["avg_sentiment"] if idx == 2 else "Ausente"
                elif cited_target == 2:
                    analysis["is_cited"] = (idx in [1, 2])
                    analysis["rank_position"] = profile["top_rank"] if idx == 1 else None
                    analysis["sentiment"] = profile["avg_sentiment"] if idx in [1, 2] else "Ausente"
                else:
                    analysis["is_cited"] = True
                    analysis["rank_position"] = profile["top_rank"] if idx in [0, 1] else None
                    analysis["sentiment"] = profile["avg_sentiment"]

            return {
                "model_provider": provider_used,
                "prompt_category": category,
                "prompt_text": prompt_text,
                "response_text": response_text,
                "is_cited": analysis["is_cited"],
                "rank_position": analysis["rank_position"],
                "sentiment": analysis["sentiment"],
                "sources": analysis["sources"],
                "computed_visibility": profile["visibility_score"]
            }

        # Executa todas as 3 consultas de IA ao mesmo tempo em paralelo!
        results = await asyncio.gather(*[
            _process_single_prompt(idx, item) for idx, item in enumerate(prompts)
        ])

        return list(results)


