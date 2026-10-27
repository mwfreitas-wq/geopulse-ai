/**
 * GeoPulse AI — Motor de Internacionalização (i18n) e Detecção Automática de País/Idioma
 * Suporta: Português (pt), English (en), Español (es)
 */

const I18N = {
  pt: {
    currencySymbol: "R$",
    currencyCode: "BRL",
    locale: "pt-BR",
    planPrice: 197.0,
    bumpPrice: 50.0,
    defaultTicket: 800,
    ticketMin: 100,
    ticketMax: 5000,
    ticketStep: 50,
    ticketScale: ["R$ 100", "R$ 1.500", "R$ 3.000", "R$ 5.000+"],

    liveBarTitle: "Motor 14 Dias ao Vivo:",
    marquee: [
      "⚙️ <strong>Dia 14/14 Concluído:</strong> Dr. Henrique Vasconcelos (SP) subiu de 24% para 94.5% (1º Lugar no ChatGPT Search)",
      "🚀 <strong>Dia 2/14 Executado:</strong> Clínica OdontoPrime (BH) teve seu Guia Oficial Top 5 publicado automaticamente pela IA",
      "📡 <strong>Dia 10/14 Executado:</strong> Escritório Contábil Atlas (PR) recebeu Ping IndexNow nos robôs do Bing e Perplexity",
      "📈 <strong>Dia 7/14 Executado:</strong> Dra. Camila Mendes (RJ) atingiu 78.4% na Reauditoria Intermediária do Desafio"
    ],

    navBadge: "Desafio 14 Dias IA",
    navSub: "A IA que trabalha 14 dias por você para posicionar sua marca no topo",
    navLinkVideo: "🎥 Vídeo (40s)",
    navLinkChallenge: "🔥 O Desafio de 14 Dias",
    navLinkHow: "Como Funciona",
    navLinkDir: "Diretório Oficial",
    navDemoBtn: "📊 Ver Evolução 14 Dias",
    navCtaBtn: "Teste Gratuito (10s) ↓",

    heroBadgePill: "Desafio Guiado de 14 Dias",
    heroBadgeDesc: "Nossa IA trabalha 14 dias consecutivos por você para colocar seu nome no topo das pesquisas de IA",
    heroHeadline: 'Se um cliente abrir o <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">ChatGPT agora</span> na sua cidade, quem a IA recomenda?',
    heroParagraph: "Descubra sua nota gratuitamente em <strong>10 segundos</strong>. E se você estiver invisível, ative nosso <strong>Desafio de 14 Dias</strong>: nossa Inteligência Artificial assume o trabalho pesado e executa <strong>14 ações técnicas diárias</strong> para fazer sua empresa ou nome profissional subir no ranking do ChatGPT, Gemini e Perplexity.",
    heroVideoTitle: "🎥 Apresentação Oficial GeoPulse AI (0:40s)",

    simBtnDay0: "Dia 0 (Hoje)",
    simBtnDay14: "Dia 14 (Pós-IA)",
    simExplainTitle: "💡 Pelo que você está pagando no Desafio (R$ 197 único):",
    simExplainDesc: "Durante <strong>14 dias seguidos</strong>, nossa IA executa 1 etapa técnica por dia (cria seus arquivos semânticos, publica artigos comparativos, envia pings aos robôs e reaudita sua nota) para colocar você no topo das pesquisas feitas por IA.",

    step1Badge: "👇 Passo 1 (Gratuito): Descubra sua Nota Atual em 10 Segundos",
    formMainTitle: "Auditoria Gratuita de Visibilidade em IA",
    btnPresetAdv: "⚖️ Exemplo Advogado",
    btnPresetClinica: "🦷 Exemplo Clínica",
    btnDemoSim: "⚡ Simular Diagnóstico Agora",

    btnTypeCompany: "🏢 Sou Empresa / Clínica / Escritório",
    btnTypeAuto: "👨‍⚕️ Sou Profissional Liberal / Autônomo",

    formCompany: {
      nameLabel: "🏢 Nome da Empresa, Clínica ou Marca *",
      namePlaceholder: "Ex: Clínica OdontoPrime ou Silva & Associados",
      urlLabel: "🌐 Site Oficial ou Instagram da Empresa *",
      urlPlaceholder: "Ex: www.suaempresa.com.br ou @suaempresa",
      nicheLabel: "🎯 Especialidade ou Ramo de Atuação da Empresa *",
      nichePlaceholder: "Ex: Implantes Dentários, Advocacia Empresarial, Contabilidade",
      cityLabel: "📍 Cidade e Estado da Empresa *",
      cityPlaceholder: "Ex: São Paulo - SP, Belo Horizonte - MG",
      registryLabel: "🏛️ CNPJ ou Registro Oficial da Empresa (Opcional)",
      registryPlaceholder: "Ex: 00.000.000/0001-00 ou Registro em Conselho",
      registryHint: "Ajuda os robôs de IA a confirmarem a legitimidade da sua empresa.",
      competitorsLabel: "⚔️ Concorrentes Diretos na Região (Opcional)",
      competitorsPlaceholder: "Ex: Concorrente 1, Concorrente 2",
      competitorsHint: "A IA compara sua empresa contra eles nas recomendações de busca."
    },

    formAuto: {
      nameLabel: "👨‍⚕️ Seu Nome Profissional Completo *",
      namePlaceholder: "Ex: Dr. Roberto Guimarães ou Dra. Camila Mendes",
      urlLabel: "🌐 Seu Perfil no Instagram, Site ou LinkedIn *",
      urlPlaceholder: "Ex: instagram.com/dr.roberto ou www.drroberto.com.br",
      nicheLabel: "🎯 Sua Especialidade ou Área de Atuação *",
      nichePlaceholder: "Ex: Advogado Trabalhista, Médico Cirurgião, Dentista, Psicóloga",
      cityLabel: "📍 Cidade e Estado onde você Atende *",
      cityPlaceholder: "Ex: São Paulo - SP, Rio de Janeiro - RJ",
      registryLabel: "📜 Seu Registro Profissional (OAB, CRM, CRO, CREA, CRP, CRC, etc.) *",
      registryPlaceholder: "Ex: OAB/SP 123.456, CRM 98.765, CRO 12.345",
      registryHint: "Essencial para o ChatGPT e Gemini recomendarem seu nome com autoridade e credibilidade máxima.",
      competitorsLabel: "⚔️ Outros Profissionais Concorrentes na Região (Opcional)",
      competitorsPlaceholder: "Ex: Dr. Concorrente X, Dra. Concorrente Y",
      competitorsHint: "A IA compara você diretamente com outros profissionais da mesma cidade."
    },

    submitBtn: "🚀 Executar Diagnóstico Gratuito nas IAs Agora",
    submitBtnLoading: "⏳ Auditando nos motores de IA...",

    lossBadge: "Impacto Comercial Direto",
    lossMonthlyLbl: "Perda Mensal Estimada",
    lossSubMonthlyLbl: "/ mês para concorrentes",
    lossTicketSimTitle: "Simule com o seu Ticket Médio Real:",
    lossTicketSimSub: "Arraste para ajustar quanto em média um cliente gasta com você:",
    lossTicketSimBadge: "Ticket Selecionado:",

    guarBadge: "Risco Zero Absoluto • Proteção ao Consumidor",
    guarTitle: "Garantia Incondicional de 7 Dias: Devolução de 100%",
    guarDesc: "Confiamos tanto na eficácia da nossa tecnologia de engenharia semântica que assumimos todo o risco: se em até <strong>7 dias</strong> após a contratação sua estrutura GEO, seu arquivo <code>/llms.txt</code> e seu Guia Oficial Top 5 não forem publicados e entregues no servidor, basta nos enviar uma única mensagem e <strong>devolvemos 100% do seu valor via PIX na mesma hora</strong>, sem perguntas e sem letras miúdas.",

    faqBadge: "Tire suas Dúvidas",
    faqTitle: "Perguntas Frequentes sobre o Desafio",
    faqSub: "Tudo o que você precisa saber antes de ativar a autoridade da sua marca na IA.",

    faqs: [
      {
        q: "📱 Não tenho site oficial, uso apenas o Instagram ou WhatsApp. Funciona para mim?",
        a: "<strong>Sim, 100%!</strong> O GeoPulse AI gera e hospeda externamente sua página oficial de autoridade (com dados estruturados Schema.org JSON-LD e o arquivo canônico <code>/llms.txt</code>) dentro do domínio indexado <code>geopulseai.store</code>. O seu perfil do Instagram, WhatsApp ou LinkedIn é cadastrado como o canal oficial de contato para onde a IA direcionará os clientes recomendados."
      },
      {
        q: "💻 Preciso entender de programação ou contratar um programador?",
        a: "<strong>Absolutamente nada!</strong> O trabalho técnico complexo (geração de grafos semânticos, redação dos artigos Top 5, pings para robôs via IndexNow e auditorias nos modelos generativos) é executado de forma 100% autônoma pelo nosso motor no servidor. Você só acompanha o diário de bordo."
      },
      {
        q: "💳 O valor de R$ 197 é uma taxa única ou existe mensalidade escondida?",
        a: "<strong>Taxa única promocional de R$ 197,00.</strong> Não existe nenhuma mensalidade, assinatura ou taxa recorrente surpresa. O valor cobre os 14 dias de execuções ativas do motor de IA e garante a permanência vitalícia dos seus ativos gerados no nosso diretório público indexado."
      },
      {
        q: "🤖 Quanto tempo leva para os robôs do ChatGPT, Gemini e Google lerem minha página?",
        a: "No momento da ativação, nosso sistema emite o ping oficial do protocolo <strong>IndexNow</strong> (validado pelo Bing, Yandex e pelo mecanismo de busca em tempo real do ChatGPT). Enquanto os métodos tradicionais de SEO demoram até 6 meses, a indexação de autoridade em IA costuma ser rastreada entre algumas horas e poucos dias."
      },
      {
        q: "🛡️ O que acontece se eu não gostar dos resultados?",
        a: "Você está 100% seguro pela nossa <strong>Garantia Blindada de 7 Dias</strong>. Se por qualquer motivo você não ficar plenamente satisfeito com a entrega técnica da sua autoridade, devolvemos 100% do valor pago via PIX imediatamente."
      }
    ],

    checkout: {
      badge: "🚀 Desafio Sprint de 14 Dias IA",
      title: "Ativar 14 Dias de Trabalho da IA",
      desc: "Investimento em <strong>taxa única</strong> (sem mensalidades). Inclui os 14 dias de engenharia semântica + 7 ativos vitais + publicação do Guia Oficial Top 5.",
      bumpTitle: "SIM! Adicionar Pacote Expansão Regional",
      bumpBadge: "+ R$ 50,00",
      bumpDesc: "Blindagem semântica em até <strong>3 cidades vizinhas</strong> da sua região + Kit com <strong>Bio de Alta Conversão & 5 Posts de Autoridade IA</strong> para Instagram e LinkedIn.",
      totalLabel: "Total a Pagar (Taxa Única):",
      mpBtn: "💳 Pagar com Mercado Pago (PIX ou Cartão em até 12x)",
      pixTitle: "PIX Instantâneo Oficial (Banco Central):",
      pixScanPill: "Escaneie no App do Banco",
      pixScanDesc: "Abra o app do seu banco, escolha <strong>PIX</strong> e aponte a câmera para pagar com o valor exato já preenchido.",
      pixCopyBtn: "📋 Copiar PIX Copia e Cola",
      pixKeyDetails: "Ou prefere transferir pela Chave Aleatória simples? Clique aqui",
      pixPaidBtn: "✅ Já fiz o PIX — Iniciar Meu Desafio de 14 Dias"
    },

    chat: {
      header: "Especialista GeoPulse — Online",
      sub: "Tire dúvidas sobre o Desafio 14 Dias",
      inputPlaceholder: "Digite sua dúvida aqui...",
      sendBtn: "Enviar",
      typing: "Digitando resposta...",
      quickHow: "Como funciona o Desafio?",
      quickPrice: "Qual o valor e formas de pagamento?",
      quickSite: "Preciso de site ou programador?",
      quickGuar: "Existe garantia se eu não gostar?"
    }
  },

  en: {
    currencySymbol: "$",
    currencyCode: "USD",
    locale: "en-US",
    planPrice: 47.0,
    bumpPrice: 15.0,
    defaultTicket: 250,
    ticketMin: 50,
    ticketMax: 2000,
    ticketStep: 25,
    ticketScale: ["$50", "$500", "$1,000", "$2,000+"],

    liveBarTitle: "Live 14-Day AI Engine:",
    marquee: [
      "⚙️ <strong>Day 14/14 Completed:</strong> Dr. Henry Vance (NY) climbed from 24% to 94.5% (#1 Rank on ChatGPT Search)",
      "🚀 <strong>Day 2/14 Executed:</strong> Prime Dental Clinic (Austin) got its official Top 5 Guide published automatically by AI",
      "📡 <strong>Day 10/14 Executed:</strong> Atlas Accounting Firm (London) received real-time IndexNow Ping on Bing & Perplexity bots",
      "📈 <strong>Day 7/14 Executed:</strong> Dr. Emily Stone (Miami) reached 78.4% in the Mid-Challenge AI Re-Audit"
    ],

    navBadge: "14-Day AI Challenge",
    navSub: "The AI that works 14 consecutive days for you to rank your brand at the very top",
    navLinkVideo: "🎥 Video (40s)",
    navLinkChallenge: "🔥 The 14-Day Challenge",
    navLinkHow: "How It Works",
    navLinkDir: "Official Directory",
    navDemoBtn: "📊 View 14-Day Evolution",
    navCtaBtn: "Free Test (10s) ↓",

    heroBadgePill: "Guided 14-Day Challenge",
    heroBadgeDesc: "Our AI works 14 consecutive days for you to put your name at the top of AI search rankings",
    heroHeadline: 'If a customer opens <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">ChatGPT right now</span> in your city, who does the AI recommend?',
    heroParagraph: "Discover your visibility score for free in <strong>10 seconds</strong>. And if you are invisible, activate our <strong>14-Day Challenge</strong>: our Artificial Intelligence takes over the heavy lifting and executes <strong>14 daily technical actions</strong> to elevate your brand to the top of ChatGPT, Gemini, and Perplexity.",
    heroVideoTitle: "🎥 Official GeoPulse AI Presentation (0:40s)",

    simBtnDay0: "Day 0 (Today)",
    simBtnDay14: "Day 14 (Post-AI)",
    simExplainTitle: "💡 What you get with the 14-Day Challenge ($47 one-time):",
    simExplainDesc: "For <strong>14 consecutive days</strong>, our AI executes 1 technical action per day (creates semantic schema files, publishes comparative guides, pings search bots, and audits your rank) to place you #1.",

    step1Badge: "👇 Step 1 (Free): Discover Your AI Score in 10 Seconds",
    formMainTitle: "Free AI Visibility & Share of Model Audit",
    btnPresetAdv: "⚖️ Lawyer Example",
    btnPresetClinica: "🦷 Clinic Example",
    btnDemoSim: "⚡ Simulate Diagnostic Now",

    btnTypeCompany: "🏢 Company / Clinic / Agency",
    btnTypeAuto: "👨‍⚕️ Solo Professional / Specialist",

    formCompany: {
      nameLabel: "🏢 Company, Clinic, or Brand Name *",
      namePlaceholder: "Ex: Prime Dental Clinic or Apex Law Partners",
      urlLabel: "🌐 Official Website or Social Profile *",
      urlPlaceholder: "Ex: www.yourcompany.com or @yourcompany",
      nicheLabel: "🎯 Business Specialty or Industry *",
      nichePlaceholder: "Ex: Cosmetic Dentistry, Corporate Law, Cloud Accounting",
      cityLabel: "📍 City and State / Region *",
      cityPlaceholder: "Ex: New York - NY, London - UK, Miami - FL",
      registryLabel: "🏛️ Official Registration or Company Tax ID (Optional)",
      registryPlaceholder: "Ex: State License, Chamber of Commerce ID",
      registryHint: "Helps AI models verify the authenticity and legitimacy of your business.",
      competitorsLabel: "⚔️ Direct Competitors in your Area (Optional)",
      competitorsPlaceholder: "Ex: Competitor 1, Competitor 2",
      competitorsHint: "AI models compare your business directly against them in recommendation prompts."
    },

    formAuto: {
      nameLabel: "👨‍⚕️ Your Full Professional Name *",
      namePlaceholder: "Ex: Dr. Robert Vance or Dr. Emily Stone",
      urlLabel: "🌐 Your Website, LinkedIn, or Profile URL *",
      urlPlaceholder: "Ex: linkedin.com/in/drrobert or www.drrobert.com",
      nicheLabel: "🎯 Your Specialty or Field of Practice *",
      nichePlaceholder: "Ex: Employment Attorney, Orthopedic Surgeon, Psychologist",
      cityLabel: "📍 City and Region where you practice *",
      cityPlaceholder: "Ex: New York - NY, Los Angeles - CA, London",
      registryLabel: "📜 Professional Board License (Bar, Medical Board, etc.) *",
      registryPlaceholder: "Ex: State Bar #123456, Medical License #98765",
      registryHint: "Crucial for ChatGPT and Gemini to cite your name with maximum authority and trustworthiness.",
      competitorsLabel: "⚔️ Other Competing Specialists in your Area (Optional)",
      competitorsPlaceholder: "Ex: Dr. Competitor X, Dr. Competitor Y",
      competitorsHint: "The AI compares you directly with other local practitioners."
    },

    submitBtn: "🚀 Run Free AI Diagnostic Now",
    submitBtnLoading: "⏳ Auditing across AI engines...",

    lossBadge: "Direct Commercial Impact",
    lossMonthlyLbl: "Estimated Monthly Loss",
    lossSubMonthlyLbl: "/ mo to competitors",
    lossTicketSimTitle: "Simulate with your Real Average Ticket:",
    lossTicketSimSub: "Drag to adjust how much an average customer spends with you:",
    lossTicketSimBadge: "Selected Ticket:",

    guarBadge: "Absolute Zero Risk • 100% Protection",
    guarTitle: "7-Day Unconditional Guarantee: 100% Refund",
    guarDesc: "We are so confident in our semantic engineering technology that we take all the risk: if within <strong>7 days</strong> of activation your GEO structure, your <code>/llms.txt</code> file, and your official Top 5 Authority Guide are not published and live on the web, simply send us a message and <strong>we will refund 100% of your money immediately</strong>, no questions asked.",

    faqBadge: "Got Questions?",
    faqTitle: "Frequently Asked Questions about the Challenge",
    faqSub: "Everything you need to know before putting your brand on top of AI search engines.",

    faqs: [
      {
        q: "📱 I don't have a formal website, only LinkedIn or Instagram. Does it work for me?",
        a: "<strong>Yes, 100%!</strong> GeoPulse AI generates and hosts your official authority page (with Schema.org JSON-LD data and the canonical <code>/llms.txt</code> file) on our indexed domain <code>geopulseai.store</code>. Your LinkedIn, Instagram, or booking link is registered as the official destination where AI models send new clients."
      },
      {
        q: "💻 Do I need coding skills or need to hire a developer?",
        a: "<strong>Not at all!</strong> The complex technical work (semantic entity graphs, Top 5 authority articles, IndexNow robot pings, and LLM probes) is executed 100% autonomously by our cloud engine. You simply monitor the 14-day progress log."
      },
      {
        q: "💳 Is the $47 fee a one-time payment or are there hidden monthly subscriptions?",
        a: "<strong>One-time promotional fee of $47.00 USD.</strong> There are zero recurring subscriptions, monthly fees, or hidden costs. It covers all 14 days of automated AI engine actions and guarantees lifetime placement in our public indexed directory."
      },
      {
        q: "🤖 How long does it take for ChatGPT, Gemini, and search bots to read my page?",
        a: "Upon activation, our system triggers the official <strong>IndexNow protocol</strong> (used by Bing, Yandex, and real-time ChatGPT Search crawlers). While traditional SEO takes 6+ months, AI authority indexing is typically crawled within hours to a few days."
      },
      {
        q: "🛡️ What happens if I am not satisfied with the results?",
        a: "You are fully protected by our <strong>7-Day Ironclad Guarantee</strong>. If for any reason you are not completely satisfied with your technical delivery, we issue a 100% instant refund without hassle."
      }
    ],

    checkout: {
      badge: "🚀 14-Day AI Sprint Challenge",
      title: "Activate 14 Days of Autonomous AI Work",
      desc: "One-time investment (no subscriptions). Includes 14 days of semantic engineering + 7 vital authority assets + live publication of your official Top 5 Guide.",
      bumpTitle: "YES! Add Regional Expansion Package",
      bumpBadge: "+ $15.00 USD",
      bumpDesc: "Semantic shielding across up to <strong>3 neighboring cities</strong> in your region + High-Conversion <strong>Bio & 5 Authority AI Posts Kit</strong> for LinkedIn and Instagram.",
      totalLabel: "Total Amount (One-Time Fee):",
      mpBtn: "💳 Pay with Credit or Debit Card ($47.00 USD)",
      pixTitle: "International / Alternative Payment:",
      pixScanPill: "Secure Global Checkout",
      pixScanDesc: "Instant automated delivery upon completion. Encrypted 256-bit SSL transaction.",
      pixCopyBtn: "📋 Copy Checkout Reference",
      pixKeyDetails: "Are you from Brazil and prefer Central Bank PIX? Click here",
      pixPaidBtn: "✅ Payment Completed — Start My 14-Day Challenge"
    },

    chat: {
      header: "GeoPulse Specialist — Online",
      sub: "Ask any question about the 14-Day AI Sprint",
      inputPlaceholder: "Type your question here...",
      sendBtn: "Send",
      typing: "Typing response...",
      quickHow: "How does the Challenge work?",
      quickPrice: "What is the price and payment options?",
      quickSite: "Do I need a website or developer?",
      quickGuar: "Is there a money-back guarantee?"
    }
  },

  es: {
    currencySymbol: "$",
    currencyCode: "USD",
    locale: "es-ES",
    planPrice: 47.0,
    bumpPrice: 15.0,
    defaultTicket: 250,
    ticketMin: 50,
    ticketMax: 2000,
    ticketStep: 25,
    ticketScale: ["$50", "$500", "$1.000", "$2.000+"],

    liveBarTitle: "Motor 14 Días en Vivo:",
    marquee: [
      "⚙️ <strong>Día 14/14 Concluido:</strong> Dr. Enrique Vasconcelos (Madrid) subió del 24% al 94.5% (1º Lugar en ChatGPT Search)",
      "🚀 <strong>Día 2/14 Ejecutado:</strong> Clínica OdontoPrime (Bogotá) tuvo su Guía Oficial Top 5 publicada automáticamente por la IA",
      "📡 <strong>Día 10/14 Ejecutado:</strong> Estudio Contable Atlas (Buenos Aires) recibió Ping IndexNow en Bing y Perplexity",
      "📈 <strong>Día 7/14 Ejecutado:</strong> Dra. Camila Méndez (CDMX) alcanzó el 78.4% en la Reauditoría Intermedia del Desafío"
    ],

    navBadge: "Desafío 14 Días IA",
    navSub: "La IA que trabaja 14 días consecutivos por ti para posicionar tu marca en la cima",
    navLinkVideo: "🎥 Video (40s)",
    navLinkChallenge: "🔥 El Desafío de 14 Días",
    navLinkHow: "Cómo Funciona",
    navLinkDir: "Directorio Oficial",
    navDemoBtn: "📊 Ver Evolución 14 Días",
    navCtaBtn: "Prueba Gratis (10s) ↓",

    heroBadgePill: "Desafío Guiado de 14 Días",
    heroBadgeDesc: "Nuestra IA trabaja 14 días consecutivos por ti para colocar tu nombre en la cima de las búsquedas con IA",
    heroHeadline: 'Si un cliente abre <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">ChatGPT ahora</span> en tu ciudad, ¿a quién recomienda la IA?',
    heroParagraph: "Descubre tu puntuación de visibilidad gratis en <strong>10 segundos</strong>. Y si eres invisible, activa nuestro <strong>Desafío de 14 Días</strong>: nuestra Inteligencia Artificial asume el trabajo pesado y ejecuta <strong>14 acciones técnicas diarias</strong> para elevar tu marca a la cima de ChatGPT, Gemini y Perplexity.",
    heroVideoTitle: "🎥 Presentación Oficial GeoPulse AI (0:40s)",

    simBtnDay0: "Día 0 (Hoy)",
    simBtnDay14: "Día 14 (Con IA)",
    simExplainTitle: "💡 Lo que obtienes con el Desafío ($47 tarifa única):",
    simExplainDesc: "Durante <strong>14 días consecutivos</strong>, nuestra IA ejecuta 1 acción técnica por día (crea archivos semánticos, publica guías comparativas, envía pings a los robots y audita tu posición) para colocarte en el 1º lugar.",

    step1Badge: "👇 Paso 1 (Gratis): Descubre tu Puntuación en 10 Segundos",
    formMainTitle: "Auditoría Gratuita de Visibilidad en IA",
    btnPresetAdv: "⚖️ Ejemplo Abogado",
    btnPresetClinica: "🦷 Ejemplo Clínica",
    btnDemoSim: "⚡ Simular Diagnóstico Ahora",

    btnTypeCompany: "🏢 Empresa / Clínica / Negocio",
    btnTypeAuto: "👨‍⚕️ Profesional Independiente",

    formCompany: {
      nameLabel: "🏢 Nombre de la Empresa, Clínica o Marca *",
      namePlaceholder: "Ej: Clínica OdontoPrime o Bufete Gómez & Asociados",
      urlLabel: "🌐 Sitio Web Oficial o Perfil de Redes *",
      urlPlaceholder: "Ej: www.tuempresa.com o @tuempresa",
      nicheLabel: "🎯 Especialidad o Sector de Actividad *",
      nichePlaceholder: "Ej: Implantes Dentales, Abogados Laborales, Contabilidad",
      cityLabel: "📍 Ciudad y Región de la Empresa *",
      cityPlaceholder: "Ej: Madrid, Ciudad de México, Bogotá, Buenos Aires",
      registryLabel: "🏛️ Registro Fiscal o Licencia Oficial (Opcional)",
      registryPlaceholder: "Ej: NIF, CIF, RFC o Registro Comercial",
      registryHint: "Ayuda a los motores de IA a verificar la legitimidad oficial de tu negocio.",
      competitorsLabel: "⚔️ Competidores Directos en tu Zona (Opcional)",
      competitorsPlaceholder: "Ej: Competidor 1, Competidor 2",
      competitorsHint: "La IA compara tu empresa directamente frente a ellos en sus recomendaciones."
    },

    formAuto: {
      nameLabel: "👨‍⚕️ Tu Nombre Profesional Completo *",
      namePlaceholder: "Ej: Dr. Roberto Guimarães o Dra. Camila Méndez",
      urlLabel: "🌐 Tu Sitio Web, LinkedIn o Instagram Profesional *",
      urlPlaceholder: "Ej: linkedin.com/in/drroberto o www.drroberto.com",
      nicheLabel: "🎯 Tu Especialidad o Campo Profesional *",
      nichePlaceholder: "Ej: Abogado Laboral, Cirujano, Odontólogo, Psicóloga",
      cityLabel: "📍 Ciudad y Región donde atiendes *",
      cityPlaceholder: "Ej: Madrid, Ciudad de México, Bogotá, Santiago",
      registryLabel: "📜 Número de Colegiatura o Registro Profesional *",
      registryPlaceholder: "Ej: Colegiado #12345, Cédula Profesional #98765",
      registryHint: "Fundamental para que ChatGPT y Gemini recomienden tu nombre con máxima autoridad y credibilidad.",
      competitorsLabel: "⚔️ Otros Profesionales Colegas en la Región (Opcional)",
      competitorsPlaceholder: "Ej: Dr. Competidor X, Dra. Competidor Y",
      competitorsHint: "La IA te compara directamente con otros profesionales de tu misma ciudad."
    },

    submitBtn: "🚀 Ejecutar Diagnóstico Gratuito en IAs Ahora",
    submitBtnLoading: "⏳ Auditando en motores de IA...",

    lossBadge: "Impacto Comercial Directo",
    lossMonthlyLbl: "Pérdida Mensual Estimada",
    lossSubMonthlyLbl: "/ mes para competidores",
    lossTicketSimTitle: "Simula con tu Ticket Medio Real:",
    lossTicketSimSub: "Desliza para ajustar cuánto gasta en promedio un cliente contigo:",
    lossTicketSimBadge: "Ticket Seleccionado:",

    guarBadge: "Riesgo Cero Absoluto • Protección Total",
    guarTitle: "Garantía Incondicional de 7 Días: Devolución del 100%",
    guarDesc: "Confiamos tanto en la eficacia de nuestra tecnología semántica que asumimos todo el riesgo: si dentro de los <strong>7 días</strong> posteriores a la contratación tu estructura GEO, tu archivo <code>/llms.txt</code> y tu Guía Oficial Top 5 no están publicados en la web, solo envíanos un mensaje y <strong>te reembolsamos el 100% de inmediato</strong>, sin preguntas ni letra pequeña.",

    faqBadge: "Resuelve tus Dudas",
    faqTitle: "Preguntas Frecuentes sobre el Desafío",
    faqSub: "Todo lo que necesitas saber antes de activar la autoridad de tu marca en IA.",

    faqs: [
      {
        q: "📱 No tengo sitio web oficial, solo uso Instagram o WhatsApp. ¿Funciona para mí?",
        a: "<strong>¡Sí, al 100%!</strong> GeoPulse AI genera y aloja externamente tu página oficial de autoridad (con Schema.org JSON-LD y el archivo canónico <code>/llms.txt</code>) en nuestro dominio indexado <code>geopulseai.store</code>. Tu perfil de Instagram, WhatsApp o LinkedIn se registra como el canal de contacto al que la IA enviará a los clientes."
      },
      {
        q: "💻 ¿Necesito conocimientos de programación o contratar a un programador?",
        a: "<strong>¡Absolutamente nada!</strong> El trabajo técnico complejo (grafos de entidad, redacción de artículos Top 5, pings a robots con IndexNow y auditorías generativas) se ejecuta de forma 100% autónoma en nuestro servidor. Tú solo sigues el diario de a bordo."
      },
      {
        q: "💳 ¿El valor de $47 es un pago único o hay cuotas mensuales?",
        a: "<strong>Tarifa única promocional de $47.00 USD.</strong> No existe ninguna suscripción ni cuotas mensuales recurrentes. Cubre los 14 días de ejecuciones de IA y garantiza la permanencia de por vida de tus activos generados en nuestro directorio indexado."
      },
      {
        q: "🤖 ¿Cuánto tardan los robots de ChatGPT, Gemini y Google en leer mi página?",
        a: "Al momento de la activación, nuestro sistema emite el ping oficial del protocolo <strong>IndexNow</strong> (validado por Bing y el buscador en tiempo real de ChatGPT). Mientras que el SEO tradicional tarda hasta 6 meses, la indexación de IA suele completarse entre unas horas y pocos días."
      },
      {
        q: "🛡️ ¿Qué pasa si no estoy conforme con los resultados?",
        a: "Estás 100% protegido por nuestra <strong>Garantía Blindada de 7 Días</strong>. Si por cualquier motivo no quedas totalmente satisfecho con la entrega técnica, te devolvemos el 100% de tu dinero de inmediato."
      }
    ],

    checkout: {
      badge: "🚀 Desafío Sprint de 14 Días IA",
      title: "Activar 14 Días de Trabajo Autónomo de la IA",
      desc: "Inversión en <strong>tarifa única</strong> (sin suscripciones). Incluye 14 días de ingeniería semántica + 7 activos vitales + publicación de tu Guía Oficial Top 5.",
      bumpTitle: "¡SÍ! Agregar Paquete de Expansión Regional",
      bumpBadge: "+ $15.00 USD",
      bumpDesc: "Blindaje semántico en hasta <strong>3 ciudades vecinas</strong> de tu región + Kit con <strong>Bio de Alta Conversión y 5 Posts de Autoridad IA</strong> para redes sociales.",
      totalLabel: "Total a Pagar (Tarifa Única):",
      mpBtn: "💳 Pagar con Tarjeta de Crédito o Débito ($47.00 USD)",
      pixTitle: "Pago Internacional Seguro:",
      pixScanPill: "Pasarela Segura Global",
      pixScanDesc: "Activación automática inmediata. Transacción cifrada con protocolo SSL de 256 bits.",
      pixCopyBtn: "📋 Copiar Referencia de Pago",
      pixKeyDetails: "¿Estás en Brasil y prefieres pagar con PIX? Haz clic aquí",
      pixPaidBtn: "✅ Pago Realizado — Iniciar Mi Desafío de 14 Días"
    },

    chat: {
      header: "Especialista GeoPulse — En Línea",
      sub: "Resuelve tus dudas sobre el Desafío de 14 Días",
      inputPlaceholder: "Escribe tu consulta aquí...",
      sendBtn: "Enviar",
      typing: "Escribiendo respuesta...",
      quickHow: "¿Cómo funciona el Desafío?",
      quickPrice: "¿Cuál es el precio y formas de pago?",
      quickSite: "¿Necesito sitio web o programador?",
      quickGuar: "¿Tengo garantía si no me convence?"
    }
  }
};

let currentLang = "pt";

/**
 * Detecta automaticamente o idioma do visitante:
 * 1. Preferência salva no localStorage
 * 2. Idioma do navegador/sistema (navigator.languages / navigator.language)
 * 3. Fuso horário como heurística geográfica adicional
 * 4. Fallback padrão: 'en' para tráfego internacional geral
 */
function detectLanguage() {
  try {
    const saved = localStorage.getItem("geopulse_lang");
    if (saved && ["pt", "en", "es"].includes(saved)) {
      return saved;
    }

    const browserLangs = navigator.languages || [navigator.language || navigator.userLanguage || ""];
    for (const raw of browserLangs) {
      const l = (raw || "").toLowerCase();
      if (l.startsWith("pt")) return "pt";
      if (l.startsWith("es")) return "es";
      if (l.startsWith("en")) return "en";
    }

    const tz = (Intl.DateTimeFormat().resolvedOptions().timeZone || "").toLowerCase();
    if (/sao_paulo|lisbon|fortaleza|recife|manaus|cuiaba|belem/i.test(tz)) return "pt";
    if (/madrid|mexico|bogota|buenos_aires|santiago|lima|caracas|montevideo|asuncion|havana/i.test(tz)) return "es";
  } catch (e) {
    console.warn("Language detection fallback:", e);
  }
  return "en";
}

/**
 * Altera o idioma da página e atualiza os elementos visuais
 */
function setLanguage(lang) {
  if (!["pt", "en", "es"].includes(lang)) lang = "pt";
  currentLang = lang;
  try {
    localStorage.setItem("geopulse_lang", lang);
  } catch (e) {}

  // Atualiza visual dos botões do seletor
  ["pt", "en", "es"].forEach((l) => {
    const btn = document.getElementById(`lang-btn-${l}`);
    if (btn) {
      if (l === lang) {
        btn.className = "px-2 py-1 rounded-lg text-xs font-extrabold transition flex items-center gap-1 bg-white shadow-sm text-slate-900";
      } else {
        btn.className = "px-2 py-1 rounded-lg text-xs font-extrabold transition flex items-center gap-1 text-slate-500 hover:text-slate-900";
      }
    }
  });

  applyLanguage(lang);
}

/**
 * Aplica os textos traduzidos a todos os elementos da página
 */
function applyLanguage(lang) {
  const dict = I18N[lang] || I18N.pt;

  // Atualiza título da aba e meta description
  if (lang === "en") {
    document.title = "GeoPulse AI — 14-Day Challenge: Our AI Working Daily to Rank You #1 on ChatGPT & Gemini";
  } else if (lang === "es") {
    document.title = "GeoPulse AI — Desafío de 14 Días: Nuestra IA Trabajando para Colocarte en 1º Lugar en ChatGPT y Gemini";
  } else {
    document.title = "GeoPulse AI — Desafio de 14 Dias: Nossa IA Trabalhando para Colocar Você em 1º Lugar no ChatGPT e Gemini";
  }

  // Marquee superior
  const barTitle = document.getElementById("live-bar-title");
  if (barTitle) barTitle.textContent = dict.liveBarTitle;

  const marqueeTrack = document.getElementById("live-marquee-track");
  if (marqueeTrack && dict.marquee) {
    marqueeTrack.innerHTML = dict.marquee.map((m) => `<span>${m}</span>`).join("");
  }

  // Navbar
  const navBadge = document.getElementById("nav-badge-text");
  if (navBadge) navBadge.textContent = dict.navBadge;

  const navSub = document.getElementById("nav-sub-text");
  if (navSub) navSub.textContent = dict.navSub;

  const navVideo = document.getElementById("nav-link-video");
  if (navVideo) navVideo.textContent = dict.navLinkVideo;

  const navChallenge = document.getElementById("nav-link-challenge");
  if (navChallenge) navChallenge.textContent = dict.navLinkChallenge;

  const navHow = document.getElementById("nav-link-how");
  if (navHow) navHow.textContent = dict.navLinkHow;

  const navDir = document.getElementById("nav-link-dir");
  if (navDir) navDir.textContent = dict.navLinkDir;

  const navDemo = document.getElementById("nav-demo-btn");
  if (navDemo) navDemo.textContent = dict.navDemoBtn;

  const navCta = document.getElementById("nav-cta-btn");
  if (navCta) navCta.textContent = dict.navCtaBtn;

  // Hero Section
  const heroBadgePill = document.getElementById("hero-badge-pill");
  if (heroBadgePill) heroBadgePill.textContent = dict.heroBadgePill;

  const heroBadgeDesc = document.getElementById("hero-badge-desc");
  if (heroBadgeDesc) heroBadgeDesc.textContent = dict.heroBadgeDesc;

  const heroHeadline = document.getElementById("hero-headline");
  if (heroHeadline) heroHeadline.innerHTML = dict.heroHeadline;

  const heroParagraph = document.getElementById("hero-paragraph");
  if (heroParagraph) heroParagraph.innerHTML = dict.heroParagraph;

  const heroVideoTitle = document.getElementById("hero-video-title");
  if (heroVideoTitle) heroVideoTitle.textContent = dict.heroVideoTitle;

  // Simulator
  const simBtn0 = document.getElementById("hero-sim-before-btn");
  if (simBtn0) simBtn0.textContent = dict.simBtnDay0;

  const simBtn14 = document.getElementById("hero-sim-after-btn");
  if (simBtn14) simBtn14.textContent = dict.simBtnDay14;

  const simExpTitle = document.getElementById("sim-explain-title");
  if (simExpTitle) simExpTitle.innerHTML = dict.simExplainTitle;

  const simExpDesc = document.getElementById("sim-explain-desc");
  if (simExpDesc) simExpDesc.innerHTML = dict.simExplainDesc;

  // Formulário
  const step1 = document.getElementById("step1-badge");
  if (step1) step1.textContent = dict.step1Badge;

  const formTitle = document.getElementById("form-main-title");
  if (formTitle) formTitle.textContent = dict.formMainTitle;

  const btnAdv = document.getElementById("btn-preset-adv");
  if (btnAdv) btnAdv.textContent = dict.btnPresetAdv;

  const btnClinica = document.getElementById("btn-preset-clinica");
  if (btnClinica) btnClinica.textContent = dict.btnPresetClinica;

  const btnSim = document.getElementById("btn-demo-sim");
  if (btnSim) btnSim.textContent = dict.btnDemoSim;

  const btnComp = document.getElementById("btn-type-company");
  if (btnComp) btnComp.innerHTML = `<span>🏢</span> ${dict.btnTypeCompany.replace("🏢 ", "")}`;

  const btnAuto = document.getElementById("btn-type-autonomous");
  if (btnAuto) btnAuto.innerHTML = `<span>👨‍⚕️</span> ${dict.btnTypeAuto.replace("👨‍⚕️ ", "")}`;

  const submitBtn = document.getElementById("submit-audit-btn");
  if (submitBtn) submitBtn.textContent = dict.submitBtn;

  // Atualiza labels dos campos de acordo com a entidade atual
  const currentEntity = document.getElementById("entity_type")?.value || "company";
  if (typeof window.applyEntityLabelsI18n === "function") {
    window.applyEntityLabelsI18n(currentEntity, dict);
  }

  // Calculadora de perda financeira e ticket
  const lossMonthLbl = document.getElementById("loss-title-monthly-lbl");
  if (lossMonthLbl) lossMonthLbl.textContent = dict.lossMonthlyLbl;

  const lossSubMonthLbl = document.getElementById("loss-sub-monthly-lbl");
  if (lossSubMonthLbl) lossSubMonthLbl.textContent = dict.lossSubMonthlyLbl;

  const lossSimTitle = document.getElementById("loss-ticket-sim-title");
  if (lossSimTitle) lossSimTitle.textContent = dict.lossTicketSimTitle;

  const lossSimSub = document.getElementById("loss-ticket-sim-sub");
  if (lossSimSub) lossSimSub.textContent = dict.lossTicketSimSub;

  const lossSimBadge = document.getElementById("loss-ticket-sim-badge");
  if (lossSimBadge) lossSimBadge.textContent = dict.lossTicketSimBadge;

  // Atualiza slider da calculadora
  const slider = document.getElementById("loss-ticket-slider");
  if (slider) {
    slider.min = dict.ticketMin;
    slider.max = dict.ticketMax;
    slider.step = dict.ticketStep;
    slider.value = dict.defaultTicket;
  }
  if (typeof window.updateLossCalculation === "function") {
    window.updateLossCalculation(dict.defaultTicket);
  }

  // Garantia 7 Dias
  const guarBadge = document.getElementById("guar-badge-txt");
  if (guarBadge) guarBadge.textContent = dict.guarBadge;

  const guarTitle = document.getElementById("guar-title-txt");
  if (guarTitle) guarTitle.innerHTML = dict.guarTitle;

  const guarDesc = document.getElementById("guar-desc-txt");
  if (guarDesc) guarDesc.innerHTML = dict.guarDesc;

  // FAQ
  const faqBadge = document.getElementById("faq-badge-txt");
  if (faqBadge) faqBadge.textContent = dict.faqBadge;

  const faqTitle = document.getElementById("faq-title-txt");
  if (faqTitle) faqTitle.textContent = dict.faqTitle;

  const faqSub = document.getElementById("faq-sub-txt");
  if (faqSub) faqSub.textContent = dict.faqSub;

  // Atualiza os itens do FAQ
  const faqDetails = document.querySelectorAll("#garantia-faq details");
  if (faqDetails && dict.faqs) {
    faqDetails.forEach((elem, idx) => {
      if (dict.faqs[idx]) {
        const summary = elem.querySelector("summary span:first-child");
        if (summary) summary.textContent = dict.faqs[idx].q;
        const p = elem.querySelector("p");
        if (p) p.innerHTML = dict.faqs[idx].a;
      }
    });
  }

  // Chat Flutuante
  const chatInput = document.getElementById("ai-chat-input");
  if (chatInput) chatInput.placeholder = dict.chat.inputPlaceholder;

  // Modal Checkout
  const chBadge = document.getElementById("checkout-badge-pill");
  if (chBadge) chBadge.textContent = dict.checkout.badge;

  const chTitle = document.getElementById("checkout-title-h3");
  if (chTitle) chTitle.textContent = dict.checkout.title;

  const chDesc = document.getElementById("checkout-desc-p");
  if (chDesc) chDesc.innerHTML = dict.checkout.desc;

  const bumpTitle = document.getElementById("order-bump-title-txt");
  if (bumpTitle) bumpTitle.textContent = dict.checkout.bumpTitle;

  const bumpBadge = document.getElementById("order-bump-badge-txt");
  if (bumpBadge) bumpBadge.textContent = dict.checkout.bumpBadge;

  const bumpDesc = document.getElementById("order-bump-desc-txt");
  if (bumpDesc) bumpDesc.innerHTML = dict.checkout.bumpDesc;

  const totalLbl = document.getElementById("checkout-total-lbl");
  if (totalLbl) totalLbl.textContent = dict.checkout.totalLabel;

  const currSym = document.getElementById("checkout-currency-symbol");
  if (currSym) currSym.textContent = dict.currencySymbol;

  const mpBtn = document.getElementById("checkout-mp-btn");
  if (mpBtn) mpBtn.innerHTML = `<span>💳</span> ${dict.checkout.mpBtn.replace("💳 ", "")}`;

  // Se for visitante internacional (en ou es), esconde a obrigatoriedade do PIX brasileiro
  const pixBox = document.getElementById("pix-payment-box");
  if (pixBox) {
    if (lang === "pt") {
      pixBox.style.display = "block";
    } else {
      // Para tráfego global, mantém como opção secundária recolhida
      pixBox.style.display = "block";
    }
  }
  const modalTotal = document.getElementById("modal-total-display");
  if (modalTotal) {
    const isBump = window.currentOrderBump || false;
    const price = dict.planPrice + (isBump ? dict.bumpPrice : 0);
    modalTotal.textContent = dict.currencyCode === "BRL" 
      ? price.toFixed(2).replace(".", ",") 
      : `${price.toFixed(2)} ${dict.currencyCode}`;
  }
}
