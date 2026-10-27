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
    videoHdBadge: "▶ Alta Definição (HD)",
    videoBadge: "Explicação Rápida (40s)",
    videoListen: "🔊 Clique para ouvir",
    videoWatchBtn: "▶ Assistir Apresentação (0:40s)",
    videoQuote: '💬 <em>"Mais de 70% das pessoas pararam de procurar no Google. Agora elas compram o que a IA recomenda direto no chat."</em>',

    // SIMULADOR DO DESAFIO (Imagem do usuário)
    sim: {
      headerBadge: "Simulador do Desafio de 14 Dias",
      headerTitle: "Como sua posição sobe dia após dia",
      btnDay0: "Dia 0 (Hoje)",
      btnDay14: "Dia 14 (Pós-IA)",
      day0Label: "Status no Dia 0 (Sem a IA trabalhar):",
      day0Score: "Score: 21.4%",
      day0Badge: "⚠️ VOCÊ FORA DO RANKING DA IA",
      day0Competitor: "🥇 1. Seu Concorrente Direto — <span class=\"text-emerald-600 font-bold\">Recomendado #1</span>",
      day0YourCompany: "❌ Sua Empresa / Seu Nome",
      day0Invisible: "Invisível no Chat",

      day14Label: "Resultado no Dia 14 (Após 14 ações da IA):",
      day14Score: "Score: 94.5%",
      day14Badge: "🚀 DIA 14: VOCÊ EM 1º LUGAR NAS IAs",
      day14YourCompany: "🥇 1. SUA EMPRESA / SEU NOME — Recomendado #1",

      explainTitle: "💡 Pelo que você está pagando no Desafio (R$ 197 único):",
      explainDesc: "Durante <strong>14 dias seguidos</strong>, nossa IA executa 1 etapa técnica por dia (cria seus arquivos semânticos, publica artigos comparativos, envia pings aos robôs e reaudita sua nota) para colocar você no topo das pesquisas feitas por IA."
    },

    step1Badge: "👇 Passo 1 (Gratuito): Descubra sua Nota Atual em 10 Segundos",
    formMainTitle: "Auditoria Gratuita de Visibilidade em IA",

    presets: {
      adv: "⚖️ Exemplo Advogado",
      clinica: "🦷 Exemplo Clínica",
      demo: "⚡ Simular Diagnóstico Agora"
    },

    entityButtons: {
      company: "Sou Empresa / Clínica / Escritório",
      autonomous: "Sou Profissional Liberal / Autônomo"
    },

    formCompany: {
      nameLabel: "🏢 Nome da Empresa, Clínica ou Marca *",
      namePlaceholder: "Ex: Clínica OdontoPrime ou Silva & Associados",
      urlLabel: "🌐 Site Oficial ou Instagram da Empresa *",
      urlPlaceholder: "Ex: www.suaempresa.com.br ou @suaempresa",
      nicheLabel: "🎯 Especialidade ou Ramo de Atuação *",
      nichePlaceholder: "Ex: Implantes Dentários, Advocacia Trabalhista, Contabilidade",
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
      nameLabel: "👤 Seu Nome Profissional Completo *",
      namePlaceholder: "Ex: Dra. Camila Mendes ou Dr. Rafael Vasconcelos",
      urlLabel: "🌐 Seu Instagram Profissional, LinkedIn ou Site *",
      urlPlaceholder: "Ex: @dr.seunome ou www.seusite.com.br",
      nicheLabel: "🎯 Sua Especialidade de Atuação *",
      nichePlaceholder: "Ex: Dermatologia, Direito Tributário, Psicologia Clínica",
      cityLabel: "📍 Cidade e Estado Onde Você Atende *",
      cityPlaceholder: "Ex: Rio de Janeiro - RJ, Curitiba - PR",
      registryLabel: "📜 Registro de Classe Profissional (CRM, OAB, CRO, CRP, CRC...)",
      registryPlaceholder: "Ex: CRM/SP 123.456 ou OAB/RJ 98.765",
      registryHint: "Fundamental para a IA certificar você como Autoridade Técnica verificada.",
      competitorsLabel: "⚔️ Outros Especialistas que Concorrem com Você (Opcional)",
      competitorsPlaceholder: "Ex: Dr. Fulano, Clínica Tal",
      competitorsHint: "Para a IA comparar sua autoridade contra os nomes já citados."
    },

    contact: {
      whatsapp: "📱 WhatsApp com DDD *",
      whatsappPlaceholder: "Ex: (11) 98765-4321",
      email: "✉️ Seu E-mail para Receber o Relatório",
      emailPlaceholder: "Ex: seuemail@dominio.com.br",
      securityNote: "🔒 Diagnóstico 100% Gratuito em 10 segundos",
      submitBtn: "🔍 Executar Diagnóstico Gratuito nas IAs Agora"
    },

    sprintSection: {
      badge: "Transparência Total: Pelo que você está pagando?",
      title: "Veja o que nossa IA faz por você durante os 14 Dias",
      subtitle: "Você paga uma única vez (R$ 197) e nosso motor executa automaticamente as 14 etapas abaixo para construir sua liderança nas pesquisas feitas por IA:"
    },

    scheduleDayPrefix: "Dia",
    scheduleDayOf: "de",
    scheduleSub: "Executado automaticamente pela IA",
    schedule14: [
      { day: 1, title: "Protocolo de Entidade & JSON-LD + /llms.txt" },
      { day: 2, title: "Publicação do Guia Oficial Top 5 da Cidade" },
      { day: 3, title: "Arquitetura de FAQ Semântico Zero-Click" },
      { day: 4, title: "Ancoragem de Entidade no ChatGPT & Perplexity" },
      { day: 5, title: "Artigo Educativo de Aprofundamento do Nicho" },
      { day: 6, title: "Enriquecimento de Dados Estruturados Schema.org" },
      { day: 7, title: "Reauditoria Intermediária & Ajuste de Densidade" },
      { day: 8, title: "Construção de Página Semântica de Comparativo" },
      { day: 9, title: "Matriz de Prova Social & Casos de Sucesso" },
      { day: 10, title: "Pings IndexNow nos Rastreadores de IA" },
      { day: 11, title: "Artigo de Tendências e Inovações do Setor" },
      { day: 12, title: "Auditoria de Citações e Menções de Terceiros" },
      { day: 13, title: "Consolidação da Base de Conhecimento Local" },
      { day: 14, title: "Relatório Final de Autoridade & Entrega Oficial" }
    ],

    results: {
      statusBadge: "Diagnóstico Concluído (Dia 0)",
      reportTitle: "Relatório de Posicionamento IA",
      shareBtn: "Enviar para o Sócio (WhatsApp)",
      topCta: "🚀 Iniciar Desafio de 14 Dias (IA Trabalhando por Você — R$ 197)",
      metric1Label: "Nota Atual nas IAs (Share of Model)",
      metric1Goal: "Meta após os 14 dias: >90%",
      metric2Label: "Posição Atual no Ranking",
      notRanked: "Fora do Ranking",
      rankSuffix: "º Lugar",
      metric2Sub: "Ranking espontâneo na sua cidade",
      metric3Label: "Status do Desafio de 14 Dias",
      dayPrefix: "Dia",
      metric3Sub: "14 ações diárias prontas para iniciar",
      clientsPerMonth: "clientes / mês",

      lossHeaderBadge: "Alerta de Faturamento: Quanto você está perdendo hoje?",
      lossHeaderTitle: "Estimativa de Negócios e Clientes Perdidos para Concorrentes",
      lossHeaderDescTemplate: "Quando alguém na sua cidade busca recomendação de {niche} no ChatGPT ou Gemini, os algoritmos recomendam seus concorrentes no topo. Veja o cálculo estimado do dinheiro que está deixando de entrar no seu caixa:",
      searchesLabel: "Buscas Locais na IA / Mês",
      searchesSub: "Pessoas pesquisando no ChatGPT e Gemini com alta intenção de contratação na sua cidade.",
      clientsLabel: "Clientes Perdidos / Mês",
      clientsSub: "Clientes que fecham com o concorrente indicado em 1º lugar pela IA.",
      annualLabel: "Prejuízo Anual Projetado",
      annualSub: "Estimativa anual acumulada indo para seus concorrentes diretos.",

      roiBadge: "Cálculo de Retorno",
      roiTitle: "O GeoPulse AI custa apenas <strong>R$ 197 taxa única</strong>",
      roiDesc: "Com <strong>apenas 1 único cliente recuperado</strong> através do ChatGPT ou Gemini, você já recupera com sobras todo o valor do Desafio de 14 Dias e consolida sua liderança na sua região.",
      roiCta: "🛡️ Parar de Perder Clientes e Ativar (R$ 197) →",

      auditsHeading: "🤖 O que o ChatGPT, Gemini e Perplexity responderam:",
      cited: "✓ Citado",
      notCited: "✗ Não Recomendado",
      action14: "✓ Ação nos 14 Dias:",

      sidebarBadge: "🔥 Desafio Sprint de 14 Dias",
      sidebarTitle: "Contrate nossa IA para trabalhar 14 dias seguidos pela sua posição no ranking",
      sidebarDesc: "Por uma <strong>taxa única de R$ 197 (sem mensalidade)</strong>, nossa IA executa 1 ação técnica por dia durante 14 dias (JSON-LD, /llms.txt, Guia Oficial Top 5 da Cidade, FAQ Semântico e Pings IndexNow) para colocar você em 1º lugar.",
      sidebarCta: "Ativar Meu Desafio de 14 Dias Agora (R$ 197) →"
    },

    scarcity: {
      statusBadge: "Status de Exclusividade Regional",
      ruleLabel: "Regra de Ouro da IA:",
      vagaText: "Vaga #1 Oficial em",
      paraText: "para",
      availBadge: "DISPONÍVEL AGORA",
      desc: "Os algoritmos de IA só recomendam <strong>1 único profissional ou empresa no topo #1 do Guia Oficial</strong>. Ao ativar o Desafio de 14 Dias, você assegura a primazia antes que um concorrente local ocupe a indicação canônica.",
      ctaBtn: "Garantir Exclusividade da Vaga #1 →"
    },

    lossBadge: "Impacto Comercial Direto",
    lossMonthlyLbl: "Perda Mensal Estimada",
    lossSubMonthlyLbl: "/ mês para concorrentes",
    lossTicketSimTitle: "Simule com o seu Ticket Médio Real:",
    lossTicketSimSub: "Arraste para ajustar quanto em média um cliente gasta com você:",
    lossTicketSimBadge: "Ticket Selecionado:",

    guarBadge: "Risco Zero Absoluto • Proteção ao Consumidor",
    guarTitle: "Garantia Incondicional de 7 Dias: Devolução de 100%",
    guarDesc: "Confiamos tanto na eficácia da nossa tecnologia de engenharia semântica que assumimos todo o risco: se em até <strong>7 dias</strong> após a contratação sua estrutura GEO, seu arquivo <code>/llms.txt</code> e seu Guia Oficial Top 5 não forem publicados e entregues no servidor, basta nos enviar uma única mensagem e <strong>devolvemos 100% do seu valor via PIX na mesma hora</strong>, sem perguntas e sem letras miúdas.",

    faqBadge: "Tire Suas Dúvidas",
    faqTitle: "Perguntas Frequentes sobre o Desafio",
    faqSub: "Tudo o que você precisa saber antes de iniciar os 14 dias da IA:",
    faqs: [
      {
        q: "💰 O valor de R$ 197 é uma taxa única ou existe mensalidade escondida?",
        a: "<strong>Taxa única promocional de R$ 197,00.</strong> Não existe nenhuma mensalidade, assinatura ou taxa recorrente surpresa. O valor cobre os 14 dias de execuções ativas do motor de IA e garante a permanência vitalícia dos seus ativos gerados no nosso diretório público indexado."
      },
      {
        q: "⚡ Eu preciso fazer alguma coisa técnica ou a IA faz tudo sozinha?",
        a: "<strong>Você não precisa fazer nada técnico.</strong> O GeoPulse foi construído justamente para donos de empresas e profissionais que não entendem de programação nem de SEO avançado. Nossa IA gera o código, constrói os textos semânticos, publica no nosso subdomínio otimizado e dispara os protocolos para o ChatGPT, Perplexity e Gemini."
      },
      {
        q: "🕒 Quanto tempo leva para ver os primeiros resultados no ChatGPT e Gemini?",
        a: "Como o Google, ChatGPT Search e Perplexity atualizam seus índices em ritmos diferentes, a maioria dos clientes começa a ver as primeiras citações e recomendações entre o <strong>7º e o 14º dia</strong> de execução contínua."
      },
      {
        q: "🎯 Por que existe a regra de exclusividade de 1 empresa por nicho/cidade?",
        a: "Porque uma IA generativa só indica <strong>1 resposta de autoridade máxima em primeiro lugar</strong>. Se aceitássemos dois concorrentes diretos no mesmo bairro, estaríamos gerando conflito canônico."
      },
      {
        q: "🛡️ Como funciona a garantia de 7 dias de devolução total?",
        a: "Simples e transparente: se você ativar o desafio e por qualquer motivo não ficar satisfeito com os ativos gerados ou com o progresso técnico da IA, basta nos avisar pelo WhatsApp ou e-mail de suporte dentro de 7 dias."
      }
    ],

    floatingChatPill: "💬 Dúvidas sobre o Desafio? Fale com a IA",

    loading: {
      badge: "Auditoria em Tempo Real",
      title: "Consultando Motores de IA...",
      initSub: "Conectando ao leitor semântico e extraindo dados públicos do seu site/perfil...",
      footer: "Simulando consultas no ChatGPT Search, Gemini e Perplexity",
      btnRunning: "⏳ Auditando nos motores de IA...",
      doneSuccess: "✓ Auditoria concluída com sucesso!",
      doneFinish: "Finalizando...",
      steps: [
        { at: 28, text: "🔍 Lendo metadados técnicos, autoridade e área de atendimento..." },
        { at: 52, text: "🤖 Simulando buscas de clientes no ChatGPT Search, Gemini e Perplexity..." },
        { at: 74, text: "📊 Mapeando concorrentes diretos recomendados pelos algoritmos na região..." },
        { at: 90, text: "💰 Calculando estimativa de clientes e faturamento perdido para terceiros..." },
        { at: 96, text: "✨ Estruturando o relatório oficial de posicionamento..." }
      ]
    },

    chat: {
      title: "Especialista GeoPulse AI",
      online: "Online 24h • Tira-dúvidas",
      welcome: "Olá! Sou a Especialista de IA do GeoPulse. Tem alguma dúvida sobre como funciona o Desafio de 14 Dias ou como colocamos você em 1º Lugar nas recomendações?",
      inputPlaceholder: "Digite sua dúvida aqui...",
      sendBtn: "Enviar",
      typing: "Digitando resposta...",
      fallbackReply: "O GeoPulse AI ativa sua presença em 1º Lugar nas IAs por R$ 197 taxa única com Garantia Blindada de 7 Dias. Se quiser falar diretamente com a diretoria técnica, nos envie uma mensagem!",
      quickBtns: [
        { label: "Como funciona?", msg: "Como funciona o Desafio de 14 Dias?" },
        { label: "Serve sem site?", msg: "Preciso ter site ou serve com Instagram?" },
        { label: "Tem mensalidade?", msg: "Tem mensalidade?" },
        { label: "Garantia", msg: "Qual a garantia de devolução?" }
      ]
    },

    checkout: {
      badge: "🚀 Desafio Sprint de 14 Dias IA",
      title: "Ativar 14 Dias de Trabalho da IA",
      desc: "Investimento em <strong>taxa única</strong> (sem mensalidades). Inclui os 14 dias de engenharia semântica + 7 ativos vitais + publicação do Guia Oficial Top 5.",
      bumpTitle: "SIM! Adicionar Pacote Expansão Regional",
      bumpBadge: "+ R$ 50,00",
      bumpDesc: "Blindagem semântica em até <strong>3 cidades vizinhas</strong> da sua região + Kit com <strong>Bio de Alta Conversão & 5 Posts de Autoridade IA</strong> para Instagram e LinkedIn.",
      totalLabel: "Total a Pagar (Taxa Única):",
      mpBtn: "💳 Pagar com Mercado Pago (PIX ou Cartão em até 12x)",
      pixBtn: "✅ Já fiz o PIX — Iniciar Meu Desafio de 14 Dias",
      footerGuar: "🛡️ Garantia Blindada de 7 Dias",
      footerSec: "🔒 Ambiente 100% Seguro"
    }
  },

  en: {
    currencySymbol: "$",
    currencyCode: "USD",
    locale: "en-US",
    planPrice: 47.0,
    bumpPrice: 15.0,
    defaultTicket: 300,
    ticketMin: 50,
    ticketMax: 3000,
    ticketStep: 25,
    ticketScale: ["$ 50", "$ 500", "$ 1,500", "$ 3,000+"],

    liveBarTitle: "Live 14-Day Engine:",
    marquee: [
      "⚙️ <strong>Day 14/14 Completed:</strong> Dr. Henry Vance rose from 24% to 94.5% (#1 Rank on ChatGPT Search)",
      "🚀 <strong>Day 2/14 Executed:</strong> Prime Dental Clinic had its Official Top 5 Guide published automatically by AI",
      "📡 <strong>Day 10/14 Executed:</strong> Apex Accounting received IndexNow Ping on Bing and Perplexity crawlers",
      "📈 <strong>Day 7/14 Executed:</strong> Dr. Camila Morales reached 78.4% in Mid-Challenge Re-Audit"
    ],

    navBadge: "14-Day AI Challenge",
    navSub: "The AI that works 14 straight days for you to rank your brand at #1",
    navLinkVideo: "🎥 Video (40s)",
    navLinkChallenge: "🔥 The 14-Day Challenge",
    navLinkHow: "How it Works",
    navLinkDir: "Official Directory",
    navDemoBtn: "📊 View 14-Day Evolution",
    navCtaBtn: "Free Audit (10s) ↓",

    heroBadgePill: "Guided 14-Day Challenge",
    heroBadgeDesc: "Our AI works 14 consecutive days for you to put your name at the top of AI search queries",
    heroHeadline: 'If a client opens <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">ChatGPT right now</span> in your city, who does the AI recommend?',
    heroParagraph: "Discover your score for free in <strong>10 seconds</strong>. And if you're invisible, activate our <strong>14-Day Challenge</strong>: our Artificial Intelligence takes over the heavy lifting and executes <strong>14 daily technical actions</strong> to push your company or professional brand to the top of ChatGPT, Gemini, and Perplexity.",
    heroVideoTitle: "🎥 Official GeoPulse AI Presentation (0:40s)",
    videoHdBadge: "▶ High Definition (HD)",
    videoBadge: "Quick Overview (40s)",
    videoListen: "🔊 Click to listen",
    videoWatchBtn: "▶ Watch Presentation (0:40s)",
    videoQuote: '💬 <em>"Over 70% of people stopped searching on Google. Now they buy what AI recommends directly in the chat."</em>',

    // SIMULATOR (User screenshot)
    sim: {
      headerBadge: "14-Day Challenge Simulator",
      headerTitle: "How your position climbs day after day",
      btnDay0: "Day 0 (Today)",
      btnDay14: "Day 14 (Post-AI)",
      day0Label: "Status on Day 0 (Before AI works):",
      day0Score: "Score: 21.4%",
      day0Badge: "⚠️ YOU OUT OF THE AI RANKING",
      day0Competitor: "🥇 1. Your Direct Competitor — <span class=\"text-emerald-600 font-bold\">Recommended #1</span>",
      day0YourCompany: "❌ Your Business / Your Name",
      day0Invisible: "Invisible in Chat",

      day14Label: "Result on Day 14 (After 14 AI actions):",
      day14Score: "Score: 94.5%",
      day14Badge: "🚀 DAY 14: YOU IN #1 PLACE ON AIs",
      day14YourCompany: "🥇 1. YOUR BUSINESS / YOUR NAME — Recommended #1",

      explainTitle: "💡 What you are paying for in the Challenge ($47 USD one-time):",
      explainDesc: "For <strong>14 straight days</strong>, our AI executes 1 technical step each day (generating semantic files, publishing comparison articles, pinging search bots, and re-auditing your score) to position you at the top of AI search queries."
    },

    step1Badge: "👇 Step 1 (Free): Discover your Current Score in 10 Seconds",
    formMainTitle: "Free AI Visibility Audit",

    presets: {
      adv: "⚖️ Lawyer Example",
      clinica: "🦷 Clinic Example",
      demo: "⚡ Simulate Audit Now"
    },

    entityButtons: {
      company: "Company / Clinic / Business",
      autonomous: "Independent / Specialist"
    },

    formCompany: {
      nameLabel: "🏢 Business, Clinic, or Brand Name *",
      namePlaceholder: "E.g.: Prime Dental Care or Silva & Associates",
      urlLabel: "🌐 Official Website or Social Profile *",
      urlPlaceholder: "E.g.: www.yourcompany.com or @yourbusiness",
      nicheLabel: "🎯 Industry or Service Category *",
      nichePlaceholder: "E.g.: Dental Implants, Corporate Law, Accounting",
      cityLabel: "📍 City and Region / State *",
      cityPlaceholder: "E.g.: Miami - FL, New York - NY, London - UK",
      registryLabel: "🏛️ Business Registration or Tax ID (Optional)",
      registryPlaceholder: "E.g.: EIN, Registration Number, or Chamber ID",
      registryHint: "Helps AI search engines confirm business legitimacy.",
      competitorsLabel: "⚔️ Direct Local Competitors (Optional)",
      competitorsPlaceholder: "E.g.: Competitor 1, Competitor 2",
      competitorsHint: "AI compares your authority against them in search queries."
    },

    formAuto: {
      nameLabel: "👤 Full Professional Name *",
      namePlaceholder: "E.g.: Dr. Camila Mendes or Attorney John Smith",
      urlLabel: "🌐 Professional Instagram, LinkedIn, or Website *",
      urlPlaceholder: "E.g.: @dr.johnsmith or www.johnsmithlaw.com",
      nicheLabel: "🎯 Your Specialty / Area of Expertise *",
      nichePlaceholder: "E.g.: Dermatology, Tax Law, Clinical Psychology",
      cityLabel: "📍 City and Region / State where you practice *",
      cityPlaceholder: "E.g.: Los Angeles - CA, Chicago - IL, Toronto - ON",
      registryLabel: "📜 Professional License or Board ID (Bar, Medical, Board...)",
      registryPlaceholder: "E.g.: Bar #12345 or Medical Board #67890",
      registryHint: "Crucial for AI models to verify you as a certified authority.",
      competitorsLabel: "⚔️ Other Specialists Competing with You (Optional)",
      competitorsPlaceholder: "E.g.: Dr. Jane Doe, Top Firm",
      competitorsHint: "Enables AI to measure your ranking against established authorities."
    },

    contact: {
      whatsapp: "📱 WhatsApp / Phone Number *",
      whatsappPlaceholder: "E.g.: +1 (305) 555-0192",
      email: "✉️ Your Email to Receive the Report",
      emailPlaceholder: "E.g.: you@yourcompany.com",
      securityNote: "🔒 100% Free Audit in 10 seconds",
      submitBtn: "🔍 Run Free AI Visibility Audit Now"
    },

    sprintSection: {
      badge: "Total Transparency: What are you paying for?",
      title: "See what our AI does for you during the 14 Days",
      subtitle: "You pay only once ($47 USD) and our engine automatically executes the 14 steps below to build your leadership in AI searches:"
    },

    scheduleDayPrefix: "Day",
    scheduleDayOf: "of",
    scheduleSub: "Executed automatically by AI",
    schedule14: [
      { day: 1, title: "Entity Protocol & JSON-LD + /llms.txt" },
      { day: 2, title: "Official City Top 5 Guide Publication" },
      { day: 3, title: "Zero-Click Semantic FAQ Architecture" },
      { day: 4, title: "Entity Anchoring in ChatGPT & Perplexity" },
      { day: 5, title: "Educational Niche In-Depth Article" },
      { day: 6, title: "Schema.org Structured Data Enrichment" },
      { day: 7, title: "Mid-Sprint Re-Audit & Density Adjustment" },
      { day: 8, title: "Semantic Comparison Page Construction" },
      { day: 9, title: "Social Proof Matrix & Success Cases" },
      { day: 10, title: "IndexNow Pings to AI Crawlers" },
      { day: 11, title: "Industry Trends & Innovation Article" },
      { day: 12, title: "Third-Party Citations & Mentions Audit" },
      { day: 13, title: "Local Knowledge Base Consolidation" },
      { day: 14, title: "Final Authority Report & Official Delivery" }
    ],

    results: {
      statusBadge: "Diagnostic Completed (Day 0)",
      reportTitle: "AI Positioning Report",
      shareBtn: "Send to Partner (WhatsApp)",
      topCta: "🚀 Start 14-Day Challenge (AI Working for You — $47 USD)",
      metric1Label: "Current AI Score (Share of Model)",
      metric1Goal: "Goal after 14 days: >90%",
      metric2Label: "Current Ranking Position",
      notRanked: "Out of Ranking",
      rankSuffix: "Rank",
      metric2Sub: "Spontaneous ranking in your city",
      metric3Label: "14-Day Challenge Status",
      dayPrefix: "Day",
      metric3Sub: "14 daily actions ready to start",
      clientsPerMonth: "clients / month",

      lossHeaderBadge: "Revenue Alert: How much are you losing today?",
      lossHeaderTitle: "Estimated Business & Clients Lost to Competitors",
      lossHeaderDescTemplate: "When someone in your city asks ChatGPT or Gemini for a recommendation in {niche}, the algorithms recommend your competitors at the top. Here is the estimated revenue you are missing out on:",
      searchesLabel: "Local AI Searches / Mo",
      searchesSub: "People searching on ChatGPT and Gemini with high purchasing intent in your city.",
      clientsLabel: "Lost Clients / Mo",
      clientsSub: "Clients who buy from the competitor ranked #1 by AI.",
      annualLabel: "Projected Annual Loss",
      annualSub: "Cumulative annual revenue going straight to your direct competitors.",

      roiBadge: "ROI Calculation",
      roiTitle: "GeoPulse AI costs only <strong>$47 USD one-time fee</strong>",
      roiDesc: "With <strong>just 1 single client recovered</strong> via ChatGPT or Gemini, you already recover the entire cost of the 14-Day Challenge with profit and secure your local leadership.",
      roiCta: "🛡️ Stop Losing Clients & Activate ($47 USD) →",

      auditsHeading: "🤖 What ChatGPT, Gemini, and Perplexity responded:",
      cited: "✓ Cited",
      notCited: "✗ Not Recommended",
      action14: "✓ 14-Day Action:",

      sidebarBadge: "🔥 14-Day Sprint Challenge",
      sidebarTitle: "Hire our AI to work 14 days straight for your ranking position",
      sidebarDesc: "For a <strong>one-time fee of $47 USD (no subscriptions)</strong>, our AI executes 1 technical action per day for 14 days (JSON-LD, /llms.txt, City Official Top 5 Guide, Semantic FAQ, and IndexNow Pings) to place you #1.",
      sidebarCta: "Activate My 14-Day Challenge Now ($47 USD) →"
    },

    scarcity: {
      statusBadge: "Regional Exclusivity Status",
      ruleLabel: "AI Golden Rule:",
      vagaText: "Official #1 Spot in",
      paraText: "for",
      availBadge: "AVAILABLE NOW",
      desc: "AI algorithms only recommend <strong>1 single professional or business at the #1 top of the Official Guide</strong>. By activating the 14-Day Challenge, you secure exclusivity before a local competitor takes the canonical referral.",
      ctaBtn: "Secure #1 Exclusivity Now →"
    },

    lossBadge: "Direct Commercial Impact",
    lossMonthlyLbl: "Estimated Monthly Loss",
    lossSubMonthlyLbl: "/ mo to competitors",
    lossTicketSimTitle: "Simulate with your Real Average Ticket:",
    lossTicketSimSub: "Drag to adjust how much an average customer spends with you:",
    lossTicketSimBadge: "Selected Ticket:",

    guarBadge: "Absolute Zero Risk • Consumer Protection",
    guarTitle: "7-Day Unconditional Guarantee: 100% Refund",
    guarDesc: "We are so confident in our semantic engineering technology that we assume all the risk: if within <strong>7 days</strong> of purchase your GEO structure, your <code>/llms.txt</code> file, and your Official Top 5 Guide are not published and delivered on the server, just send us a single message and <strong>we will refund 100% of your payment immediately</strong>, no questions asked and no fine print.",

    faqBadge: "Clear Your Doubts",
    faqTitle: "Frequently Asked Questions about the Challenge",
    faqSub: "Everything you need to know before starting the AI's 14 days:",
    faqs: [
      {
        q: "💰 Is the $47 USD fee one-time or are there hidden subscriptions?",
        a: "<strong>One-time promotional fee of $47.00 USD.</strong> There is no monthly fee, subscription, or surprise recurring cost. The price covers 14 days of active AI engine executions and guarantees lifetime hosting of your assets in our indexed public directory."
      },
      {
        q: "⚡ Do I need to do anything technical, or does AI handle everything?",
        a: "<strong>You don't need to do anything technical.</strong> GeoPulse was built specifically for business owners and professionals who don't know coding or complex SEO. Our AI generates the code, writes semantic copy, publishes on our high-speed directory, and triggers crawler protocols for ChatGPT, Perplexity, and Gemini."
      },
      {
        q: "🕒 How long does it take to see the first results on ChatGPT and Gemini?",
        a: "Because search engines and LLM crawlers refresh at different rates, most clients start seeing spontaneous mentions and citations between the <strong>7th and 14th day</strong> of continuous execution."
      },
      {
        q: "🎯 Why is there a 1-business-per-niche/city exclusivity rule?",
        a: "Because generative AI only delivers <strong>1 top canonical authority answer</strong>. If we accepted two competing businesses in the same city, we would create a canonical conflict."
      },
      {
        q: "🛡️ How does the 7-day 100% money-back guarantee work?",
        a: "Simple and transparent: if you activate the challenge and for any reason are not thrilled with the technical progress or generated assets, just message our support within 7 days for a full immediate refund."
      }
    ],

    floatingChatPill: "💬 Questions about the Challenge? Chat with AI",

    loading: {
      badge: "Real-Time AI Audit",
      title: "Querying AI Search Engines...",
      initSub: "Connecting to semantic reader and extracting public data from your website/profile...",
      footer: "Simulating live queries on ChatGPT Search, Gemini, and Perplexity",
      btnRunning: "⏳ Auditing across AI engines...",
      doneSuccess: "✓ Audit completed successfully!",
      doneFinish: "Finishing...",
      steps: [
        { at: 28, text: "🔍 Reading technical metadata, authority signals, and service area..." },
        { at: 52, text: "🤖 Simulating customer queries on ChatGPT Search, Gemini, and Perplexity..." },
        { at: 74, text: "📊 Mapping direct competitors recommended by algorithms in your city..." },
        { at: 90, text: "💰 Calculating estimated lost clients and revenue going to competitors..." },
        { at: 96, text: "✨ Structuring your official AI positioning report..." }
      ]
    },

    chat: {
      title: "GeoPulse AI Specialist",
      online: "Online 24/7 • Instant Q&A",
      welcome: "Hello! I am GeoPulse's AI Specialist. Do you have any questions about how the 14-Day Challenge works, pricing ($47 USD), or how we rank you #1 on AI recommendations?",
      inputPlaceholder: "Type your question here...",
      sendBtn: "Send",
      typing: "Typing reply...",
      fallbackReply: "GeoPulse AI activates your #1 ranking across AI search engines for a one-time $47 USD fee with a 7-Day Ironclad Guarantee!",
      quickBtns: [
        { label: "How it works?", msg: "How does the 14-Day Challenge work?" },
        { label: "No website needed?", msg: "Do I need a website or does Instagram work?" },
        { label: "Any monthly fee?", msg: "Is there any monthly subscription?" },
        { label: "Guarantee", msg: "How does the 7-day refund guarantee work?" }
      ]
    },

    checkout: {
      badge: "🚀 14-Day AI Sprint Challenge",
      title: "Activate 14 Days of AI Work",
      desc: "Investment in a <strong>one-time fee</strong> (no monthly subscriptions). Includes 14 days of semantic engineering + 7 vital assets + Official Top 5 Guide publication.",
      bumpTitle: "YES! Add Regional Expansion Package",
      bumpBadge: "+ $15.00 USD",
      bumpDesc: "Semantic shielding in up to <strong>3 neighboring cities</strong> in your region + Kit with <strong>High-Converting Bio & 5 AI Authority Posts</strong> for Instagram and LinkedIn.",
      totalLabel: "Total to Pay (One-Time Fee):",
      mpBtn: "💳 Pay with PayPal / International Credit Card ($47 USD)",
      pixBtn: "✅ I have sent the payment — Start My 14-Day Challenge",
      footerGuar: "🛡️ 7-Day Ironclad Guarantee",
      footerSec: "🔒 100% Secure Environment"
    }
  },

  es: {
    currencySymbol: "$",
    currencyCode: "USD",
    locale: "es-ES",
    planPrice: 47.0,
    bumpPrice: 15.0,
    defaultTicket: 300,
    ticketMin: 50,
    ticketMax: 3000,
    ticketStep: 25,
    ticketScale: ["$ 50", "$ 500", "$ 1,500", "$ 3,000+"],

    liveBarTitle: "Motor de 14 Días en Vivo:",
    marquee: [
      "⚙️ <strong>Día 14/14 Completado:</strong> Dr. Henry Vance subió de 24% a 94.5% (1º Puesto en ChatGPT Search)",
      "🚀 <strong>Día 2/14 Ejecutado:</strong> Clínica OdontoPrime publicó su Guía Oficial Top 5 automáticamente por IA",
      "📡 <strong>Día 10/14 Ejecutado:</strong> Estudio Contable Atlas recibió Ping IndexNow en Bing y Perplexity",
      "📈 <strong>Día 7/14 Ejecutado:</strong> Dra. Camila Morales alcanzó 78.4% en la Reauditoría Intermedia del Desafío"
    ],

    navBadge: "Desafío de 14 Días IA",
    navSub: "La IA que trabaja 14 días seguidos por ti para posicionar tu marca en el #1",
    navLinkVideo: "🎥 Video (40s)",
    navLinkChallenge: "🔥 El Desafío de 14 Días",
    navLinkHow: "Cómo Funciona",
    navLinkDir: "Directorio Oficial",
    navDemoBtn: "📊 Ver Evolución 14 Días",
    navCtaBtn: "Prueba Gratis (10s) ↓",

    heroBadgePill: "Desafío Guiado de 14 Días",
    heroBadgeDesc: "Nuestra IA trabaja 14 días consecutivos por ti para colocar tu nombre en la cima de las búsquedas de IA",
    heroHeadline: 'Si un cliente abre <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-600">ChatGPT ahora</span> en tu ciudad, ¿a quién recomienda la IA?',
    heroParagraph: "Descubre tu puntuación gratis en <strong>10 segundos</strong>. Y si estás invisible, activa nuestro <strong>Desafío de 14 Días</strong>: nuestra Inteligencia Artificial asume el trabajo pesado y ejecuta <strong>14 acciones técnicas diarias</strong> para hacer subir tu empresa o nombre profesional en el ranking de ChatGPT, Gemini y Perplexity.",
    heroVideoTitle: "🎥 Presentación Oficial GeoPulse AI (0:40s)",
    videoHdBadge: "▶ Alta Definición (HD)",
    videoBadge: "Resumen Rápido (40s)",
    videoListen: "🔊 Haz clic para escuchar",
    videoWatchBtn: "▶ Ver Presentación (0:40s)",
    videoQuote: '💬 <em>"Más del 70% de las personas dejaron de buscar en Google. Ahora compran lo que la IA recomienda directo en el chat."</em>',

    // SIMULADOR (Imagen del usuario)
    sim: {
      headerBadge: "Simulador del Desafío de 14 Días",
      headerTitle: "Cómo tu posición sube día tras día",
      btnDay0: "Día 0 (Hoy)",
      btnDay14: "Día 14 (Post-IA)",
      day0Label: "Estado en el Día 0 (Sin la IA trabajar):",
      day0Score: "Score: 21.4%",
      day0Badge: "⚠️ ESTÁS FUERA DEL RANKING DE IA",
      day0Competitor: "🥇 1. Tu Competidor Directo — <span class=\"text-emerald-600 font-bold\">Recomendado #1</span>",
      day0YourCompany: "❌ Tu Empresa / Tu Nombre",
      day0Invisible: "Invisible en el Chat",

      day14Label: "Resultado en el Día 14 (Tras 14 acciones de la IA):",
      day14Score: "Score: 94.5%",
      day14Badge: "🚀 DÍA 14: TÚ EN 1º LUGAR EN LAS IAs",
      day14YourCompany: "🥇 1. TU EMPRESA / TU NOMBRE — Recomendado #1",

      explainTitle: "💡 Por qué estás pagando en el Desafío ($47 USD único):",
      explainDesc: "Durante <strong>14 días seguidos</strong>, nuestra IA ejecuta 1 etapa técnica por día (crea tus archivos semánticos, publica artículos comparativos, envía pings a los rastreadores y reaudita tu nota) para posicionarte en el #1 de las búsquedas de IA."
    },

    step1Badge: "👇 Paso 1 (Gratis): Descubre tu Puntuación Actual en 10 Segundos",
    formMainTitle: "Auditoría Gratuita de Visibilidad en IA",

    presets: {
      adv: "⚖️ Ejemplo Abogado",
      clinica: "🦷 Ejemplo Clínica",
      demo: "⚡ Simular Auditoría Ahora"
    },

    entityButtons: {
      company: "Empresa / Clínica / Negocio",
      autonomous: "Profesional Independiente / Autónomo"
    },

    formCompany: {
      nameLabel: "🏢 Nombre de la Empresa, Clínica o Marca *",
      namePlaceholder: "Ej.: Clínica OdontoPrime o Silva & Asociados",
      urlLabel: "🌐 Sitio Web Oficial o Instagram del Negocio *",
      urlPlaceholder: "Ej.: www.tuempresa.com o @tuempresa",
      nicheLabel: "🎯 Especialidad o Rubro de Actividad *",
      nichePlaceholder: "Ej.: Implantes Dentales, Abogacía Laboral, Contabilidad",
      cityLabel: "📍 Ciudad y Región / Provincia *",
      cityPlaceholder: "Ej.: Madrid - España, Buenos Aires - Argentina, Santiago - Chile",
      registryLabel: "🏛️ CIF / RFC o Registro Oficial de la Empresa (Opcional)",
      registryPlaceholder: "Ej.: CIF B-12345678 o Registro Mercantil",
      registryHint: "Ayuda a los motores de IA a confirmar la legitimidad de tu negocio.",
      competitorsLabel: "⚔️ Competidores Directos en la Región (Opcional)",
      competitorsPlaceholder: "Ej.: Competidor 1, Competidor 2",
      competitorsHint: "La IA comparará tu empresa contra ellos en las recomendaciones."
    },

    formAuto: {
      nameLabel: "👤 Tu Nombre Profesional Completo *",
      namePlaceholder: "Ej.: Dra. Camila Morales o Lic. Rafael Morales",
      urlLabel: "🌐 Tu Instagram Profesional, LinkedIn o Sitio Web *",
      urlPlaceholder: "Ej.: @dr.tunombre o www.tusitio.com",
      nicheLabel: "🎯 Tu Especialidad o Área de Práctica *",
      nichePlaceholder: "Ej.: Dermatología, Derecho Tributario, Psicología",
      cityLabel: "📍 Ciudad y Región donde Atiendes *",
      cityPlaceholder: "Ej.: Bogotá - Colombia, CDMX - México, Lima - Perú",
      registryLabel: "📜 Colegiatura o Matrícula Profesional (Colegio Médico, Abogados...)",
      registryPlaceholder: "Ej.: Matrícula Profesional 45.678",
      registryHint: "Clave para que la IA te certifique como Autoridad Técnica verificada.",
      competitorsLabel: "⚔️ Otros Especialistas que Compiten Contigo (Opcional)",
      competitorsPlaceholder: "Ej.: Dr. Gómez, Centro Médico X",
      competitorsHint: "Permite a la IA comparar tu posicionamiento contra la competencia."
    },

    contact: {
      whatsapp: "📱 WhatsApp / Teléfono de Contacto *",
      whatsappPlaceholder: "Ej.: +34 612 345 678",
      email: "✉️ Tu Correo Electrónico para Recibir el Informe",
      emailPlaceholder: "Ej.: tu@tuempresa.com",
      securityNote: "🔒 Auditoría 100% Gratuita en 10 segundos",
      submitBtn: "🔍 Ejecutar Auditoría Gratuita en las IAs Ahora"
    },

    sprintSection: {
      badge: "Transparencia Total: ¿Por qué estás pagando?",
      title: "Mira lo que nuestra IA hace por ti durante los 14 Días",
      subtitle: "Pagas una sola vez ($47 USD) y nuestro motor ejecuta automáticamente las 14 etapas a continuación para construir tu liderazgo en búsquedas de IA:"
    },

    scheduleDayPrefix: "Día",
    scheduleDayOf: "de",
    scheduleSub: "Ejecutado automáticamente por la IA",
    schedule14: [
      { day: 1, title: "Protocolo de Entidad y JSON-LD + /llms.txt" },
      { day: 2, title: "Publicación de la Guía Oficial Top 5 de la Ciudad" },
      { day: 3, title: "Arquitectura de FAQ Semántico Zero-Click" },
      { day: 4, title: "Anclaje de Entidad en ChatGPT y Perplexity" },
      { day: 5, title: "Artículo Educativo de Profundización del Nicho" },
      { day: 6, title: "Enriquecimiento de Datos Estructurados Schema.org" },
      { day: 7, title: "Reauditoría Intermedia y Ajuste de Densidad" },
      { day: 8, title: "Construcción de Página Semántica Comparativa" },
      { day: 9, title: "Matriz de Prueba Social y Casos de Éxito" },
      { day: 10, title: "Pings IndexNow a los Rastreadores de IA" },
      { day: 11, title: "Artículo de Tendencias e Innovaciones del Sector" },
      { day: 12, title: "Auditoría de Citas y Menciones de Terceros" },
      { day: 13, title: "Consolidación de la Base de Conocimiento Local" },
      { day: 14, title: "Informe Final de Autoridad y Entrega Oficial" }
    ],

    results: {
      statusBadge: "Diagnóstico Completado (Día 0)",
      reportTitle: "Informe de Posicionamiento IA",
      shareBtn: "Enviar al Socio (WhatsApp)",
      topCta: "🚀 Iniciar Desafío de 14 Días (IA Trabajando por Ti — $47 USD)",
      metric1Label: "Puntuación Actual en IAs (Share of Model)",
      metric1Goal: "Meta tras los 14 días: >90%",
      metric2Label: "Posición Actual en el Ranking",
      notRanked: "Fuera del Ranking",
      rankSuffix: "º Lugar",
      metric2Sub: "Ranking espontáneo en tu ciudad",
      metric3Label: "Estado del Desafío de 14 Días",
      dayPrefix: "Día",
      metric3Sub: "14 acciones diarias listas para iniciar",
      clientsPerMonth: "clientes / mes",

      lossHeaderBadge: "Alerta de Facturación: ¿Cuánto estás perdiendo hoy?",
      lossHeaderTitle: "Estimación de Negocios y Clientes Perdidos para Competidores",
      lossHeaderDescTemplate: "Cuando alguien en tu ciudad busca recomendaciones de {niche} en ChatGPT o Gemini, los algoritmos recomiendan a tus competidores. Mira el cálculo estimado del dinero que estás perdiendo:",
      searchesLabel: "Búsquedas Locales en IA / Mes",
      searchesSub: "Personas buscando en ChatGPT y Gemini con alta intención de contratación en tu ciudad.",
      clientsLabel: "Clientes Perdidos / Mes",
      clientsSub: "Clientes que compran al competidor indicado en 1º lugar por la IA.",
      annualLabel: "Pérdida Anual Proyectada",
      annualSub: "Estimación anual acumulada yendo a tus competidores directos.",

      roiBadge: "Cálculo de Retorno",
      roiTitle: "GeoPulse AI cuesta solo <strong>$47 USD tarifa única</strong>",
      roiDesc: "Con <strong>solo 1 único cliente recuperado</strong> a través de ChatGPT o Gemini, ya recuperas con creces todo el valor del Desafío de 14 Días y consolidas tu liderazgo local.",
      roiCta: "🛡️ Dejar de Perder Clientes y Activar ($47 USD) →",

      auditsHeading: "🤖 Qué respondieron ChatGPT, Gemini y Perplexity:",
      cited: "✓ Citado",
      notCited: "✗ No Recomendado",
      action14: "✓ Acción en los 14 Días:",

      sidebarBadge: "🔥 Desafío Sprint de 14 Días",
      sidebarTitle: "Contrata a nuestra IA para trabajar 14 días seguidos por tu posición en el ranking",
      sidebarDesc: "Por una <strong>tarifa única de $47 USD (sin mensualidades)</strong>, nuestra IA ejecuta 1 acción técnica por día durante 14 días (JSON-LD, /llms.txt, Guía Oficial Top 5 de la Ciudad, FAQ Semántico y Pings IndexNow) para colocarte en 1º lugar.",
      sidebarCta: "Activar Mi Desafío de 14 Días Ahora ($47 USD) →"
    },

    scarcity: {
      statusBadge: "Estado de Exclusividad Regional",
      ruleLabel: "Regla de Oro de la IA:",
      vagaText: "Plaza #1 Oficial en",
      paraText: "para",
      availBadge: "DISPONIBLE AHORA",
      desc: "Los algoritmos de IA solo recomiendan a <strong>1 único profesional o empresa en el top #1 de la Guía Oficial</strong>. Al activar el Desafío de 14 Días, aseguras la exclusividad antes de que un competidor local tome la recomendación canónica.",
      ctaBtn: "Asegurar Exclusividad de la Plaza #1 →"
    },

    lossBadge: "Impacto Comercial Directo",
    lossMonthlyLbl: "Pérdida Mensual Estimada",
    lossSubMonthlyLbl: "/ mes para competidores",
    lossTicketSimTitle: "Simula con tu Ticket Medio Real:",
    lossTicketSimSub: "Desliza para ajustar cuánto gasta en promedio un cliente contigo:",
    lossTicketSimBadge: "Ticket Seleccionado:",

    guarBadge: "Riesgo Cero Absoluto • Protección al Consumidor",
    guarTitle: "Garantía Incondicional de 7 Días: Devolución del 100%",
    guarDesc: "Confiamos tanto en la eficacia de nuestra tecnología semántica que asumimos todo el riesgo: si dentro de los <strong>7 días</strong> posteriores a la contratación tu estructura GEO, tu archivo <code>/llms.txt</code> y tu Guía Oficial Top 5 no están publicados y entregados en el servidor, solo envíanos un mensaje y <strong>te devolveremos el 100% de tu dinero inmediatamente</strong>, sin preguntas ni letra chica.",

    faqBadge: "Resuelve Tus Dudas",
    faqTitle: "Preguntas Frecuentes sobre el Desafío",
    faqSub: "Todo lo que necesitas saber antes de iniciar los 14 días de la IA:",
    faqs: [
      {
        q: "💰 ¿La tarifa de $47 USD es un pago único o hay mensualidades ocultas?",
        a: "<strong>Tarifa única promocional de $47.00 USD.</strong> No existe ninguna mensualidad, suscripción ni cobro recurrente sorpresa. El precio cubre los 14 días de ejecuciones activas del motor de IA y garantiza la permanencia de por vida de tus activos generados en nuestro directorio público indexado."
      },
      {
        q: "⚡ ¿Necesito hacer algo técnico o la IA lo hace todo sola?",
        a: "<strong>No necesitas hacer nada técnico.</strong> GeoPulse fue creado justamente para dueños de empresas y profesionales que no entienden de programación ni de SEO avanzado. Nuestra IA genera el código, redacta los textos semánticos, publica en nuestro directorio de alta velocidad y envía los protocolos para ChatGPT, Perplexity y Gemini."
      },
      {
        q: "🕒 ¿Cuánto tiempo toma ver los primeros resultados en ChatGPT y Gemini?",
        a: "Como los motores de IA y buscadores actualizan sus índices a diferentes ritmos, la mayoría de los clientes comienza a notar sus primeras menciones y recomendaciones espontáneas entre el <strong>7º y el 14º día</strong> de ejecución continua."
      },
      {
        q: "🎯 ¿Por qué existe la regla de exclusividad de 1 empresa por nicho y ciudad?",
        a: "Porque la IA generativa solo entrega <strong>1 respuesta canónica en primer lugar</strong>. Si aceptáramos a dos competidores directos en la misma ciudad, generaríamos un conflicto canónico."
      },
      {
        q: "🛡️ ¿Cómo funciona la garantía de 7 días de devolución total?",
        a: "Simple y transparente: si activas el desafío y por cualquier motivo no quedas conforme con los activos generados o el progreso técnico de la IA, solo avísanos por soporte dentro de los primeros 7 días para un reembolso completo."
      }
    ],

    floatingChatPill: "💬 ¿Dudas sobre el Desafío? Chatea con la IA",

    loading: {
      badge: "Auditoría en Tiempo Real",
      title: "Consultando Motores de IA...",
      initSub: "Conectando al lector semántico y extrayendo datos públicos de tu sitio/perfil...",
      footer: "Simulando consultas en ChatGPT Search, Gemini y Perplexity",
      btnRunning: "⏳ Auditando en los motores de IA...",
      doneSuccess: "✓ ¡Auditoría completada con éxito!",
      doneFinish: "Finalizando...",
      steps: [
        { at: 28, text: "🔍 Leyendo metadatos técnicos, autoridad y área de cobertura..." },
        { at: 52, text: "🤖 Simulando búsquedas de clientes en ChatGPT Search, Gemini y Perplexity..." },
        { at: 74, text: "📊 Mapeando competidores directos recomendados por los algoritmos en la región..." },
        { at: 90, text: "💰 Calculando estimación de clientes y facturación perdida ante terceros..." },
        { at: 96, text: "✨ Estructurando el informe oficial de posicionamiento..." }
      ]
    },

    chat: {
      title: "Especialista GeoPulse AI",
      online: "En línea 24h • Consultas",
      welcome: "¡Hola! Soy la Especialista de IA de GeoPulse. ¿Tienes alguna duda sobre cómo funciona el Desafío de 14 Días, precios ($47 USD) o cómo te posicionamos en 1º Lugar?",
      inputPlaceholder: "Escribe tu duda aquí...",
      sendBtn: "Enviar",
      typing: "Escribiendo respuesta...",
      fallbackReply: "GeoPulse AI activa tu presencia en 1º Lugar en las IAs por $47 USD tarifa única con Garantía Blindada de 7 Días.",
      quickBtns: [
        { label: "¿Cómo funciona?", msg: "¿Cómo funciona el Desafío de 14 Días?" },
        { label: "¿Sirve sin web?", msg: "¿Necesito tener sitio web o sirve con Instagram?" },
        { label: "¿Hay mensualidad?", msg: "¿Tiene alguna mensualidad?" },
        { label: "Garantía", msg: "¿Cuál es la garantía de devolución?" }
      ]
    },

    checkout: {
      badge: "🚀 Desafío Sprint de 14 Días IA",
      title: "Activar 14 Días de Trabajo de la IA",
      desc: "Inversión en <strong>tarifa única</strong> (sin mensualidades). Incluye los 14 días de ingeniería semántica + 7 activos vitales + publicación de la Guía Oficial Top 5.",
      bumpTitle: "¡SÍ! Agregar Paquete de Expansión Regional",
      bumpBadge: "+ $15.00 USD",
      bumpDesc: "Blindaje semántico en hasta <strong>3 ciudades vecinas</strong> de tu región + Kit con <strong>Biografía de Alta Conversión y 5 Posts de Autoridad IA</strong> para Instagram y LinkedIn.",
      totalLabel: "Total a Pagar (Tarifa Única):",
      mpBtn: "💳 Pagar con PayPal / Tarjeta Internacional ($47 USD)",
      pixBtn: "✅ Ya realicé el pago — Iniciar Mi Desafío de 14 Días",
      footerGuar: "🛡️ Garantía Blindada de 7 Días",
      footerSec: "🔒 Ambiente 100% Seguro"
    }
  }
};

let currentLang = "pt";

function detectLanguage() {
  const saved = localStorage.getItem("geopulse_lang");
  if (saved && ["pt", "en", "es"].includes(saved)) {
    return saved;
  }
  const browserLangs = navigator.languages || [navigator.language || "pt"];
  for (const bl of browserLangs) {
    const code = bl.toLowerCase().slice(0, 2);
    if (code === "pt") return "pt";
    if (code === "es") return "es";
    if (code === "en") return "en";
  }
  return "pt";
}

function setLanguage(lang) {
  if (!["pt", "en", "es"].includes(lang)) lang = "pt";
  currentLang = lang;
  window.currentLang = lang;
  localStorage.setItem("geopulse_lang", lang);

  const btnPt = document.getElementById("lang-btn-pt");
  const btnEn = document.getElementById("lang-btn-en");
  const btnEs = document.getElementById("lang-btn-es");

  const activeClasses = "bg-white text-slate-900 shadow-sm border border-slate-200";
  const inactiveClasses = "text-slate-500 hover:text-slate-900";

  [btnPt, btnEn, btnEs].forEach((btn) => {
    if (btn) {
      btn.className = btn.className.replace(activeClasses, "").replace(inactiveClasses, "");
    }
  });

  if (lang === "pt" && btnPt) btnPt.className += " " + activeClasses;
  if (lang === "en" && btnEn) btnEn.className += " " + activeClasses;
  if (lang === "es" && btnEs) btnEs.className += " " + activeClasses;

  applyLanguage(lang);
}

window.render14DaySchedule = function(lang) {
  const dict = I18N[lang] || I18N.pt;
  const grid = document.getElementById("public-sprint-days-grid");
  if (!grid || !dict.schedule14) return;

  grid.innerHTML = dict.schedule14.map((d) => `
    <div class="bg-white rounded-2xl p-4 border border-slate-200 shadow-sm space-y-1">
      <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-extrabold">${dict.scheduleDayPrefix} ${d.day} ${dict.scheduleDayOf} 14</span>
      <h4 class="text-sm font-extrabold text-slate-900 pt-1">${d.title}</h4>
      <p class="text-[11px] text-slate-500">${dict.scheduleSub}</p>
    </div>
  `).join("");
};

window.updateResultsI18n = function(lang) {
  const l = (lang && I18N[lang]) ? lang : (window.currentLang || "pt");
  const dict = I18N[l] || I18N.pt;
  const res = dict.results || {};
  const sc = dict.scarcity || {};

  // Diagnostic Results Top (Image 2)
  const statusBadge = document.getElementById("res-status-badge");
  if (statusBadge) statusBadge.textContent = res.statusBadge;

  const repTitle = document.getElementById("res-company-title");
  if (repTitle && !window.currentDiagnosticData) repTitle.textContent = res.reportTitle;

  const shareBtnText = document.getElementById("res-share-btn-text");
  if (shareBtnText) shareBtnText.textContent = res.shareBtn;

  const topCta = document.getElementById("res-top-cta-btn");
  if (topCta) topCta.textContent = res.topCta;

  // Metric 1
  const m1Lbl = document.getElementById("res-metric1-label");
  if (m1Lbl) m1Lbl.textContent = res.metric1Label;
  const m1Goal = document.getElementById("res-metric1-goal");
  if (m1Goal) m1Goal.textContent = res.metric1Goal;

  // Metric 2
  const m2Lbl = document.getElementById("res-metric2-label");
  if (m2Lbl) m2Lbl.textContent = res.metric2Label;
  const m2Sub = document.getElementById("res-metric2-sub");
  if (m2Sub) m2Sub.textContent = res.metric2Sub;

  // Metric 3
  const m3Lbl = document.getElementById("res-metric3-label");
  if (m3Lbl) m3Lbl.textContent = res.metric3Label;
  const m3Sub = document.getElementById("res-metric3-sub");
  if (m3Sub) m3Sub.textContent = res.metric3Sub;

  // Scarcity Banner (Image 2)
  const scStatus = document.getElementById("scarcity-status-badge");
  if (scStatus) scStatus.textContent = sc.statusBadge;

  const scRule = document.getElementById("scarcity-rule-label");
  if (scRule) scRule.textContent = sc.ruleLabel;

  const scVaga = document.getElementById("scarcity-vaga-text");
  if (scVaga) scVaga.textContent = sc.vagaText;

  const scPara = document.getElementById("scarcity-para-text");
  if (scPara) scPara.textContent = sc.paraText;

  const scAvail = document.getElementById("scarcity-avail-badge");
  if (scAvail) scAvail.textContent = sc.availBadge;

  const scDesc = document.getElementById("scarcity-desc");
  if (scDesc) scDesc.innerHTML = sc.desc;

  const scCta = document.getElementById("scarcity-cta-btn");
  if (scCta) scCta.textContent = sc.ctaBtn;

  // Financial Loss Card Header & Metrics
  const lossHeaderBadge = document.getElementById("loss-header-badge");
  if (lossHeaderBadge) lossHeaderBadge.textContent = res.lossHeaderBadge;

  const lossHeaderTitle = document.getElementById("loss-header-title");
  if (lossHeaderTitle) lossHeaderTitle.textContent = res.lossHeaderTitle;

  const lossHeaderDesc = document.getElementById("loss-header-desc");
  if (lossHeaderDesc && window.currentDiagnosticData) {
    const n = window.currentDiagnosticData.company?.niche || (l === "en" ? "your industry" : (l === "es" ? "tu rubro" : "sua área"));
    lossHeaderDesc.innerHTML = res.lossHeaderDescTemplate.replace("{niche}", `<strong id="loss-niche-text" class="text-slate-900">${n}</strong>`);
  }

  const lossSearchesLbl = document.getElementById("loss-metric-searches-lbl");
  if (lossSearchesLbl) lossSearchesLbl.textContent = res.searchesLabel;
  const lossSearchesSub = document.getElementById("loss-metric-searches-sub");
  if (lossSearchesSub) lossSearchesSub.textContent = res.searchesSub;

  const lossClientsLbl = document.getElementById("loss-metric-clients-lbl");
  if (lossClientsLbl) lossClientsLbl.textContent = res.clientsLabel;
  const lossClientsSub = document.getElementById("loss-metric-clients-sub");
  if (lossClientsSub) lossClientsSub.textContent = res.clientsSub;

  const lossAnnualLbl = document.getElementById("loss-metric-annual-lbl");
  if (lossAnnualLbl) lossAnnualLbl.textContent = res.annualLabel;
  const lossAnnualSub = document.getElementById("loss-metric-annual-sub");
  if (lossAnnualSub) lossAnnualSub.textContent = res.annualSub;

  const lossScale = document.getElementById("loss-ticket-scale");
  if (lossScale && dict.ticketScale) {
    lossScale.innerHTML = dict.ticketScale.map((s) => `<span>${s}</span>`).join("");
  }

  // ROI Green Banner (Price dynamically converted)
  const lossRoiBadge = document.getElementById("loss-roi-badge");
  if (lossRoiBadge) lossRoiBadge.textContent = res.roiBadge;

  const lossRoiTitle = document.getElementById("loss-roi-title");
  if (lossRoiTitle) lossRoiTitle.innerHTML = res.roiTitle;

  const lossRoiDesc = document.getElementById("loss-roi-desc");
  if (lossRoiDesc) lossRoiDesc.innerHTML = res.roiDesc;

  const lossRoiCta = document.getElementById("loss-roi-cta-btn");
  if (lossRoiCta) lossRoiCta.textContent = res.roiCta;

  // Audits and Sidebar (Price dynamically converted)
  const auditsHeading = document.getElementById("res-audits-heading");
  if (auditsHeading) auditsHeading.textContent = res.auditsHeading;

  const resSidebarBadge = document.getElementById("res-sidebar-badge");
  if (resSidebarBadge) resSidebarBadge.textContent = res.sidebarBadge;

  const resSidebarTitle = document.getElementById("res-sidebar-title");
  if (resSidebarTitle) resSidebarTitle.textContent = res.sidebarTitle;

  const resSidebarDesc = document.getElementById("res-sidebar-desc");
  if (resSidebarDesc) resSidebarDesc.innerHTML = res.sidebarDesc;

  const resSidebarCta = document.getElementById("res-sidebar-cta-btn");
  if (resSidebarCta) resSidebarCta.textContent = res.sidebarCta;

  // If results data is already loaded in DOM, update dynamic values as well:
  if (window.currentDiagnosticData) {
    const data = window.currentDiagnosticData;
    const topRank = data.metrics?.top_rank_achieved;
    const topRankElem = document.getElementById("res-top-rank");
    if (topRankElem) {
      if (topRank) {
        topRankElem.textContent = l === "en" ? `#${topRank} Rank` : `#${topRank}º Lugar`;
      } else {
        topRankElem.textContent = res.notRanked;
      }
    }

    const sprintBadge = document.getElementById("res-sprint-badge");
    if (sprintBadge) {
      const day = data.company?.sprint_day_current || (data.company?.is_paid ? 14 : 0);
      sprintBadge.textContent = `${res.dayPrefix} ${day}/14`;
    }

    const clientsElem = document.getElementById("loss-clients-count");
    if (clientsElem && window.currentLossEstimatedClients) {
      clientsElem.textContent = `~ ${window.currentLossEstimatedClients} ${res.clientsPerMonth}`;
    }

    const searchElem = document.getElementById("loss-search-volume");
    if (searchElem && window.currentLossSearchCount) {
      const searchUnit = l === "en" ? "searches" : (l === "es" ? "búsquedas" : "buscas");
      searchElem.textContent = `~ ${window.currentLossSearchCount.toLocaleString(dict.locale || "pt-BR")} ${searchUnit}`;
    }
  }

  // Also update loss calculation ticket display with right currency
  const slider = document.getElementById("loss-ticket-slider");
  if (slider && typeof window.updateLossCalculation === "function") {
    window.updateLossCalculation(slider.value || dict.defaultTicket);
  }
};

function applyLanguage(lang) {
  const dict = I18N[lang] || I18N.pt;

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
    marqueeTrack.innerHTML = dict.marquee
      .map((item) => `<span class="inline-flex items-center gap-1.5">${item}</span>`)
      .join('<span class="text-emerald-500">•</span>');
  }

  // Navbar
  const navBadge = document.getElementById("nav-badge-text");
  if (navBadge) navBadge.textContent = dict.navBadge;

  const navSub = document.getElementById("nav-sub-text");
  if (navSub) navSub.textContent = dict.navSub;

  const linkVideo = document.getElementById("nav-link-video");
  if (linkVideo) linkVideo.textContent = dict.navLinkVideo;

  const linkChallenge = document.getElementById("nav-link-challenge");
  if (linkChallenge) linkChallenge.textContent = dict.navLinkChallenge;

  const linkHow = document.getElementById("nav-link-how");
  if (linkHow) linkHow.textContent = dict.navLinkHow;

  const linkDir = document.getElementById("nav-link-dir");
  if (linkDir) linkDir.textContent = dict.navLinkDir;

  const navDemo = document.getElementById("nav-demo-btn");
  if (navDemo) navDemo.textContent = dict.navDemoBtn;

  const navCta = document.getElementById("nav-cta-btn");
  if (navCta) navCta.textContent = dict.navCtaBtn;

  // Hero Section
  const heroBadge = document.getElementById("hero-badge-pill");
  if (heroBadge) heroBadge.textContent = dict.heroBadgePill;

  const heroBadgeDesc = document.getElementById("hero-badge-desc");
  if (heroBadgeDesc) heroBadgeDesc.textContent = dict.heroBadgeDesc;

  const heroHeadline = document.getElementById("hero-headline");
  if (heroHeadline) heroHeadline.innerHTML = dict.heroHeadline;

  const heroPara = document.getElementById("hero-paragraph");
  if (heroPara) heroPara.innerHTML = dict.heroParagraph;

  const heroVidTitle = document.getElementById("hero-video-title");
  if (heroVidTitle) heroVidTitle.textContent = dict.heroVideoTitle;

  const vidHd = document.getElementById("video-hd-badge");
  if (vidHd && dict.videoHdBadge) vidHd.textContent = dict.videoHdBadge;

  const vidBadge = document.getElementById("video-overlay-badge") || document.getElementById("video-badge-text");
  if (vidBadge) vidBadge.textContent = dict.videoBadge;

  const vidListen = document.getElementById("video-overlay-listen") || document.getElementById("video-listen-tip");
  if (vidListen) vidListen.textContent = dict.videoListen;

  const vidWatch = document.getElementById("video-overlay-watch-btn");
  if (vidWatch && dict.videoWatchBtn) vidWatch.textContent = dict.videoWatchBtn;

  const vidQuote = document.getElementById("video-overlay-quote");
  if (vidQuote && dict.videoQuote) vidQuote.innerHTML = dict.videoQuote;

  // Troca dinâmica do vídeo dublado para o idioma selecionado
  const videoElem = document.getElementById("hero-pitch-video") || document.getElementById("apresentacao-video");
  if (videoElem) {
    const videoSrcMap = {
      pt: "/static/videos/apresentacao.mp4",
      en: "/static/videos/apresentacao_en.mp4",
      es: "/static/videos/apresentacao_es.mp4"
    };
    const targetSrc = videoSrcMap[lang] || videoSrcMap.pt;
    const currentSrc = videoElem.getAttribute("src");
    if (currentSrc !== targetSrc) {
      videoElem.src = targetSrc;
      const sourceElem = document.getElementById("video-source-main");
      if (sourceElem) sourceElem.src = targetSrc;
      videoElem.load();
    }
  }

  // SIMULADOR DO DESAFIO (Imagem do usuário)
  const simHBadge = document.getElementById("hero-sim-header-badge");
  if (simHBadge && dict.sim) simHBadge.textContent = dict.sim.headerBadge;

  const simHTitle = document.getElementById("hero-sim-header-title");
  if (simHTitle && dict.sim) simHTitle.textContent = dict.sim.headerTitle;

  const simExpTitle = document.getElementById("sim-explain-title");
  if (simExpTitle && dict.sim) simExpTitle.innerHTML = dict.sim.explainTitle;

  const simExpDesc = document.getElementById("sim-explain-desc");
  if (simExpDesc && dict.sim) simExpDesc.innerHTML = dict.sim.explainDesc;

  if (typeof window.renderHeroSim === "function") {
    window.renderHeroSim(window.heroSimCurrentMode || "before", lang);
  }

  // Formulário de Auditoria & Presets
  const step1 = document.getElementById("step1-badge");
  if (step1 && dict.step1Badge) step1.textContent = dict.step1Badge;

  const formTitle = document.getElementById("form-main-title");
  if (formTitle && dict.formMainTitle) formTitle.textContent = dict.formMainTitle;

  const btnAdv = document.getElementById("btn-preset-adv");
  if (btnAdv && dict.presets) btnAdv.textContent = dict.presets.adv;

  const btnClinica = document.getElementById("btn-preset-clinica");
  if (btnClinica && dict.presets) btnClinica.textContent = dict.presets.clinica;

  const btnDemo = document.getElementById("btn-demo-sim");
  if (btnDemo && dict.presets) btnDemo.textContent = dict.presets.demo;

  const btnCompTxt = document.getElementById("btn-type-company-text");
  if (btnCompTxt && dict.entityButtons) btnCompTxt.textContent = dict.entityButtons.company;

  const btnAutoTxt = document.getElementById("btn-type-autonomous-text");
  if (btnAutoTxt && dict.entityButtons) btnAutoTxt.textContent = dict.entityButtons.autonomous;

  // Atualiza labels de acordo com o tipo ativo (empresa ou autônomo)
  const curType = document.getElementById("entity_type")?.value || "company";
  if (typeof window.applyEntityLabelsI18n === "function") {
    window.applyEntityLabelsI18n(curType, dict);
  }

  // Contato e Envio do formulário
  const lblWpp = document.getElementById("label-whatsapp");
  if (lblWpp && dict.contact) lblWpp.textContent = dict.contact.whatsapp;

  const inpWpp = document.getElementById("whatsapp");
  if (inpWpp && dict.contact) inpWpp.placeholder = dict.contact.whatsappPlaceholder;

  const lblMail = document.getElementById("label-email");
  if (lblMail && dict.contact) lblMail.textContent = dict.contact.email;

  const inpMail = document.getElementById("email");
  if (inpMail && dict.contact) inpMail.placeholder = dict.contact.emailPlaceholder;

  const secNote = document.getElementById("form-security-note");
  if (secNote && dict.contact) secNote.textContent = dict.contact.securityNote;

  const subBtn = document.getElementById("submit-audit-btn");
  if (subBtn && dict.contact) subBtn.textContent = dict.contact.submitBtn;

  // 14-Day Section Header & Grid (Image 1)
  const spBadge = document.getElementById("sprint-section-badge");
  if (spBadge && dict.sprintSection) spBadge.textContent = dict.sprintSection.badge;

  const spTitle = document.getElementById("sprint-section-title");
  if (spTitle && dict.sprintSection) spTitle.textContent = dict.sprintSection.title;

  const spSubtitle = document.getElementById("sprint-section-subtitle");
  if (spSubtitle && dict.sprintSection) spSubtitle.textContent = dict.sprintSection.subtitle;

  if (typeof window.render14DaySchedule === "function") {
    window.render14DaySchedule(lang);
  }

  // Diagnostic Results (Image 2)
  if (typeof window.updateResultsI18n === "function") {
    window.updateResultsI18n(lang);
  }

  // Loss Calculator
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

  // Floating Chat Pill at bottom
  const floatChatBtn = document.getElementById("floating-chat-btn-text");
  if (floatChatBtn && dict.floatingChatPill) floatChatBtn.textContent = dict.floatingChatPill;

  // Modal de Carregamento (Loading)
  if (dict.loading) {
    const ldBadge = document.getElementById("diag-load-badge");
    if (ldBadge) ldBadge.textContent = dict.loading.badge;
    const ldTitle = document.getElementById("diag-load-title");
    if (ldTitle) ldTitle.textContent = dict.loading.title;
    const ldSub = document.getElementById("diag-load-subtitle");
    if (ldSub) ldSub.textContent = dict.loading.initSub;
    const ldFoot = document.getElementById("diag-load-footer");
    if (ldFoot) ldFoot.textContent = dict.loading.footer;
  }

  // Chat Flutuante
  const chatHeaderTitle = document.getElementById("ai-chat-header-title");
  if (chatHeaderTitle && dict.chat) chatHeaderTitle.textContent = dict.chat.title;

  const chatHeaderStatus = document.getElementById("ai-chat-header-status");
  if (chatHeaderStatus && dict.chat) chatHeaderStatus.textContent = dict.chat.online;

  const chatWelcome = document.getElementById("ai-chat-welcome-msg");
  if (chatWelcome && dict.chat) chatWelcome.textContent = dict.chat.welcome;

  const chatQuickBtns = document.getElementById("ai-chat-quick-btns");
  if (chatQuickBtns && dict.chat && dict.chat.quickBtns) {
    chatQuickBtns.innerHTML = dict.chat.quickBtns.map((b) =>
      `<button type="button" onclick="sendQuickChatMessage('${b.msg.replace(/'/g, "\'")}')" class="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-emerald-50 text-slate-700 whitespace-nowrap">${b.label}</button>`
    ).join("");
  }

  const chatInput = document.getElementById("ai-chat-input");
  if (chatInput && dict.chat) chatInput.placeholder = dict.chat.inputPlaceholder;

  const chatSendBtn = document.getElementById("ai-chat-send-btn");
  if (chatSendBtn && dict.chat && dict.chat.sendBtn) chatSendBtn.textContent = dict.chat.sendBtn;

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
  if (mpBtn) {
    const isBump = window.currentOrderBump || false;
    const price = dict.planPrice + (isBump ? dict.bumpPrice : 0);
    if (lang === "en") {
      mpBtn.innerHTML = `<span>💳</span> Pay with PayPal or Card ($${price.toFixed(2)} USD)`;
    } else if (lang === "es") {
      mpBtn.innerHTML = `<span>💳</span> Pagar con PayPal o Tarjeta ($${price.toFixed(2)} USD)`;
    } else {
      mpBtn.innerHTML = `<span>💳</span> ${dict.checkout.mpBtn.replace("💳 ", "")}`;
    }
  }

  const pixBox = document.getElementById("pix-payment-box");
  if (pixBox) {
    if (lang === "pt") {
      pixBox.style.display = "block";
    } else {
      pixBox.style.display = "none";
    }
  }

  const chFootGuar = document.getElementById("checkout-footer-guar");
  if (chFootGuar && dict.checkout?.footerGuar) chFootGuar.textContent = dict.checkout.footerGuar;

  const chFootSec = document.getElementById("checkout-footer-sec");
  if (chFootSec && dict.checkout?.footerSec) chFootSec.textContent = dict.checkout.footerSec;

  const modalTotal = document.getElementById("modal-total-display");
  if (modalTotal) {
    const isBump = window.currentOrderBump || false;
    const price = dict.planPrice + (isBump ? dict.bumpPrice : 0);
    modalTotal.textContent = dict.currencyCode === "BRL"
      ? price.toFixed(2).replace(".", ",")
      : `${price.toFixed(2)} ${dict.currencyCode}`;
  }
}
