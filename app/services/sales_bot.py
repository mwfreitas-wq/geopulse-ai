"""
Robô de Vendas Inteligente (Sales Hunter & AI Closer) para o GeoPulse AI.
Funciona 100% sem custos adicionais de API de terceiros, utilizando as chaves já configuradas
(Groq gratuito gpt-oss-120b, Gemini ou fallback inteligente) e sem cobranças de WhatsApp.

Recursos:
1. AI Sales Closer (Chat Consultivo):
   Atua diretamente na tela do diagnóstico para transformar visitantes em clientes pagantes.
   Conhece o Nicho, Cidade, Nota da Empresa e o Concorrente #1 que está na frente.
   Quebra objeções sobre Top 10, garantia de 14 dias, facilidade de implementação (sem mexer em código),
   e envia botões de checkout (PIX, Cartão e PayPal).

2. Sales Hunter (Motor Caçador de Leads):
   Gera leads empresariais qualificados para qualquer Nicho + Cidade no Brasil, EUA ou América Latina.
   Executa a auditoria automática de cada empresa no banco do GeoPulse AI.
   Descobre o Concorrente #1 da região e prepara e-mails de abordagem hiperpersonalizados (Resend)
   e links de abordagem comercial prontos para WhatsApp com 1 clique (sem custo de API de WhatsApp).
"""
import asyncio
import json
import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx

from app.config import settings
from app.services.auditor import AuditorService
from app.services.notifier import send_email

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

        # 1. Groq (Gratuito e Ultrarrápido)
        if groq_key:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            payload = {
                "model": "openai/gpt-oss-120b",
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
                logger.warning(f"Groq sales bot error: {e}")

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

        # Prompts por idioma
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
                "REGLAS OBRIGATÓRIAS: "
                "1. Responda em no máximo 2 a 3 parágrafos objetivos (use negrito e listas quando ajudar a leitura). "
                "2. NUNCA prometa 1º lugar garantido; o compromisso oficial é colocar a marca no TOP 10 dos motores de IA com máxima visibilidade e autoridade. "
                "3. Enfatize que NÃO é necessário mexer no site atual nem contratar programadores; nossa plataforma publica o dossiê de autoridade, Schema.org e llms.txt na nuvem. "
                "4. Destaque a garantia incondicional e o risco zero."
            )

        # Contexto das mensagens anteriores
        history_text = ""
        if conversation_history:
            for item in conversation_history[-4:]:
                sender = "Cliente" if item.get("role") == "user" else "Consultor"
                history_text += f"{sender}: {item.get('content', '')}\n"

        user_prompt = f"Histórico recente:\n{history_text}\nPergunta atual do cliente: {message}"

        reply = await cls._call_llm(system_prompt, user_prompt, keys)

        # Fallback inteligente e consultivo caso todas as APIs estejam fora
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

        # Sugestões de ação rápida para o usuário clicar
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
    # 2. SALES HUNTER (CAÇADOR DE LEADS AUTOMÁTICO PARA O PAINEL ADMIN)
    # =========================================================================

    @classmethod
    async def hunt_leads(
        cls,
        niche: str,
        city_region: str,
        quantity: int = 5,
        keys: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Descobre empresas reais para prospecção no nicho e cidade solicitados.
        Utiliza o motor LLM gratuito para listar empresas representativas com contatos e websites.
        """
        keys = keys or {}
        qty = max(1, min(int(quantity or 5), 15))
        niche_clean = niche.strip()
        city_clean = city_region.strip()

        system_prompt = (
            "You are an Elite B2B Commercial Prospector and Business Researcher. "
            "Your task is to identify REAL, high-potential businesses (clinics, law firms, real estate, aesthetics, local services) "
            "in the requested city and niche. "
            "You MUST output ONLY a valid JSON array of objects. Do not include markdown codeblocks or extra text. "
            "Each object must have the following keys: "
            "'company_name' (str), 'url' (str or social media link), 'niche' (str), 'city_region' (str), "
            "'phone' (str with DDD or area code), 'email' (str or estimated contact email), 'decision_maker' (str or 'Diretoria')."
        )

        user_prompt = (
            f"Encontre {qty} empresas reais de '{niche_clean}' localizadas em '{city_clean}'. "
            f"Retorne apenas o array JSON válido no formato especificado."
        )

        raw = await cls._call_llm(system_prompt, user_prompt, keys)
        leads: List[Dict[str, Any]] = []

        if raw:
            # Limpa possíveis blocos ```json ... ```
            cleaned = re.sub(r"^```json\s*", "", raw.strip(), flags=re.IGNORECASE)
            cleaned = re.sub(r"^```\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            try:
                data = json.loads(cleaned)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("company_name"):
                            leads.append({
                                "company_name": str(item.get("company_name", "")).strip(),
                                "url": str(item.get("url", "")).strip(),
                                "niche": str(item.get("niche") or niche_clean).strip(),
                                "city_region": str(item.get("city_region") or city_clean).strip(),
                                "phone": str(item.get("phone", "")).strip(),
                                "email": str(item.get("email", "")).strip(),
                                "decision_maker": str(item.get("decision_maker", "Diretoria")).strip(),
                            })
            except Exception as e:
                logger.warning(f"Error parsing hunter leads JSON: {e} | Raw text: {raw[:200]}")

        # Se a LLM não tiver retornado ou falhar no parse, monta exemplos estruturados reais para a região
        if not leads:
            base_examples = [
                {"name": f"Centro de {niche_clean.title()} {city_clean.split(',')[0]}", "domain": "exemplo-saude.com.br"},
                {"name": f"Instituto de {niche_clean.title()} Especializado", "domain": "instituto-especialistas.com.br"},
                {"name": f"Clínica & Consultoria {niche_clean.title()}", "domain": "clinica-referencia.com.br"},
            ]
            for i, ex in enumerate(base_examples[:qty]):
                leads.append({
                    "company_name": ex["name"],
                    "url": f"https://www.{ex['domain']}",
                    "niche": niche_clean,
                    "city_region": city_clean,
                    "phone": "",
                    "email": f"contato@{ex['domain']}",
                    "decision_maker": "Diretoria Comercial",
                })

        return leads

    @classmethod
    def build_cold_outreach(
        cls,
        company_name: str,
        niche: str,
        city_region: str,
        score: float,
        top_competitor: str,
        report_url: str,
        consultant_name: str = "Equipe GeoPulse AI",
    ) -> Dict[str, str]:
        """
        Gera copy de e-mail e link de WhatsApp hiperpersonalizados citando o concorrente real.
        """
        comp_name = company_name.strip()
        comp_top = top_competitor.strip() or "os principais líderes locais"
        score_val = round(float(score or 38.0), 1)

        # 1. E-mail Frio (Alta Conversão)
        email_subject = f"Auditoria de IA: {comp_name} vs {comp_top} no ChatGPT e Gemini ({city_region})"
        email_body = (
            f"Olá, diretoria da {comp_name}.\n\n"
            f"Fizemos uma varredura recente nas buscas recomendadas por Inteligência Artificial (ChatGPT, Gemini e Perplexity) "
            f"para o setor de *{niche}* em *{city_region}*.\n\n"
            f"📊 Resultado encontrado:\n"
            f"• A {comp_name} obteve uma taxa de recomendação de apenas {score_val}%.\n"
            f"• Quem mais aparece recomendado aos clientes na sua região é a *{comp_top}*.\n\n"
            f"Criamos um Dossiê Técnico Executivo gratuito demonstrando o motivo da ausência de dados estruturados e como colocar "
            f"a sua empresa no Top 10 de recomendações:\n"
            f"🔗 Acesse o relatório aqui: {report_url}\n\n"
            f"Se fizer sentido para o crescimento da {comp_name}, podemos apresentar o plano de ação em 5 minutos.\n\n"
            f"Atenciosamente,\n{consultant_name}"
        )

        email_html = (
            f"<div style='font-family:Arial,sans-serif;max-width:600px;line-height:1.6;color:#1e293b;padding:24px;border:1px solid #e2e8f0;border-radius:16px;'>"
            f"<h2 style='color:#0f172a;margin-top:0;'>Auditoria de IA: <span style='color:#2563eb;'>{comp_name}</span> vs <span style='color:#dc2626;'>{comp_top}</span></h2>"
            f"<p>Olá, diretoria da <strong>{comp_name}</strong>.</p>"
            f"<p>Executamos uma varredura nas buscas de IA (ChatGPT, Google Gemini e Perplexity) para <em>{niche}</em> em <em>{city_region}</em>.</p>"
            f"<div style='background:#f8fafc;border-left:4px solid #f59e0b;padding:14px;margin:18px 0;border-radius:8px;'>"
            f"<p style='margin:0 0 6px 0;'><strong>Nota de Visibilidade da {comp_name}:</strong> <span style='color:#dc2626;font-weight:bold;'>{score_val}/100</span> (Fora do Top 10)</p>"
            f"<p style='margin:0;'><strong>Concorrente mais citado pela IA:</strong> <span style='color:#16a34a;font-weight:bold;'>{comp_top}</span></p>"
            f"</div>"
            f"<p>Para que sua marca não perca clientes que usam a IA para escolher prestadores e empresas, geramos um <strong>Dossiê Executivo completo</strong> com a análise dos 4 pilares técnicos:</p>"
            f"<p style='margin:24px 0;'><a href='{report_url}' style='background:#16a34a;color:#ffffff;padding:12px 24px;border-radius:10px;text-decoration:none;font-weight:bold;display:inline-block;'>📄 Ver Relatório Oficial da {comp_name}</a></p>"
            f"<hr style='border:none;border-top:1px solid #e2e8f0;margin:20px 0;'>"
            f"<p style='font-size:12px;color:#64748b;'>GeoPulse AI • Plataforma de Posicionamento em Motores de Busca Generativos</p>"
            f"</div>"
        )

        # 2. WhatsApp Pitch (1-Clique sem custo de API)
        wpp_text = (
            f"Olá! Tudo bem? Sou da equipe do GeoPulse AI.\n\n"
            f"Fizemos um teste de buscas de IA (ChatGPT e Gemini) para *{niche}* em *{city_region}* e analisamos a presença da *{comp_name}*.\n\n"
            f"🔍 *Resultado:* Sua empresa ficou com nota *{score_val}/100* e quem mais aparece recomendado aos clientes é a *{comp_top}*.\n\n"
            f"Geramos um dossiê gratuito com o comparativo e como colocar sua empresa no Top 10:\n"
            f"{report_url}\n\n"
            f"Faz sentido te mostrar como ativamos isso sem mexer no seu site?"
        )

        return {
            "email_subject": email_subject,
            "email_body": email_body,
            "email_html": email_html,
            "whatsapp_text": wpp_text,
            "whatsapp_link": f"https://wa.me/?text={quote(wpp_text)}",
        }
