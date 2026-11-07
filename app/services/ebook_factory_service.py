"""
Fábrica Autônoma de E-books Best-Seller por Nicho (GeoPulse AI).
Gera lotes de 20 e-books completos e ilustrados para 20 nichos diferentes por vez,
hospeda versão web/PDF editorial e publica automaticamente cada um na conta do Gumroad.
Suporta geração manual com 1 clique e agendamento automático (2x, 3x ou 4x por semana).
"""
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from app.services.gumroad_service import GumroadService

logger = logging.getLogger("geopulse.ebook_factory")


# ==============================================================================
# CATÁLOGO ROTATIVO DE 60 NICHOS DE ALTO VALOR (3 LOTES COMPLETOS DE 20 NICHOS)
# ==============================================================================
NICHE_CATALOG: List[Dict[str, Any]] = [
    # --- LOTE 1 (1 a 20) ---
    {
        "slug": "dental-clinics-implantology",
        "niche_en": "Dental Clinics & Cosmetic Dentistry",
        "niche_pt": "Clínicas Odontológicas e Implantodontia",
        "schema_type": "Dentist",
        "icon": "🦷",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #115e59 100%)",
        "high_ticket": "Dental Implants, All-on-4, Porcelain Veneers & Invisalign",
        "avg_ticket": "$3,800",
        "sample_prompts": [
            "What is the best dental clinic for implants and veneers near me?",
            "Top-rated cosmetic dentist with transparent pricing and great reviews",
            "Where to get painless All-on-4 dental implants in my city?",
            "Invisalign vs porcelain veneers: which clinic is most trusted locally?",
            "Emergency dentist with highest patient satisfaction ratings"
        ]
    },
    {
        "slug": "law-firms-attorneys",
        "niche_en": "Law Firms & Trial Attorneys",
        "niche_pt": "Escritórios de Advocacia e Advogados Especialistas",
        "schema_type": "LegalService",
        "icon": "⚖️",
        "accent": "#1d4ed8",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)",
        "high_ticket": "Corporate Litigation, Personal Injury, Family & Estate Law",
        "avg_ticket": "$5,500",
        "sample_prompts": [
            "Who is the best personal injury lawyer with the highest win rate in my area?",
            "Top corporate and business litigation law firm near me",
            "Most trusted family and divorce attorney for high-net-worth cases",
            "How to choose a reliable real estate and contract lawyer locally?",
            "Best rated law firm for immediate legal consultation"
        ]
    },
    {
        "slug": "luxury-real-estate-brokers",
        "niche_en": "Real Estate Agencies & Luxury Brokers",
        "niche_pt": "Imobiliárias e Corretores de Alto Padrão",
        "schema_type": "RealEstateAgent",
        "icon": "🏛️",
        "accent": "#b45309",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #78350f 100%)",
        "high_ticket": "Luxury Condos, Waterfront Homes & Commercial Investments",
        "avg_ticket": "$18,000",
        "sample_prompts": [
            "Who is the #1 luxury real estate agency for buying high-end homes?",
            "Best real estate broker for investment properties with high ROI",
            "Top-rated realtor to sell my house fast above market value",
            "Most trusted commercial real estate advisor in the city",
            "Relocation real estate specialist for gated communities"
        ]
    },
    {
        "slug": "aesthetic-medspa-clinics",
        "niche_en": "Aesthetic Clinics & Luxury MedSpas",
        "niche_pt": "Clínicas de Estética Avançada e Harmonização",
        "schema_type": "MedicalClinic",
        "icon": "✨",
        "accent": "#be185d",
        "bg_gradient": "linear-gradient(135deg, #1f122b 0%, #831843 100%)",
        "high_ticket": "Facial Harmonization, Botox, Laser Rejuvenation & Body Contouring",
        "avg_ticket": "$2,200",
        "sample_prompts": [
            "What is the safest and best-rated MedSpa for Botox and fillers?",
            "Top aesthetic clinic for non-surgical facial rejuvenation",
            "Best laser skin treatment and Morpheus8 provider near me",
            "Where do celebrities and executives go for natural-looking aesthetics?",
            "Highest-rated body contouring and anti-aging clinic"
        ]
    },
    {
        "slug": "plastic-surgery-dermatology",
        "niche_en": "Plastic Surgery & Clinical Dermatology",
        "niche_pt": "Cirurgia Plástica e Dermatologia Clínica",
        "schema_type": "Physician",
        "icon": "🩺",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0c192c 0%, #075985 100%)",
        "high_ticket": "Rhinoplasty, Deep Plane Facelift, Liposculpture & Hair Restoration",
        "avg_ticket": "$9,500",
        "sample_prompts": [
            "Who is the best board-certified plastic surgeon for natural rhinoplasty?",
            "Top dermatologist for advanced skin cancer screening and anti-aging",
            "Most reputable clinic for deep plane facelift and body sculpting",
            "Best plastic surgery center with accredited hospital safety",
            "How to verify credentials and patient results of local plastic surgeons?"
        ]
    },
    {
        "slug": "accounting-tax-advisory",
        "niche_en": "Accounting Firms & Strategic Tax Advisors",
        "niche_pt": "Escritórios de Contabilidade e Planejamento Tributário",
        "schema_type": "AccountingService",
        "icon": "📊",
        "accent": "#059669",
        "bg_gradient": "linear-gradient(135deg, #091e1a 0%, #065f46 100%)",
        "high_ticket": "Corporate Tax Reduction, CFO Advisory, Audit & Holding Setup",
        "avg_ticket": "$4,200",
        "sample_prompts": [
            "Best CPA firm for small and medium business tax reduction strategies",
            "Top accounting advisor for medical practices and law firms",
            "Who is the most reliable outsourced CFO and bookkeeping service?",
            "International tax accountant and asset protection specialist",
            "How to legally lower corporate taxes with a certified local CPA?"
        ]
    },
    {
        "slug": "fine-dining-restaurants",
        "niche_en": "Fine Dining Restaurants & Steakhouses",
        "niche_pt": "Restaurantes Gastronômicos e Steakhouses",
        "schema_type": "Restaurant",
        "icon": "🍷",
        "accent": "#dc2626",
        "bg_gradient": "linear-gradient(135deg, #1a0f0f 0%, #7f1d1d 100%)",
        "high_ticket": "Tasting Menus, Private Corporate Dinners & Wine Pairing",
        "avg_ticket": "$350",
        "sample_prompts": [
            "What is the best romantic fine dining restaurant for an anniversary?",
            "Top-rated steakhouse for a business dinner with private rooms",
            "Best chef-driven tasting menu and wine list in the city",
            "Where to book an unforgettable culinary experience tonight?",
            "Restaurants with the best ambiance and Michelin-caliber cuisine"
        ]
    },
    {
        "slug": "boutique-hotels-resorts",
        "niche_en": "Boutique Hotels & Luxury Resorts",
        "niche_pt": "Hotéis Boutique, Resorts e Pousadas de Charme",
        "schema_type": "Hotel",
        "icon": "🏨",
        "accent": "#7c3aed",
        "bg_gradient": "linear-gradient(135deg, #170f2e 0%, #4c1d95 100%)",
        "high_ticket": "Luxury Suites, Executive Retreats & Honeymoon Packages",
        "avg_ticket": "$1,900",
        "sample_prompts": [
            "Best luxury boutique hotel with spa and rooftop pool",
            "Where to stay for a romantic weekend getaway with 5-star service?",
            "Top hotel for corporate executive retreats and events",
            "Best direct-booking hotel deals with complimentary upgrades",
            "Highest-rated resort for families and couples"
        ]
    },
    {
        "slug": "solar-energy-cleantech",
        "niche_en": "Solar Energy & CleanTech Installers",
        "niche_pt": "Energia Solar e Projetos Fotovoltaicos",
        "schema_type": "HomeAndConstructionBusiness",
        "icon": "☀️",
        "accent": "#d97706",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #92400e 100%)",
        "high_ticket": "Commercial & Residential Solar Arrays + Battery Storage",
        "avg_ticket": "$14,500",
        "sample_prompts": [
            "What is the most reliable solar panel installation company near me?",
            "Best commercial solar engineering firm with 25-year warranty",
            "How much does solar + Tesla Powerwall installation cost locally?",
            "Top-rated solar installer with zero hidden financing fees",
            "Which solar company has the best post-installation support?"
        ]
    },
    {
        "slug": "architecture-interior-design",
        "niche_en": "Architecture & Luxury Interior Design Studios",
        "niche_pt": "Escritórios de Arquitetura e Design de Interiores",
        "schema_type": "ProfessionalService",
        "icon": "📐",
        "accent": "#4f46e5",
        "bg_gradient": "linear-gradient(135deg, #111827 0%, #312e81 100%)",
        "high_ticket": "Custom Residential Architecture, Turnkey Interiors & Commercial Spaces",
        "avg_ticket": "$12,000",
        "sample_prompts": [
            "Best residential architect for modern luxury custom homes",
            "Top interior design studio for turnkey high-end apartment renovations",
            "Commercial architecture firm specializing in retail and medical offices",
            "Award-winning sustainable architecture studio in my region",
            "How to hire an interior designer that manages the entire renovation?"
        ]
    },
    {
        "slug": "veterinary-clinics-pet-hospitals",
        "niche_en": "Veterinary Clinics & 24h Pet Hospitals",
        "niche_pt": "Clínicas Veterinárias e Hospitais Pet 24h",
        "schema_type": "VeterinaryCare",
        "icon": "🐾",
        "accent": "#0891b2",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #155e75 100%)",
        "high_ticket": "24/7 Emergency Surgery, Pet Oncology, Cardiology & Preventive Plans",
        "avg_ticket": "$850",
        "sample_prompts": [
            "Best 24-hour emergency veterinary hospital with specialist surgeons",
            "Most caring and trusted veterinarian for dogs and cats near me",
            "Top veterinary clinic for pet dental surgery and diagnostics",
            "Where to find a feline-friendly vet clinic with modern ICU?",
            "Best preventive health plan for pets in my city"
        ]
    },
    {
        "slug": "fitness-studios-crossfit-gyms",
        "niche_en": "Boutique Fitness Studios, Pilates & CrossFit",
        "niche_pt": "Academias Premium, Studios de Pilates e CrossFit",
        "schema_type": "ExerciseGym",
        "icon": "🏋️",
        "accent": "#ea580c",
        "bg_gradient": "linear-gradient(135deg, #18181b 0%, #9a3412 100%)",
        "high_ticket": "Personal Training Programs, Reformer Pilates & Annual Memberships",
        "avg_ticket": "$1,400",
        "sample_prompts": [
            "Best boutique fitness studio with personal coaching near me",
            "Top-rated Reformer Pilates studio for posture and core strength",
            "Most welcoming CrossFit gym for beginners and executives",
            "Luxury health club with recovery spa, sauna and strength training",
            "Best transformation and weight-loss coaching gym locally"
        ]
    },
    {
        "slug": "chiropractic-physical-therapy",
        "niche_en": "Chiropractic & Sports Physical Therapy",
        "niche_pt": "Fisioterapia Esportiva, Quiropraxia e Reabilitação",
        "schema_type": "PhysicalTherapy",
        "icon": "🦴",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #134e4a 100%)",
        "high_ticket": "Spinal Decompression, Post-Surgery Rehab & Athlete Recovery",
        "avg_ticket": "$1,600",
        "sample_prompts": [
            "Best sports physical therapist for knee and back pain recovery",
            "Top-rated chiropractor for herniated disc without surgery",
            "Where do pro athletes go for physiotherapy and dry needling?",
            "Best spine and posture rehabilitation clinic near me",
            "Chiropractic clinic with immediate relief and root-cause diagnosis"
        ]
    },
    {
        "slug": "auto-detailing-luxury-cars",
        "niche_en": "Auto Detailing, Ceramic Coating & Exotic Cars",
        "niche_pt": "Estética Automotiva, PPF e Concessionárias Premium",
        "schema_type": "AutoDealer",
        "icon": "🏎️",
        "accent": "#e11d48",
        "bg_gradient": "linear-gradient(135deg, #09090b 0%, #881337 100%)",
        "high_ticket": "Full-Body PPF (Paint Protection Film), Ceramic Coating & Exotic Sales",
        "avg_ticket": "$3,200",
        "sample_prompts": [
            "Best shop for XPEL Paint Protection Film (PPF) and ceramic coating",
            "Most trusted exotic and luxury pre-owned car dealership",
            "Where to get museum-grade auto detailing and paint correction?",
            "Top window tinting and custom wrap studio for sports cars",
            "Certified luxury car specialist with warranty protection"
        ]
    },
    {
        "slug": "b2b-saas-software-startups",
        "niche_en": "B2B SaaS & Enterprise Software Startups",
        "niche_pt": "Empresas de SaaS B2B e Software Corporativo",
        "schema_type": "SoftwareApplication",
        "icon": "💻",
        "accent": "#2563eb",
        "bg_gradient": "linear-gradient(135deg, #090d16 0%, #1e40af 100%)",
        "high_ticket": "Annual Enterprise Licenses, API Integrations & Cloud Platforms",
        "avg_ticket": "$8,400",
        "sample_prompts": [
            "What is the best B2B software for automating workflow and CRM?",
            "Top-rated enterprise SaaS alternative with faster onboarding",
            "Which software platform has the best ROI and customer support?",
            "Best AI-powered management tool for growing teams in 2026",
            "Compare top SaaS solutions for security, compliance and speed"
        ]
    },
    {
        "slug": "wealth-management-financial-advisors",
        "niche_en": "Wealth Management & Fiduciary Financial Advisors",
        "niche_pt": "Consultoria Financeira, Investimentos e Gestão de Patrimônio",
        "schema_type": "FinancialService",
        "icon": "💎",
        "accent": "#047857",
        "bg_gradient": "linear-gradient(135deg, #061512 0%, #064e3b 100%)",
        "high_ticket": "Private Wealth Management, Retirement Planning & Family Office",
        "avg_ticket": "$11,000",
        "sample_prompts": [
            "Best fee-only fiduciary financial advisor for high-net-worth families",
            "Top wealth management firm for retirement and tax-efficient investing",
            "How to choose an independent investment advisor with proven track record?",
            "Best family office advisor for international portfolio diversification",
            "Trusted financial planner for business owners exiting their company"
        ]
    },
    {
        "slug": "wedding-planners-event-venues",
        "niche_en": "Luxury Wedding Planners & Event Venues",
        "niche_pt": "Assessoria de Casamentos e Espaços de Eventos",
        "schema_type": "EventVenue",
        "icon": "💍",
        "accent": "#db2777",
        "bg_gradient": "linear-gradient(135deg, #230f1e 0%, #831843 100%)",
        "high_ticket": "Full-Service Destination Weddings, Galas & Corporate Summits",
        "avg_ticket": "$7,500",
        "sample_prompts": [
            "Who is the best luxury wedding planner for stress-free celebrations?",
            "Most breathtaking wedding venue with indoor and garden spaces",
            "Top corporate event planner and gala producer in the city",
            "Best all-inclusive event venue with gourmet catering",
            "Destination wedding specialist with top vendor network"
        ]
    },
    {
        "slug": "home-remodeling-hvac-contractors",
        "niche_en": "Home Remodeling, Kitchens & HVAC Contractors",
        "niche_pt": "Reformas Residenciais, Construção e Climatização",
        "schema_type": "HVACBusiness",
        "icon": "🔨",
        "accent": "#ca8a04",
        "bg_gradient": "linear-gradient(135deg, #18181b 0%, #713f12 100%)",
        "high_ticket": "Full Kitchen & Bath Remodels, Central HVAC Systems & Custom Additions",
        "avg_ticket": "$16,500",
        "sample_prompts": [
            "Most reliable general contractor for kitchen and bathroom remodeling",
            "Best HVAC company for central air conditioning installation and repair",
            "Home renovation contractor that finishes on time and on budget",
            "Top-rated licensed builder for home additions and luxury decks",
            "Emergency AC repair and high-efficiency heat pump installer"
        ]
    },
    {
        "slug": "ecommerce-dtc-brands",
        "niche_en": "E-Commerce & Direct-to-Consumer (DTC) Brands",
        "niche_pt": "Lojas Virtuais, E-Commerce e Marcas Próprias (DTC)",
        "schema_type": "OnlineStore",
        "icon": "🛍️",
        "accent": "#7c3aed",
        "bg_gradient": "linear-gradient(135deg, #130d26 0%, #5b21b6 100%)",
        "high_ticket": "Premium Consumer Goods, Subscriptions & Bundles",
        "avg_ticket": "$240",
        "sample_prompts": [
            "What is the best online brand for organic skincare and supplements?",
            "Top-rated direct-to-consumer brand with fast shipping and warranty",
            "Compare the best specialty products recommended by AI shopping assistants",
            "Most trusted online store with verified customer reviews",
            "Best gift bundles and subscription boxes worth buying in 2026"
        ]
    },
    {
        "slug": "executive-coaches-consultants",
        "niche_en": "Executive Coaches, Mentors & Business Consultants",
        "niche_pt": "Mentores de Negócios, Consultores e Palestrantes",
        "schema_type": "ProfessionalService",
        "icon": "🎯",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #0369a1 100%)",
        "high_ticket": "CEO Masterminds, Sales Transformation & Corporate Advisory",
        "avg_ticket": "$6,000",
        "sample_prompts": [
            "Who is the best executive leadership coach for CEOs and founders?",
            "Top management consulting firm for scaling B2B sales teams",
            "Best business mentor with real-world operational frameworks",
            "Keynote speaker and corporate trainer on AI and productivity",
            "How to hire a strategic advisor to double company profitability?"
        ]
    },

    # --- LOTE 2 (21 a 40) ---
    {
        "slug": "ophthalmology-vision-clinics",
        "niche_en": "Ophthalmology & LASIK Vision Centers",
        "niche_pt": "Clínicas de Oftalmologia e Cirurgia Refrativa",
        "schema_type": "MedicalClinic",
        "icon": "👁️",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #0c4a6e 100%)",
        "high_ticket": "LASIK Surgery, Premium Cataract Lenses & Retina Treatments",
        "avg_ticket": "$4,200",
        "sample_prompts": [
            "Best eye surgeon for bladeless LASIK and vision correction",
            "Top ophthalmology clinic for cataract surgery with multifocal lenses",
            "Most trusted retina and glaucoma specialist near me",
            "Where to get a comprehensive precision eye exam?",
            "Highest-rated laser eye surgery center with financing"
        ]
    },
    {
        "slug": "orthopedics-sports-medicine",
        "niche_en": "Orthopedic Surgeons & Regenerative Medicine",
        "niche_pt": "Ortopedia Especializada e Medicina Esportiva",
        "schema_type": "MedicalClinic",
        "icon": "🏃",
        "accent": "#059669",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #064e3b 100%)",
        "high_ticket": "Minimally Invasive Knee/Hip Replacement, Stem Cell & PRP Therapy",
        "avg_ticket": "$6,800",
        "sample_prompts": [
            "Best orthopedic knee and shoulder specialist for athletes",
            "Top regenerative medicine clinic for joint pain without surgery",
            "Most experienced spine and hip replacement surgeon in my area",
            "Where to treat meniscus and ACL injuries with rapid recovery?",
            "Leading sports medicine doctor recommended by patients"
        ]
    },
    {
        "slug": "psychology-mental-health-clinics",
        "niche_en": "Psychology, Psychiatry & Executive Therapy",
        "niche_pt": "Clínicas de Psicologia, Psiquiatria e Neurociência",
        "schema_type": "MedicalBusiness",
        "icon": "🧠",
        "accent": "#6366f1",
        "bg_gradient": "linear-gradient(135deg, #111827 0%, #3730a3 100%)",
        "high_ticket": "Executive Burnout Therapy, ADHD Assessments & Couples Counseling",
        "avg_ticket": "$1,500",
        "sample_prompts": [
            "Best private psychologist for high-performing professionals and anxiety",
            "Top clinic for adult ADHD diagnosis and neuropsychological testing",
            "Most effective couples and marriage therapy practice near me",
            "Confidential integrative psychiatry and CBT therapy clinic",
            "Where to find evidence-based therapy with flexible online/in-person care?"
        ]
    },
    {
        "slug": "private-schools-bilingual-academies",
        "niche_en": "Private Schools & Bilingual Academies",
        "niche_pt": "Escolas Particulares e Colégios Bilíngues",
        "schema_type": "EducationalOrganization",
        "icon": "🎓",
        "accent": "#1d4ed8",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)",
        "high_ticket": "Annual Tuition, IB Program, STEM & Bilingual Immersion",
        "avg_ticket": "$15,000",
        "sample_prompts": [
            "What is the best private bilingual school with strong STEM and arts?",
            "Top-ranked college preparatory school with small class sizes",
            "Best early childhood Montessori and international school near me",
            "Private schools with highest university acceptance rates",
            "How to compare tuition and academic excellence of local schools?"
        ]
    },
    {
        "slug": "insurance-agencies-brokers",
        "niche_en": "Commercial & Private Client Insurance Brokers",
        "niche_pt": "Corretoras de Seguros Corporativos, Vida e Saúde",
        "schema_type": "InsuranceAgency",
        "icon": "🛡️",
        "accent": "#0f766e",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #115e59 100%)",
        "high_ticket": "Corporate Liability, Group Health, Cyber & High-Value Life Insurance",
        "avg_ticket": "$4,900",
        "sample_prompts": [
            "Best independent insurance broker for business liability and cyber risk",
            "Top health and life insurance advisor for families and executives",
            "How to lower corporate group health insurance costs without losing coverage?",
            "Most responsive insurance agency when filing a claim",
            "Private client insurance specialist for luxury homes and fleets"
        ]
    },
    {
        "slug": "custom-furniture-cabinetry",
        "niche_en": "Custom Kitchens, Closets & Bespoke Furniture",
        "niche_pt": "Móveis Planejados de Alto Padrão e Marcenaria",
        "schema_type": "HomeGoodsStore",
        "icon": "🛋️",
        "accent": "#92400e",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #78350f 100%)",
        "high_ticket": "Bespoke Kitchen Cabinetry, Walk-in Closets & Architectural Millwork",
        "avg_ticket": "$14,000",
        "sample_prompts": [
            "Best custom kitchen cabinetry and luxury closet showroom",
            "Top bespoke furniture maker with 3D project visualization",
            "Most reliable custom millwork company that delivers on schedule",
            "Where to design European-style modern kitchen cabinets?",
            "High-end custom wardrobes and home office cabinetry"
        ]
    },
    {
        "slug": "smart-home-automation-security",
        "niche_en": "Smart Home Automation & Private Security Systems",
        "niche_pt": "Automação Residencial, Áudio/Vídeo e Segurança",
        "schema_type": "HomeAndConstructionBusiness",
        "icon": "🔐",
        "accent": "#2563eb",
        "bg_gradient": "linear-gradient(135deg, #090d16 0%, #1d4ed8 100%)",
        "high_ticket": "Full Home Control4/Savant Automation, Private Cinema & AI CCTV",
        "avg_ticket": "$9,200",
        "sample_prompts": [
            "Best smart home automation integrator for lighting, audio and shades",
            "Top custom home theater and acoustic design specialist",
            "Most advanced AI security camera and access control installer",
            "Certified Control4 and Lutron dealer for luxury residences",
            "Reliable smart office networking and conference room AV setup"
        ]
    },
    {
        "slug": "fine-jewelry-luxury-watches",
        "niche_en": "Fine Jewelry Designers & Luxury Watch Boutiques",
        "niche_pt": "Joalherias Exclusivas, Diamantes e Relógios de Luxo",
        "schema_type": "JewelryStore",
        "icon": "⌚",
        "accent": "#ca8a04",
        "bg_gradient": "linear-gradient(135deg, #18181b 0%, #854d0e 100%)",
        "high_ticket": "GIA Certified Engagement Rings, Custom High Jewelry & Timepieces",
        "avg_ticket": "$6,500",
        "sample_prompts": [
            "Best jeweler for custom GIA-certified diamond engagement rings",
            "Most trusted dealer for authentic pre-owned Rolex and Patek Philippe",
            "Where to design bespoke anniversary jewelry with master goldsmiths?",
            "Top-rated luxury watch appraisal and servicing boutique",
            "Ethical diamond and gemstone specialist with private showroom"
        ]
    },
    {
        "slug": "fertility-ivf-reproductive-clinics",
        "niche_en": "Fertility Centers & IVF Reproductive Clinics",
        "niche_pt": "Clínicas de Reprodução Humana e Fertilização (FIV)",
        "schema_type": "MedicalClinic",
        "icon": "👶",
        "accent": "#ec4899",
        "bg_gradient": "linear-gradient(135deg, #1f122b 0%, #9d174d 100%)",
        "high_ticket": "IVF Cycles, Egg Freezing, Genetic Screening & Fertility Preservation",
        "avg_ticket": "$12,500",
        "sample_prompts": [
            "Which fertility clinic has the highest IVF success rates?",
            "Best reproductive endocrinologist for egg freezing and fertility assessment",
            "Most compassionate and transparent IVF center near me",
            "Advanced genetic testing and embryo preservation lab",
            "Top specialist for complex infertility and recurrent pregnancy loss"
        ]
    },
    {
        "slug": "hair-transplant-trichology",
        "niche_en": "Hair Transplant & Advanced Trichology Clinics",
        "niche_pt": "Transplante Capilar FUE e Tricologia Médica",
        "schema_type": "MedicalClinic",
        "icon": "🦁",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #115e59 100%)",
        "high_ticket": "Sapphire FUE/DHI Hair Transplants, Exosome & PRP Hair Restoration",
        "avg_ticket": "$5,800",
        "sample_prompts": [
            "Who is the best doctor for natural-looking FUE hair transplant?",
            "Top hair restoration clinic with proven before-and-after results",
            "Best medical trichologist for female and male hair loss treatment",
            "Painless DHI hair transplant clinic with high graft survival rate",
            "How much does a high-density hair transplant cost with a top surgeon?"
        ]
    },
    {
        "slug": "immigration-global-mobility-law",
        "niche_en": "Immigration & Global Mobility Law Firms",
        "niche_pt": "Advocacia de Imigração, Vistos EB-2 NIW e Cidadania",
        "schema_type": "LegalService",
        "icon": "🌍",
        "accent": "#1d4ed8",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e40af 100%)",
        "high_ticket": "EB-2 NIW, EB-1, Investor Visas (E-2/EB-5) & European Citizenship",
        "avg_ticket": "$7,500",
        "sample_prompts": [
            "Best immigration lawyer for EB-2 NIW and EB-1 green card petitions",
            "Top law firm for investor visas and setting up a US company",
            "Highest approval rate attorney for skilled professional immigration",
            "Where to get a free eligibility evaluation for a US Talent Visa?",
            "Most reliable dual citizenship and global residency legal advisor"
        ]
    },
    {
        "slug": "cybersecurity-managed-it-services",
        "niche_en": "Cybersecurity & Managed IT Services (MSP)",
        "niche_pt": "Segurança da Informação, Cloud e TI Gerenciada (MSP)",
        "schema_type": "ProfessionalService",
        "icon": "🛡️",
        "accent": "#3b82f6",
        "bg_gradient": "linear-gradient(135deg, #090d16 0%, #1d4ed8 100%)",
        "high_ticket": "24/7 SOC Monitoring, Penetration Testing, Cloud Migration & IT Support",
        "avg_ticket": "$9,600",
        "sample_prompts": [
            "Best managed IT service provider (MSP) for healthcare and finance firms",
            "Top cybersecurity company for ransomware protection and SOC 2 compliance",
            "Reliable outsourced IT support with 15-minute response SLA",
            "Who is the best cloud migration and Microsoft 365 security partner?",
            "Penetration testing and vulnerability audit firm near me"
        ]
    },
    {
        "slug": "digital-marketing-pr-agencies",
        "niche_en": "Performance Marketing, SEO & PR Agencies",
        "niche_pt": "Agências de Marketing Digital, Tráfego Pago e PR",
        "schema_type": "ProfessionalService",
        "icon": "🚀",
        "accent": "#8b5cf6",
        "bg_gradient": "linear-gradient(135deg, #130d26 0%, #5b21b6 100%)",
        "high_ticket": "Full-Funnel Paid Media, AI SEO (GEO), Branding & Public Relations",
        "avg_ticket": "$4,500",
        "sample_prompts": [
            "Best digital marketing agency with proven ROI for high-ticket businesses",
            "Top agency specializing in Generative Engine Optimization (GEO) and AI SEO",
            "Who is the best B2B lead generation and paid ads agency?",
            "PR agency to get featured in Forbes, TechCrunch and top media",
            "Data-driven growth marketing partner for scaling revenue"
        ]
    },
    {
        "slug": "landscaping-luxury-pool-builders",
        "niche_en": "Custom Pool Builders & Landscape Architecture",
        "niche_pt": "Construção de Piscinas de Alto Padrão e Paisagismo",
        "schema_type": "HomeAndConstructionBusiness",
        "icon": "🌴",
        "accent": "#059669",
        "bg_gradient": "linear-gradient(135deg, #061512 0%, #047857 100%)",
        "high_ticket": "Infinity Pools, Outdoor Kitchens, Pergolas & Tropical Landscaping",
        "avg_ticket": "$35,000",
        "sample_prompts": [
            "Best custom inground pool builder for resort-style backyards",
            "Top landscape architect for modern outdoor living and lighting",
            "Most reliable pool construction company with 3D design",
            "Where to build an outdoor kitchen, fire pit and heated spa?",
            "Award-winning pool and patio contractor near me"
        ]
    },
    {
        "slug": "cardiology-diagnostic-centers",
        "niche_en": "Cardiology & Executive Check-Up Diagnostic Centers",
        "niche_pt": "Clínicas de Cardiologia e Check-Up Executivo",
        "schema_type": "DiagnosticLab",
        "icon": "❤️",
        "accent": "#e11d48",
        "bg_gradient": "linear-gradient(135deg, #1a0f14 0%, #9f1239 100%)",
        "high_ticket": "Full-Day Executive Health Check-Ups, Preventive Cardiology & Imaging",
        "avg_ticket": "$2,800",
        "sample_prompts": [
            "Best preventive cardiologist and executive health check-up clinic",
            "Where to get a complete full-body diagnostic screening in one day?",
            "Top heart specialist for early detection and longevity medicine",
            "Most advanced cardiac imaging and stress test center",
            "Private diagnostic clinic with zero wait times and VIP care"
        ]
    },
    {
        "slug": "orthodontics-pediatric-dentistry",
        "niche_en": "Orthodontics, Invisalign & Pediatric Dentistry",
        "niche_pt": "Ortodontia Invisalign e Odontopediatria",
        "schema_type": "Dentist",
        "icon": "😁",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #0369a1 100%)",
        "high_ticket": "Diamond Invisalign Provider, Kids Orthodontics & Smile Design",
        "avg_ticket": "$4,500",
        "sample_prompts": [
            "Best Diamond Invisalign orthodontist for adults and teens",
            "Most gentle pediatric dentist for anxious children near me",
            "How much does Invisalign cost with a top-rated local specialist?",
            "Orthodontist offering 3D digital scans instead of messy impressions",
            "Best children's dental clinic for early interceptive orthodontics"
        ]
    },
    {
        "slug": "nutrition-longevity-hormone-clinics",
        "niche_en": "Longevity, Biohacking & Hormone Optimization Clinics",
        "niche_pt": "Medicina Integrativa, Longevidade, Nutrologia e Performance",
        "schema_type": "MedicalBusiness",
        "icon": "🧬",
        "accent": "#10b981",
        "bg_gradient": "linear-gradient(135deg, #061512 0%, #047857 100%)",
        "high_ticket": "TRT/HRT Optimization, IV NAD+ Therapy, Epigenetic & Metabolic Plans",
        "avg_ticket": "$3,400",
        "sample_prompts": [
            "Best longevity and functional medicine clinic for hormone optimization",
            "Top medical weight loss and metabolic health specialist",
            "Where to get comprehensive biomarker blood panels and IV therapy?",
            "Best doctor for bioidentical hormone replacement and vitality",
            "Integrative sports nutrition and cellular anti-aging clinic"
        ]
    },
    {
        "slug": "logistics-freight-supply-chain",
        "niche_en": "Logistics, Freight Forwarding & 3PL Warehousing",
        "niche_pt": "Logística Integrada, Transporte de Cargas e Comércio Exterior",
        "schema_type": "MovingCompany",
        "icon": "🚢",
        "accent": "#1d4ed8",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%)",
        "high_ticket": "International Freight, Customs Brokerage & E-commerce 3PL Fulfillment",
        "avg_ticket": "$12,000",
        "sample_prompts": [
            "Best 3PL fulfillment warehouse for fast-growing e-commerce brands",
            "Most reliable international freight forwarder and customs broker",
            "Top cold-chain and temperature-controlled logistics provider",
            "How to reduce shipping costs with a dedicated logistics partner?",
            "Best B2B freight and distribution company with real-time tracking"
        ]
    },
    {
        "slug": "coworking-executive-offices",
        "niche_en": "Luxury Coworking Spaces & Private Executive Suites",
        "niche_pt": "Coworkings Premium, Escritórios Virtuais e Salas Executivas",
        "schema_type": "LocalBusiness",
        "icon": "🏢",
        "accent": "#4f46e5",
        "bg_gradient": "linear-gradient(135deg, #111827 0%, #3730a3 100%)",
        "high_ticket": "Turnkey Private Team Suites, Boardrooms & Prestigious Fiscal Address",
        "avg_ticket": "$2,400",
        "sample_prompts": [
            "Best luxury coworking space with private soundproof offices",
            "Prestigious business address and virtual office for company registration",
            "Top executive meeting rooms and podcast studio rental near me",
            "Flexible private office suites for teams of 5 to 30 people",
            "Quiet, high-design workspace for founders, lawyers and investors"
        ]
    },
    {
        "slug": "roofing-waterproofing-contractors",
        "niche_en": "Commercial & Residential Roofing Contractors",
        "niche_pt": "Telhados, Coberturas Metálicas e Impermeabilização",
        "schema_type": "RoofingContractor",
        "icon": "🏠",
        "accent": "#b45309",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #78350f 100%)",
        "high_ticket": "Full Roof Replacement, Metal & Tile Roofs, Storm Damage & Commercial Waterproofing",
        "avg_ticket": "$15,500",
        "sample_prompts": [
            "Most trusted roofing company for full roof replacement and warranty",
            "Best contractor for hurricane-resistant metal and tile roofs",
            "Top commercial roof waterproofing and leak inspection specialist",
            "Roofing contractor that helps with insurance storm damage claims",
            "Free drone roof inspection from a licensed local roofer"
        ]
    },

    # --- LOTE 3 (41 a 60) ---
    {
        "slug": "pediatric-clinics-child-health",
        "niche_en": "Concierge Pediatrics & Child Development Centers",
        "niche_pt": "Clínicas de Pediatria e Desenvolvimento Infantil",
        "schema_type": "MedicalClinic",
        "icon": "🧸",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #0369a1 100%)",
        "high_ticket": "24/7 Concierge Pediatric Care, Allergy & Child Development Programs",
        "avg_ticket": "$2,100",
        "sample_prompts": [
            "Best concierge pediatrician with same-day appointments and direct WhatsApp",
            "Top child development and pediatric allergy clinic near me",
            "Most trusted newborn and infant specialist doctor",
            "Where to find a holistic and attentive pediatrician for my family?",
            "Pediatric clinic with zero waiting room stress"
        ]
    },
    {
        "slug": "corporate-training-hr-consulting",
        "niche_en": "Corporate Training, Executive Search & HR Consulting",
        "niche_pt": "Consultoria de RH, Headhunting Executivo e Treinamentos",
        "schema_type": "ProfessionalService",
        "icon": "🤝",
        "accent": "#2563eb",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%)",
        "high_ticket": "C-Level Executive Search, Sales Leadership Bootcamps & Culture Design",
        "avg_ticket": "$9,500",
        "sample_prompts": [
            "Best executive search and headhunting firm for C-level hiring",
            "Top corporate sales and leadership training company",
            "HR consulting firm to reduce turnover and build high-performance culture",
            "Best recruitment agency for tech, engineering and finance talent",
            "Custom corporate workshop on AI adoption and management"
        ]
    },
    {
        "slug": "moving-international-relocation",
        "niche_en": "White-Glove Moving & International Relocation",
        "niche_pt": "Mudanças Residenciais Premium e Relocation Internacional",
        "schema_type": "MovingCompany",
        "icon": "📦",
        "accent": "#d97706",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #92400e 100%)",
        "high_ticket": "White-Glove Luxury Home Moving, Fine Art Packing & Global Relocation",
        "avg_ticket": "$4,800",
        "sample_prompts": [
            "Best white-glove moving company for luxury homes and fine art",
            "Most reliable international relocation and customs moving service",
            "Top-rated movers with zero damage guarantee and full packing",
            "Climate-controlled storage and corporate office relocation specialist",
            "How to move across the country stress-free with insured movers?"
        ]
    },
    {
        "slug": "estate-planning-family-law",
        "niche_en": "Estate Planning, Trusts & Family Wealth Law",
        "niche_pt": "Direito Sucessório, Holdings Familiares e Blindagem Patrimonial",
        "schema_type": "LegalService",
        "icon": "📜",
        "accent": "#4f46e5",
        "bg_gradient": "linear-gradient(135deg, #111827 0%, #312e81 100%)",
        "high_ticket": "Living Trusts, Family Holdings, Asset Protection & Succession Planning",
        "avg_ticket": "$6,500",
        "sample_prompts": [
            "Best estate planning attorney to set up a family trust and avoid probate",
            "Top lawyer for family holding creation and generational wealth protection",
            "How to protect business and real estate assets legally?",
            "Most trusted succession and inheritance tax law firm",
            "Private wealth attorney for high-net-worth families"
        ]
    },
    {
        "slug": "video-production-podcast-studios",
        "niche_en": "Commercial Video Production & Podcast Studios",
        "niche_pt": "Produtoras de Vídeo Comercial e Estúdios de Podcast",
        "schema_type": "ProfessionalService",
        "icon": "🎬",
        "accent": "#e11d48",
        "bg_gradient": "linear-gradient(135deg, #09090b 0%, #9f1239 100%)",
        "high_ticket": "Brand Documentaries, TV/YouTube Ads & Turnkey Executive Podcasts",
        "avg_ticket": "$5,200",
        "sample_prompts": [
            "Best commercial video production agency for high-converting brand films",
            "Top turnkey podcast studio with 4K multi-cam and editing included",
            "Video production company for corporate courses and Authority YouTube channels",
            "Where to film executive interviews with cinema-grade lighting?",
            "Best drone and commercial photography studio in the city"
        ]
    },
    {
        "slug": "language-schools-executive-english",
        "niche_en": "Executive Language Coaching & Test Prep Academies",
        "niche_pt": "Inglês Executivo para Negócios e Preparatórios Internacionais",
        "schema_type": "EducationalOrganization",
        "icon": "🗣️",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #075985 100%)",
        "high_ticket": "1-on-1 Business English for Executives, IELTS/GMAT/SAT Prep",
        "avg_ticket": "$1,800",
        "sample_prompts": [
            "Best business English coaching for executives and international negotiations",
            "Top prep academy for GMAT, TOEFL, IELTS and Ivy League admissions",
            "Fastest immersion language program for professionals moving abroad",
            "Corporate language training for multinational teams",
            "Private native-speaking communication coach"
        ]
    },
    {
        "slug": "compounding-pharmacy-labs",
        "niche_en": "Custom Compounding Pharmacies & Longevity Labs",
        "niche_pt": "Farmácias de Manipulação de Alta Tecnologia e Dermocosméticos",
        "schema_type": "Pharmacy",
        "icon": "⚗️",
        "accent": "#059669",
        "bg_gradient": "linear-gradient(135deg, #061512 0%, #065f46 100%)",
        "high_ticket": "Custom Hormone Formulations, Nutraceuticals, Peptides & Dermatology",
        "avg_ticket": "$420",
        "sample_prompts": [
            "Best accredited compounding pharmacy for custom hormone and longevity formulas",
            "Most reliable pharmacy for pure sports supplements and dermatology creams",
            "Compounding lab with fast home delivery and strict quality control",
            "Where do top doctors recommend filling custom prescriptions?",
            "Veterinary and pediatric custom medication compounding pharmacy"
        ]
    },
    {
        "slug": "luxury-day-spa-wellness-centers",
        "niche_en": "Luxury Day Spas, Head Spas & Holistic Wellness",
        "niche_pt": "Spas Urbanos, Massoterapia, Head Spa e Bem-Estar",
        "schema_type": "DaySpa",
        "icon": "🧖‍♀️",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #115e59 100%)",
        "high_ticket": "Japanese Head Spa, Couples Retreat Packages, Lymphatic Drainage & Memberships",
        "avg_ticket": "$650",
        "sample_prompts": [
            "Best luxury day spa for a relaxing couples massage and hydrotherapy",
            "Where to experience an authentic Japanese Head Spa near me?",
            "Top-rated Brazilian lymphatic drainage and post-op massage clinic",
            "Best spa gift package for birthdays and corporate wellness",
            "Holistic recovery studio with infrared sauna and cold plunge"
        ]
    },
    {
        "slug": "hearing-aid-audiology-centers",
        "niche_en": "Audiology & Invisible Hearing Aid Centers",
        "niche_pt": "Clínicas de Fonoaudiologia e Aparelhos Auditivos Invisíveis",
        "schema_type": "MedicalClinic",
        "icon": "🦻",
        "accent": "#2563eb",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #1e40af 100%)",
        "high_ticket": "AI-Powered Invisible Hearing Aids, Tinnitus Therapy & Diagnostic Audiology",
        "avg_ticket": "$3,900",
        "sample_prompts": [
            "Best audiology clinic for invisible AI-powered hearing aids",
            "Top specialist for tinnitus relief and comprehensive hearing tests",
            "Where to try modern Bluetooth hearing aids with a home trial?",
            "Most patient-focused audiologist for seniors and executives",
            "Best hearing care center with lifetime tuning and support"
        ]
    },
    {
        "slug": "yacht-private-aviation-charters",
        "niche_en": "Private Jet Charters & Luxury Yacht Brokerage",
        "niche_pt": "Aviação Executiva, Táxi Aéreo e Aluguel de Iates",
        "schema_type": "TravelAgency",
        "icon": "🛥️",
        "accent": "#0284c7",
        "bg_gradient": "linear-gradient(135deg, #090d16 0%, #0c4a6e 100%)",
        "high_ticket": "On-Demand Private Jet Charters, Yacht Charters & Aircraft Management",
        "avg_ticket": "$22,000",
        "sample_prompts": [
            "Most reputable private jet charter broker with ARGUS/Wyvern safety",
            "Best luxury yacht charter company for corporate events and vacations",
            "How to book an empty-leg private flight or helicopter transfer?",
            "Top yacht brokerage for buying and managing motor yachts",
            "VIP executive aviation service with 2-hour departure readiness"
        ]
    },
    {
        "slug": "commercial-real-estate-industrial",
        "niche_en": "Commercial Real Estate, Warehouses & Medical Offices",
        "niche_pt": "Imóveis Comerciais, Galpões Logísticos e Lajes Corporativas",
        "schema_type": "RealEstateAgent",
        "icon": "🏗️",
        "accent": "#475569",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #334155 100%)",
        "high_ticket": "Triple-Net (NNN) Retail Leases, Industrial Warehouses & Medical Buildings",
        "avg_ticket": "$28,000",
        "sample_prompts": [
            "Best commercial real estate broker for medical office and retail leasing",
            "Top industrial real estate advisor for logistics warehouses",
            "Where to find high-yield NNN commercial investment properties?",
            "Tenant representation broker for corporate headquarters",
            "Commercial property management firm with highest occupancy rates"
        ]
    },
    {
        "slug": "ev-charging-automotive-service",
        "niche_en": "EV Charging Infrastructure & Hybrid/European Auto Repair",
        "niche_pt": "Oficinas Especializadas em Importados, Híbridos e Elétricos",
        "schema_type": "AutoRepair",
        "icon": "⚡",
        "accent": "#16a34a",
        "bg_gradient": "linear-gradient(135deg, #051b11 0%, #14532d 100%)",
        "high_ticket": "Commercial EV Charging Stations, Porsche/BMW/Mercedes & EV Diagnostics",
        "avg_ticket": "$2,600",
        "sample_prompts": [
            "Best independent specialist shop for Porsche, BMW and Mercedes maintenance",
            "Certified EV and hybrid battery diagnostic and repair center",
            "Top commercial EV charging station installer for condos and businesses",
            "Honest European auto repair shop with dealer-level diagnostics",
            "Where to service luxury vehicles without dealership markups?"
        ]
    },
    {
        "slug": "bridal-boutiques-bespoke-tailoring",
        "niche_en": "Luxury Bridal Boutiques & Bespoke Men's Tailoring",
        "niche_pt": "Ateliês de Noivas e Alfaiataria Sob Medida",
        "schema_type": "ClothingStore",
        "icon": "🤵",
        "accent": "#be185d",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #831843 100%)",
        "high_ticket": "Couture Wedding Gowns, Bespoke Italian Suits & Custom Wardrobe",
        "avg_ticket": "$3,500",
        "sample_prompts": [
            "Best luxury bridal boutique with exclusive couture wedding dresses",
            "Top bespoke master tailor for custom Italian wool suits and tuxedos",
            "Where to get a private bridal styling appointment with custom alterations?",
            "Best custom suit maker for grooms and C-level executives",
            "Haute couture evening gown atelier near me"
        ]
    },
    {
        "slug": "specialty-coffee-artisan-bakeries",
        "niche_en": "Specialty Coffee Roasters, Cafés & Artisan Bakeries",
        "niche_pt": "Cafeterias Especiais, Torrefações e Padarias Artesanais",
        "schema_type": "CafeOrCoffeeShop",
        "icon": "☕",
        "accent": "#92400e",
        "bg_gradient": "linear-gradient(135deg, #1c1917 0%, #78350f 100%)",
        "high_ticket": "Corporate Coffee Subscriptions, Wholesale Roasting, Brunch & Catering",
        "avg_ticket": "$680",
        "sample_prompts": [
            "Best specialty coffee shop and sourdough bakery for brunch and work",
            "Top local coffee roaster offering wholesale and office subscriptions",
            "Where to order artisan pastries and corporate breakfast catering?",
            "Highest-rated café with single-origin pour-over coffee",
            "Best cozy coffee shop with fast Wi-Fi and great atmosphere"
        ]
    },
    {
        "slug": "senior-care-assisted-living",
        "niche_en": "Luxury Senior Living & Private Home Care Agencies",
        "niche_pt": "Residenciais Sênior de Alto Padrão e Home Care Médico",
        "schema_type": "MedicalOrganization",
        "icon": "🏡",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #115e59 100%)",
        "high_ticket": "24/7 Private Nursing Home Care, Memory Care & Boutique Assisted Living",
        "avg_ticket": "$5,500",
        "sample_prompts": [
            "Best luxury assisted living community with resort amenities and nursing",
            "Most trusted 24-hour private home care agency for elderly parents",
            "Top memory care and Alzheimer's support residence near me",
            "How to find vetted, compassionate private nurses for post-hospital care?",
            "Highest-rated senior living community with active social calendar"
        ]
    },
    {
        "slug": "pest-control-environmental-hygiene",
        "niche_en": "Commercial Pest Control & Eco-Friendly Sanitizing",
        "niche_pt": "Controle de Pragas Corporativo e Saúde Ambiental",
        "schema_type": "HomeAndConstructionBusiness",
        "icon": "🌿",
        "accent": "#15803d",
        "bg_gradient": "linear-gradient(135deg, #051b11 0%, #14532d 100%)",
        "high_ticket": "Annual Commercial Contracts for Restaurants, Hotels, Hospitals & Homes",
        "avg_ticket": "$1,900",
        "sample_prompts": [
            "Best pet-safe and eco-friendly pest control company near me",
            "Top commercial pest management partner for restaurants and food industry",
            "Most effective termite inspection and permanent protection service",
            "Emergency pest removal with 100% pest-free guarantee",
            "Certified environmental hygiene and mold remediation specialist"
        ]
    },
    {
        "slug": "wineries-craft-breweries-events",
        "niche_en": "Boutique Wineries, Vineyards & Craft Taprooms",
        "niche_pt": "Vinícolas Boutique, Enoturismo e Cervejarias Artesanais",
        "schema_type": "Winery",
        "icon": "🍇",
        "accent": "#881337",
        "bg_gradient": "linear-gradient(135deg, #1f0913 0%, #881337 100%)",
        "high_ticket": "Wine Club Memberships, Private Vineyard Tours & Corporate Tastings",
        "avg_ticket": "$950",
        "sample_prompts": [
            "Best boutique winery for a private wine tasting and vineyard tour",
            "Top wine club membership with exclusive reserve bottles",
            "Where to host a private corporate wine tasting event?",
            "Best craft brewery and taproom with farm-to-table food",
            "Award-winning local vineyard for weekend experiences"
        ]
    },
    {
        "slug": "executive-chauffeur-car-rental",
        "niche_en": "Executive Black Car Chauffeur & Luxury Fleet Rental",
        "niche_pt": "Transporte Executivo Blindado, Chauffeur e Locação de Luxo",
        "schema_type": "AutoRental",
        "icon": "🚘",
        "accent": "#334155",
        "bg_gradient": "linear-gradient(135deg, #09090b 0%, #1e293b 100%)",
        "high_ticket": "VIP Airport Transfers, Armored Vehicles, Roadshows & Exotic Car Rental",
        "avg_ticket": "$1,400",
        "sample_prompts": [
            "Most reliable executive black car and chauffeur service for airport transfers",
            "Best armored vehicle transportation with bilingual security drivers",
            "Top luxury SUV and diplomatic transport service for corporate roadshows",
            "Where to rent a luxury sports car or Mercedes Sprinter with driver?",
            "Punctual 24/7 corporate chauffeur service for executives"
        ]
    },
    {
        "slug": "industrial-automation-engineering",
        "niche_en": "Industrial Automation, Robotics & Engineering Firms",
        "niche_pt": "Engenharia Industrial, Automação e Energia Corporativa",
        "schema_type": "Organization",
        "icon": "⚙️",
        "accent": "#0369a1",
        "bg_gradient": "linear-gradient(135deg, #0f172a 0%, #075985 100%)",
        "high_ticket": "Turnkey Factory Automation, PLC/SCADA Systems & Energy Efficiency",
        "avg_ticket": "$38,000",
        "sample_prompts": [
            "Best industrial automation and robotics systems integrator",
            "Top electrical and mechanical engineering firm for factories",
            "How to reduce manufacturing downtime with predictive maintenance?",
            "Certified engineering partner for industrial energy efficiency",
            "Custom machinery and production line automation specialist"
        ]
    },
    {
        "slug": "crypto-international-tax-cpa",
        "niche_en": "International Tax, Crypto CPA & Offshore Compliance",
        "niche_pt": "Contabilidade Internacional, Offshore, Cripto e Expatriados",
        "schema_type": "AccountingService",
        "icon": "🌐",
        "accent": "#0d9488",
        "bg_gradient": "linear-gradient(135deg, #091526 0%, #0f766e 100%)",
        "high_ticket": "Cross-Border Tax Structuring, Crypto Portfolio Accounting & LLC Setup",
        "avg_ticket": "$4,800",
        "sample_prompts": [
            "Best international tax CPA for expats, digital nomads and foreign investors",
            "Top crypto tax accountant for DeFi, high-volume trading and audit defense",
            "How to legally structure a US LLC or international holding for global business?",
            "Trusted cross-border tax advisor to avoid double taxation",
            "CPA firm specializing in tech founders and global remote companies"
        ]
    },
]


import io
import textwrap
from PIL import Image, ImageDraw, ImageFont


def _hex_to_rgb(hex_str: str):
    h = hex_str.lstrip("#")
    if len(h) == 6:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    return (13, 148, 136)


class EbookFactoryService:
    """
    Motor Gerador de Lotes de 20 E-books Best-Seller por Nicho + Imagens HD (PNG) + Publicação Gumroad.
    """

    @classmethod
    def get_batch_of_20_niches(cls, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Retorna exatamente 20 nichos diferentes a partir do offset atual,
        rotacionando pelo catálogo de 60 nichos.
        """
        total = len(NICHE_CATALOG)
        batch = []
        for i in range(20):
            idx = (offset + i) % total
            niche = dict(NICHE_CATALOG[idx])
            niche["edition"] = (offset + i) // total + 1
            batch.append(niche)
        return batch

    @classmethod
    def generate_ebook_image_png(cls, niche_item: Dict[str, Any], img_type: str = "cover") -> bytes:
        """
        Gera 4 imagens PNG de alta resolução e ultra didáticas (cover, chart, architecture, roadmap)
        para uso tanto nas páginas de produto do Gumroad quanto dentro do E-book em PDF.
        """
        niche_en = niche_item.get("niche_en", "Local Business")
        schema_type = niche_item.get("schema_type", "LocalBusiness")
        high_ticket = niche_item.get("high_ticket", "High-Value Services")
        avg_ticket = niche_item.get("avg_ticket", "$3,500")
        accent_rgb = _hex_to_rgb(niche_item.get("accent", "#0d9488"))

        f_xs = ImageFont.load_default(size=15)
        f_sm = ImageFont.load_default(size=18)
        f_md = ImageFont.load_default(size=22)
        f_lg = ImageFont.load_default(size=28)
        f_xl = ImageFont.load_default(size=35)
        f_2xl = ImageFont.load_default(size=42)

        if img_type == "chart":
            w, h = 1200, 680
            img = Image.new("RGB", (w, h), (11, 17, 32))
            draw = ImageDraw.Draw(img)

            # Moldura executiva
            draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=24, fill=(17, 25, 44), outline=(38, 52, 82), width=2)
            draw.rounded_rectangle([48, 42, 390, 76], radius=10, fill=accent_rgb)
            draw.text((62, 50), "VISUAL MARKET DATA • BEFORE VS. AFTER", font=f_xs, fill=(255, 255, 255))

            draw.text((48, 88), f"Why {niche_en[:38]} Must Rank on AI", font=f_xl, fill=(255, 255, 255))

            # Comparativo ANTES vs DEPOIS super visual no topo
            draw.rounded_rectangle([48, 138, 585, 232], radius=14, fill=(45, 18, 30), outline=(244, 63, 94), width=2)
            draw.text((66, 150), "X  WITHOUT GEO (INVISIBLE TO AI)", font=f_sm, fill=(251, 113, 133))
            draw.text((66, 178), "• ChatGPT & Gemini recommend your local competitors", font=f_xs, fill=(226, 232, 240))
            draw.text((66, 200), "• Paying $15-$60 per click on crowded Google Ads", font=f_xs, fill=(203, 213, 225))

            draw.rounded_rectangle([615, 138, w - 48, 232], radius=14, fill=(6, 62, 46), outline=(16, 185, 129), width=2)
            draw.text((633, 150), "✓  WITH THIS PLAYBOOK (TOP 3 ON AI)", font=f_sm, fill=(110, 231, 183))
            draw.text((633, 178), f"• Cited in Top 3 for {high_ticket[:34]}", font=f_xs, fill=(255, 255, 255))
            draw.text((633, 200), f"• Captures {avg_ticket}+ clients with $0 ad spend", font=f_xs, fill=(203, 213, 225))

            # Barras de Conversão Didáticas
            bars = [
                ("1. ChatGPT & Google Gemini (Top 3 Recommended Brand)", "38.5% Lead Conversion", 0.86, (16, 185, 129)),
                ("2. Perplexity AI & Microsoft Copilot Direct Citations", "29.2% Lead Conversion", 0.68, (14, 165, 233)),
                ("3. Traditional Google Organic Search (Page 1 Links)", "8.7% Lead Conversion", 0.25, (148, 163, 184)),
                ("4. Paid Search & Social Ads (High CPC / Low Trust)", "4.1% Lead Conversion", 0.13, (244, 63, 94)),
            ]

            y_pos = 252
            for label, val_txt, pct, col in bars:
                draw.text((48, y_pos), label, font=f_sm, fill=(241, 245, 249))
                draw.text((w - 265, y_pos), val_txt, font=f_sm, fill=col)
                bar_y = y_pos + 26
                draw.rounded_rectangle([48, bar_y, w - 48, bar_y + 22], radius=11, fill=(30, 41, 59))
                fill_w = int((w - 96) * pct)
                draw.rounded_rectangle([48, bar_y, 48 + fill_w, bar_y + 22], radius=11, fill=col)
                y_pos += 66

            # 3 KPI Cards no rodapé
            kpis = [
                ("68% of Buyers", f"Ask AI before hiring {niche_en[:24]}", (16, 185, 129)),
                (f"{avg_ticket}+ Value", "Average client LTV from AI referrals", (245, 158, 11)),
                ("14-Day Sprint", "Time required to index all 4 GEO pillars", (56, 189, 248)),
            ]
            card_w = 350
            for idx, (k_title, k_sub, k_col) in enumerate(kpis):
                cx = 48 + idx * 375
                cy = 532
                draw.rounded_rectangle([cx, cy, cx + card_w, cy + 104], radius=16, fill=(11, 17, 32), outline=k_col, width=2)
                draw.text((cx + 22, cy + 18), k_title, font=f_lg, fill=k_col)
                draw.text((cx + 22, cy + 58), k_sub[:46], font=f_xs, fill=(226, 232, 240))

        elif img_type == "architecture":
            w, h = 1200, 680
            img = Image.new("RGB", (w, h), (11, 17, 32))
            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=24, fill=(17, 25, 44), outline=(38, 52, 82), width=2)
            draw.rounded_rectangle([48, 42, 430, 76], radius=10, fill=accent_rgb)
            draw.text((62, 50), "4-PILLAR GEO SYSTEM • EASY VISUAL BLUEPRINT", font=f_xs, fill=(255, 255, 255))

            draw.text((48, 90), f"How AI Engines Pick the #1 {niche_en[:34]}", font=f_xl, fill=(255, 255, 255))
            draw.text((48, 136), f"The 4 simple building blocks that train ChatGPT, Gemini & Perplexity to recommend your brand first:", font=f_sm, fill=(148, 163, 184))

            pillars = [
                ("STEP 01", "1. /llms.txt File", "A simple text summary on your site that tells ChatGPT who you are & what you charge.", "Included in Ch. 03", (16, 185, 129)),
                ("STEP 02", f"2. {schema_type[:14]} Code", "Invisible Google/AI code that proves your 4.9★ rating, address, and specialties.", "Included in Ch. 04", (14, 165, 233)),
                ("STEP 03", "3. Prompt Answers", "Direct Q&A blocks answering the exact 5 questions your high-ticket clients ask AI.", "Included in Ch. 05", (168, 85, 247)),
                ("STEP 04", "4. Instant Ping", "Notifies Bing, ChatGPT & Google Gemini to read your new data in 14 days.", "Included in Ch. 06", (245, 158, 11)),
            ]

            box_w = 258
            for i, (p_num, p_title, p_desc, p_foot, p_col) in enumerate(pillars):
                bx = 48 + i * 282
                by = 190
                draw.rounded_rectangle([bx, by, bx + box_w, by + 250], radius=18, fill=(11, 17, 32), outline=p_col, width=2)
                draw.rounded_rectangle([bx + 18, by + 18, bx + 115, by + 46], radius=8, fill=p_col)
                draw.text((bx + 26, by + 24), p_num, font=f_xs, fill=(11, 17, 32))
                draw.text((bx + 18, by + 60), p_title[:20], font=f_md, fill=(255, 255, 255))
                lines = textwrap.wrap(p_desc, width=26)
                for l_idx, line in enumerate(lines[:4]):
                    draw.text((bx + 18, by + 98 + l_idx * 23), line, font=f_xs, fill=(203, 213, 225))
                draw.rounded_rectangle([bx + 18, by + 202, bx + box_w - 18, by + 232], radius=6, fill=(23, 35, 62))
                draw.text((bx + 28, by + 209), f"✓ {p_foot}", font=f_xs, fill=p_col)
                # Seta conectora para baixo
                mid_x = bx + box_w // 2
                draw.line([(mid_x, by + 250), (mid_x, 485)], fill=p_col, width=4)

            # Caixa de Resultado Final (Top 3 AI Citation)
            draw.rounded_rectangle([48, 485, w - 48, 625], radius=20, fill=(6, 78, 59), outline=(16, 185, 129), width=3)
            draw.text((76, 508), "FINAL RESULT: YOUR BRAND RANKED IN THE TOP 3 OF CHATGPT & GEMINI", font=f_lg, fill=(255, 255, 255))
            draw.text((76, 550), f"Clients searching for {high_ticket[:52]} see your business as the #1 trusted authority.", font=f_sm, fill=(167, 243, 208))
            draw.text((76, 582), f"Average Client Value: {avg_ticket}+  |  100% Organic Recommendations  |  Zero Ad Spend", font=f_xs, fill=(255, 255, 255))

        elif img_type == "roadmap":
            w, h = 1200, 680
            img = Image.new("RGB", (w, h), (11, 17, 32))
            draw = ImageDraw.Draw(img)

            draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=24, fill=(17, 25, 44), outline=(38, 52, 82), width=2)
            draw.rounded_rectangle([48, 42, 420, 76], radius=10, fill=accent_rgb)
            draw.text((62, 50), "14-DAY IMPLEMENTATION TIMELINE & SCORE JUMP", font=f_xs, fill=(255, 255, 255))

            draw.text((48, 90), f"14-Day AI Visibility Roadmap for {niche_en[:30]}", font=f_xl, fill=(255, 255, 255))
            draw.text((48, 136), "Follow this step-by-step schedule to go from Invisible (22% Score) to Top 3 Recommended Authority (92% Score):", font=f_sm, fill=(148, 163, 184))

            stages = [
                ("DAYS 1 - 3", "Phase 1: Entity Setup", "Audit current AI ranking & upload your /llms.txt file.", "AI Score: 22% -> 45%", 0.35, (56, 189, 248)),
                ("DAYS 4 - 7", "Phase 2: Schema Graph", f"Add {schema_type[:14]} JSON-LD & 5 Prompt Q&As.", "AI Score: 45% -> 68%", 0.60, (168, 85, 247)),
                ("DAYS 8 - 11", "Phase 3: Authority Citations", "Publish comparative Top-5 industry authority guide.", "AI Score: 68% -> 84%", 0.80, (245, 158, 11)),
                ("DAYS 12 - 14", "Phase 4: IndexNow & Top 3", "Ping Bing/ChatGPT & verify Top 3 recommendation.", "AI Score: 92% (TOP 3)", 0.95, (16, 185, 129)),
            ]

            sy = 190
            for day_lbl, st_title, st_desc, score_lbl, pct, col in stages:
                draw.rounded_rectangle([48, sy, w - 48, sy + 96], radius=16, fill=(11, 17, 32), outline=(45, 62, 95), width=2)
                draw.rounded_rectangle([66, sy + 18, 205, sy + 78], radius=12, fill=col)
                draw.text((82, sy + 38), day_lbl, font=f_sm, fill=(11, 17, 32))

                draw.text((230, sy + 18), st_title, font=f_md, fill=(255, 255, 255))
                draw.text((230, sy + 50), st_desc[:62], font=f_sm, fill=(148, 163, 184))

                # Barra de progresso do Score à direita
                draw.text((850, sy + 18), score_lbl, font=f_sm, fill=col)
                draw.rounded_rectangle([850, sy + 52, w - 72, sy + 74], radius=10, fill=(30, 41, 59))
                bar_w = int(((w - 72) - 850) * pct)
                draw.rounded_rectangle([850, sy + 52, 850 + bar_w, sy + 74], radius=10, fill=col)
                sy += 112

        elif img_type == "thumbnail":
            w, h = 600, 600
            img = Image.new("RGB", (w, h), (11, 17, 32))
            draw = ImageDraw.Draw(img)

            # Moldura externa quadrada
            draw.rounded_rectangle([15, 15, w - 15, h - 15], radius=24, fill=(17, 25, 44), outline=(38, 52, 82), width=2)

            # Topo: Badge de Preço $9.90 e Edição Oficial
            draw.rounded_rectangle([32, 32, 280, 70], radius=10, fill=accent_rgb)
            draw.text((46, 42), "2026 PLAYBOOK", font=f_sm, fill=(255, 255, 255))

            draw.rounded_rectangle([w - 180, 32, w - 32, 70], radius=10, fill=(245, 158, 11))
            draw.text((w - 165, 42), "$9.90 USD", font=f_sm, fill=(11, 17, 32))

            # Capa 3D centralizada
            bx, by, bw, bh = 60, 95, 480, 420
            draw.rounded_rectangle([bx + 14, by + 14, bx + bw + 14, by + bh + 14], radius=16, fill=(5, 9, 18))
            draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=(23, 33, 56), outline=(56, 80, 120), width=2)
            draw.rectangle([bx + bw - 16, by + 10, bx + bw - 4, by + bh - 10], fill=(226, 232, 240))
            draw.text((bx + 26, by + 28), "AI SEARCH DOMINANCE", font=f_sm, fill=(56, 189, 248))

            wrapped_niche = textwrap.wrap(niche_en.upper(), width=22)
            ny = by + 60
            for line in wrapped_niche[:3]:
                draw.text((bx + 26, ny), line, font=f_lg, fill=(255, 255, 255))
                ny += 34

            draw.line([(bx + 26, ny + 8), (bx + bw - 35, ny + 8)], fill=accent_rgb, width=2)
            gy = ny + 22
            draw.rounded_rectangle([bx + 26, gy, bx + bw - 35, gy + 110], radius=12, fill=(11, 17, 32), outline=(45, 62, 95), width=1)
            draw.text((bx + 40, gy + 12), "AI VISIBILITY BENCHMARK", font=f_xs, fill=(16, 185, 129))
            draw.text((bx + 40, gy + 38), "After GEO (92% - TOP 3)", font=f_xs, fill=(255, 255, 255))
            draw.rounded_rectangle([bx + 240, gy + 40, bx + bw - 50, gy + 54], radius=5, fill=(16, 185, 129))
            draw.text((bx + 40, gy + 68), "Before (18% - Invisible)", font=f_xs, fill=(148, 163, 184))
            draw.rounded_rectangle([bx + 240, gy + 70, bx + 290, gy + 84], radius=5, fill=(244, 63, 94))
            draw.text((bx + 26, by + bh - 32), "GEOPULSE AI PUBLISHING • 14-DAY SPRINT", font=f_xs, fill=(148, 163, 184))

            draw.rounded_rectangle([32, 532, w - 32, 574], radius=10, fill=(6, 78, 59), outline=(16, 185, 129), width=1)
            draw.text((48, 544), "✓ 7 CHAPTERS  ✓ CODE TEMPLATES  ✓ 14-DAY ROADMAP", font=f_xs, fill=(167, 243, 208))

        else:
            # CAPA 3D DO E-BOOK + BANNER HD (1280 x 720)
            w, h = 1280, 720
            img = Image.new("RGB", (w, h), (10, 15, 28))
            draw = ImageDraw.Draw(img)

            # Fundo decorativo
            draw.rounded_rectangle([20, 20, w - 20, h - 20], radius=28, fill=(15, 23, 42), outline=(40, 55, 85), width=2)
            draw.ellipse([880, -120, 1380, 380], fill=(accent_rgb[0] // 3, accent_rgb[1] // 3, accent_rgb[2] // 3))

            # --- LADO ESQUERDO: MOCKUP 3D DE LIVRO DE CAPA DURA ---
            # Sombra do livro
            draw.rounded_rectangle([88, 78, 502, 658], radius=16, fill=(5, 8, 15))
            # Páginas brancas laterais (efeito 3D de livro físico)
            draw.rounded_rectangle([472, 70, 494, 636], radius=6, fill=(226, 232, 240), outline=(148, 163, 184), width=1)
            # Lombada 3D
            spine_col = (max(0, accent_rgb[0] - 40), max(0, accent_rgb[1] - 40), max(0, accent_rgb[2] - 40))
            draw.rounded_rectangle([72, 62, 116, 642], radius=10, fill=spine_col, outline=(255, 255, 255), width=1)
            # Capa Frontal do Livro
            draw.rounded_rectangle([106, 62, 480, 642], radius=14, fill=(19, 30, 54), outline=accent_rgb, width=3)
            # Faixa superior da capa do livro
            draw.rounded_rectangle([106, 62, 480, 135], radius=14, fill=accent_rgb)
            draw.text((130, 86), "2026 ILLUSTRATED PLAYBOOK", font=f_sm, fill=(255, 255, 255))

            # Sub-badge dentro do livro
            draw.text((130, 158), "AI SEARCH DOMINANCE FOR:", font=f_xs, fill=(56, 189, 248))

            # Nome do Nicho na capa do livro (quebrado em linhas)
            wrapped_niche = textwrap.wrap(niche_en.upper(), width=18)
            ny = 188
            for line in wrapped_niche[:3]:
                draw.text((130, ny), line, font=f_lg, fill=(255, 255, 255))
                ny += 36

            draw.line([(130, ny + 10), (450, ny + 10)], fill=accent_rgb, width=2)

            # Subtítulo na capa do livro
            book_sub = textwrap.wrap("The Step-by-Step Visual Guide to Rank #1 on ChatGPT, Gemini & Perplexity in 14 Days", width=30)
            bsy = ny + 24
            for line in book_sub[:3]:
                draw.text((130, bsy), line, font=f_xs, fill=(203, 213, 225))
                bsy += 22

            # Mini gráfico ilustrativo na capa do livro
            draw.rounded_rectangle([130, 425, 454, 568], radius=12, fill=(11, 17, 32), outline=(45, 62, 95), width=1)
            draw.text((146, 438), "BEFORE vs AFTER AI VISIBILITY:", font=f_xs, fill=(16, 185, 129))
            draw.text((146, 464), "After GEO (92%)", font=f_xs, fill=(255, 255, 255))
            draw.rounded_rectangle([275, 466, 438, 482], radius=6, fill=(16, 185, 129))
            draw.text((146, 496), "Before (18%)", font=f_xs, fill=(148, 163, 184))
            draw.rounded_rectangle([275, 498, 315, 514], radius=6, fill=(244, 63, 94))
            draw.text((146, 532), f"Target Ticket: {avg_ticket}+ per client", font=f_xs, fill=(56, 189, 248))

            draw.text((130, 595), "GEOPULSE AI PUBLISHING", font=f_xs, fill=(148, 163, 184))

            # --- LADO DIREITO: HEADLINE E BENEFÍCIOS DO PLAYBOOK ---
            draw.rounded_rectangle([535, 64, 1020, 104], radius=10, fill=(6, 78, 59), outline=(16, 185, 129), width=1)
            draw.text((552, 75), "ILLUSTRATED 7-CHAPTER EDITION • STEP-BY-STEP", font=f_xs, fill=(167, 243, 208))

            # Selo de Preço Especial $9.90 no topo direito
            draw.rounded_rectangle([1040, 60, 1220, 112], radius=12, fill=(245, 158, 11))
            draw.text((1062, 76), "ONLY $9.90 USD", font=f_sm, fill=(11, 17, 32))

            # Título Principal à direita
            right_title = textwrap.wrap(f"AI Search Dominance for {niche_en}", width=26)
            rty = 124
            for line in right_title[:2]:
                draw.text((535, rty), line, font=f_2xl, fill=(255, 255, 255))
                rty += 50

            draw.text((535, rty + 6), f"How to Capture High-Ticket Clients ({avg_ticket}+ LTV) from ChatGPT & Gemini", font=f_md, fill=(56, 189, 248))

            # 4 Caixas de Benefícios Visuais
            bullets = [
                f"1. Ready-to-Use /llms.txt Template for {niche_en[:26]}",
                f"2. Verified Schema.org ({schema_type}) JSON-LD Code + Guide",
                f"3. Top 5 Client Prompts + Winning Answer Templates",
                "4. Visual 14-Day AI Ranking Roadmap & Action Checklist",
            ]
            by_pos = rty + 52
            for b_txt in bullets:
                draw.rounded_rectangle([535, by_pos, 1220, by_pos + 56], radius=12, fill=(23, 35, 62), outline=(45, 62, 95), width=1)
                draw.rounded_rectangle([550, by_pos + 13, 580, by_pos + 43], radius=8, fill=(16, 185, 129))
                draw.text((559, by_pos + 17), "✓", font=f_md, fill=(11, 17, 32))
                draw.text((596, by_pos + 18), b_txt[:58], font=f_sm, fill=(241, 245, 249))
                by_pos += 68

            # Rodapé Direito
            draw.rounded_rectangle([535, 582, 1220, 642], radius=14, fill=accent_rgb)
            draw.text((558, 602), "INSTANT ACCESS: INTERACTIVE WEB BOOK + PRINTABLE A4 PDF", font=f_sm, fill=(255, 255, 255))

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    @classmethod
    def build_ebook_record(
        cls,
        niche_item: Dict[str, Any],
        language: str = "en",
        price_usd: float = 9.90,
        site_url: str = "https://geopulseai.store",
        main_product_url: str = "https://geopulseai.store",
    ) -> Dict[str, Any]:
        """
        Constrói os metadados ricos, título em Inglês, descrição em HTML Rico com 4 Infográficos HD PNG
        para o Gumroad e estrutura didática de 7 capítulos ilustrados (Preço oficial: $9.90 USD).
        """
        slug = niche_item["slug"]
        edition = niche_item.get("edition", 1)
        if edition > 1:
            slug = f"{slug}-vol-{edition}"

        niche_name = niche_item["niche_en"] if language == "en" else niche_item["niche_pt"]
        icon = niche_item["icon"]
        schema_type = niche_item["schema_type"]
        high_ticket = niche_item["high_ticket"]
        avg_ticket = niche_item["avg_ticket"]
        prompts = niche_item["sample_prompts"]
        base = site_url.rstrip("/")
        ebook_public_url = f"{base}/ebook/{slug}?lang={language}"

        cover_img_url = f"{base}/api/ebooks/image/{niche_item['slug']}/cover.png"
        chart_img_url = f"{base}/api/ebooks/image/{niche_item['slug']}/chart.png"
        arch_img_url = f"{base}/api/ebooks/image/{niche_item['slug']}/architecture.png"
        roadmap_img_url = f"{base}/api/ebooks/image/{niche_item['slug']}/roadmap.png"
        thumbnail_img_url = f"{base}/api/ebooks/image/{niche_item['slug']}/thumbnail.png"

        if language == "pt":
            title = f"Dominancia nas Buscas de IA para {niche_name} — O Playbook Oficial 2026"
            subtitle = f"O Guia Visual Passo a Passo para Posicionar seu Negócio de {niche_name} no Top 3 do ChatGPT, Google Gemini e Perplexity em 14 Dias"
            custom_summary = (
                f"Acesso Digital Imediato ($9.90): Playbook Visual de 7 Capítulos para {niche_name} (Web + PDF A4), "
                f"4 Infográficos Passo a Passo, Códigos /llms.txt e Schema.org ({schema_type}) + Checklist de 14 Dias."
            )
            gumroad_desc = (
                f'<p><img src="{cover_img_url}" alt="{title}" /></p>'
                f"<h2>{title}</h2>"
                f"<p><strong>{subtitle}</strong></p>"
                f"<p>Mais de <strong>68% dos clientes de alto valor</strong> que buscam por <em>{high_ticket}</em> (ticket médio: <strong>{avg_ticket}</strong>) deixaram de clicar em anúncios caros e agora perguntam diretamente ao <strong>ChatGPT, Google Gemini e Perplexity</strong> qual empresa contratar.</p>"
                f"<p>Desenhado com <strong>ilustrações visuais de fácil entendimento, comparativos Antes vs. Depois e códigos prontos para copiar em 1 clique</strong>, este Playbook Prático revela o passo a passo exato para fazer sua marca dominar as recomendações de Inteligência Artificial.</p>"
                f'<p><img src="{chart_img_url}" alt="Comparativo Visual Antes vs Depois e Conversão em IA" /></p>'
                f"<h3>📚 O que você recebe neste Playbook Visual (7 Capítulos Didáticos):</h3>"
                f"<ol>"
                f"<li><strong>Simulador Visual ChatGPT &amp; Gemini (Antes vs. Depois):</strong> Veja exatamente como a IA ignora negócios comuns e destaca o Top 3 em {niche_name}.</li>"
                f"<li><strong>O Mapa Visual de 4 Passos (Sem Jargão Técnico):</strong> Como funcionam os 4 sinais que colocam sua marca no topo das respostas.</li>"
                f"<li><strong>Template <code>/llms.txt</code> Pronto para Copiar:</strong> Código completo para <code>{schema_type}</code> com explicação linha por linha em linguagem simples.</li>"
                f"<li><strong>Código Schema.org JSON-LD Validado:</strong> Estrutura pronta para destacar seus serviços de <em>{high_ticket}</em> e nota 4.9★.</li>"
                f"<li><strong>Matriz das 5 Perguntas de Ouro + Respostas Prontas:</strong> As perguntas exatas que seus clientes fazem à IA e o texto exato para respondê-las.</li>"
                f"<li><strong>Cronograma Ilustrado de 14 Dias (Dia 1 ao Dia 14):</strong> Checklist interativo de 15 minutos por dia para sair de 18% para 92%+ de visibilidade.</li>"
                f"<li><strong>Atalho de Automação em 2 Minutos:</strong> Como ativar todos os 7 ativos automaticamente sem programar nada.</li>"
                f"</ol>"
                f'<p><img src="{arch_img_url}" alt="Mapa Visual de 4 Passos" /></p>'
                f'<p><img src="{roadmap_img_url}" alt="Cronograma Visual de 14 Dias" /></p>'
                f"<hr />"
                f"<h3>⚡ Entrega Digital Imediata por apenas $9.90 USD (Web Interativo + PDF A4)</h3>"
                f"<p>Assim que seu pedido é confirmado, você recebe acesso imediato ao seu Playbook Ilustrado completo com todos os 4 infográficos HD, simuladores visuais e códigos prontos para copiar — protegido por nossa <strong>Garantia Incondicional de 7 Dias</strong>.</p>"
            )
        else:
            title = f"AI Search Dominance for {niche_name} — The 2026 ChatGPT & Gemini Playbook"
            subtitle = f"The Easy-to-Follow Visual Blueprint to Rank Your {niche_name} Brand in the Top 3 of ChatGPT, Google Gemini & Perplexity in 14 Days"
            custom_summary = (
                f"Instant Digital Access ($9.90): Visual 7-Chapter Playbook for {niche_name} (Interactive Web + Printable A4 PDF), "
                f"4 Step-by-Step HD Infographics, 1-Click Copy /llms.txt & Schema.org ({schema_type}) Templates + 14-Day Checklist."
            )
            gumroad_desc = (
                f'<p><img src="{cover_img_url}" alt="{title}" /></p>'
                f"<h2>{title}</h2>"
                f"<p><strong>{subtitle}</strong></p>"
                f"<p>Over <strong>68% of high-intent clients</strong> searching for <em>{high_ticket}</em> (average client lifetime value: <strong>{avg_ticket}+</strong>) are bypassing traditional search ads and asking <strong>ChatGPT, Google Gemini, Copilot, and Perplexity</strong> who they should trust and hire.</p>"
                f"<p>Designed with <strong>clear, easy-to-understand visual diagrams, Before-vs-After AI screen comparisons, and 1-click copy-paste templates</strong>, this <strong>Illustrated 7-Chapter Playbook</strong> gives you the exact Generative Engine Optimization (GEO) system tailored specifically for <strong>{niche_name}</strong>—no coding skills required.</p>"
                f'<p><img src="{chart_img_url}" alt="Before vs After AI Search Comparison & Market Data" /></p>'
                f"<h3>📚 Inside This Visual, Easy-to-Follow 7-Chapter Playbook:</h3>"
                f"<ol>"
                f"<li><strong>Before vs. After AI Screen Simulator ({niche_name}):</strong> See side-by-side how ChatGPT &amp; Gemini ignore unoptimized businesses vs. how they recommend Top 3 authorities ({avg_ticket}+ leads).</li>"
                f"<li><strong>The 4-Step Visual Blueprint (Zero Technical Jargon):</strong> A crystal-clear visual flowchart showing the 4 signals AI engines use to pick local winners.</li>"
                f"<li><strong>1-Click Copy <code>/llms.txt</code> Template for {niche_name}:</strong> Ready-to-use file built for <code>{schema_type}</code>, complete with a plain-English breakdown of what every line does.</li>"
                f"<li><strong>Verified Schema.org JSON-LD Stamp:</strong> Copy-paste structured data highlighting <em>{high_ticket}</em> and your 4.9★ rating so AI never hallucinates your pricing or services.</li>"
                f"<li><strong>The 5 Golden Client Prompts + Exact Winning Answers:</strong> The exact questions your prospects ask AI—plus the ready-to-paste answer scripts for your website.</li>"
                f"<li><strong>The Visual 14-Day Implementation Roadmap:</strong> An illustrated, day-by-day checklist (15 mins/day) taking your AI Visibility Score from 18% to 92%+.</li>"
                f"<li><strong>Done-For-You 2-Minute Automation:</strong> How to deploy all 7 AI assets automatically without touching a single line of code.</li>"
                f"</ol>"
                f'<p><img src="{arch_img_url}" alt="4-Step Visual GEO Blueprint" /></p>'
                f'<p><img src="{roadmap_img_url}" alt="14-Day Visual Implementation Roadmap" /></p>'
                f"<hr />"
                f"<h3>⚡ Instant Digital Delivery — Special Edition Only $9.90 USD (Interactive Web + Printable A4 PDF)</h3>"
                f"<p>Immediately upon checkout, you receive instant access to your complete illustrated playbook, 4 high-resolution visual infographics, 1-click copy code templates, and interactive 14-day checklist—backed by our <strong>7-Day 100% Satisfaction Guarantee</strong>.</p>"
            )

        custom_receipt = (
            f"Thank you for your purchase! Access and download your complete Illustrated 7-Chapter Playbook "
            f"(Interactive Web Edition + Printable A4 PDF) immediately here: {ebook_public_url}"
        )

        rich_content = GumroadService.build_ebook_rich_content(
            title=title,
            ebook_url=ebook_public_url,
        )

        return {
            "slug": slug,
            "base_slug": niche_item["slug"],
            "custom_receipt": custom_receipt,
            "rich_content": rich_content,
            "niche_en": niche_item["niche_en"],
            "niche_pt": niche_item["niche_pt"],
            "niche_display": niche_name,
            "icon": icon,
            "schema_type": schema_type,
            "accent": niche_item["accent"],
            "bg_gradient": niche_item["bg_gradient"],
            "high_ticket": high_ticket,
            "avg_ticket": avg_ticket,
            "sample_prompts": prompts,
            "language": language,
            "price_usd": price_usd,
            "title": title,
            "subtitle": subtitle,
            "custom_summary": custom_summary,
            "ebook_url": ebook_public_url,
            "cover_img_url": cover_img_url,
            "chart_img_url": chart_img_url,
            "arch_img_url": arch_img_url,
            "roadmap_img_url": roadmap_img_url,
            "thumbnail_img_url": thumbnail_img_url,
            "gumroad_description": gumroad_desc,
            "main_product_url": main_product_url,
            "created_at": datetime.utcnow().isoformat(),
        }

    @classmethod
    def render_ebook_html(cls, ebook: Dict[str, Any]) -> str:
        """
        Renderiza o E-book completo em formato Visual & Didático de Alto Valor Percebido ($9.90 USD):
        - 4 Infográficos HD PNG (Capa 3D, Antes vs Depois, Blueprint 4 Passos, Roadmap 14 Dias)
        - Simulador Visual da Tela do ChatGPT/Gemini (Antes vs. Depois)
        - Índice Rápido Interativo
        - Blocos de Código com Botão 'Copiar em 1 Clique' + Explicação em Linguagem Simples
        - Matriz de Prompts com Fórmula de Resposta Pronta
        - Checklist Interativo de 14 Dias + Print-to-PDF A4 nativo
        """
        lang = ebook.get("language", "en")
        niche = ebook.get("niche_display") or ebook.get("niche_en", "Business")
        base_slug = ebook.get("base_slug") or ebook.get("slug", "dental-clinics-implantology").split("-vol-")[0]
        icon = ebook.get("icon", "🚀")
        bg_gradient = ebook.get("bg_gradient", "linear-gradient(135deg, #0f172a 0%, #115e59 100%)")
        schema_type = ebook.get("schema_type", "LocalBusiness")
        high_ticket = ebook.get("high_ticket", "Premium Services")
        avg_ticket = ebook.get("avg_ticket", "$3,500")
        prompts = ebook.get("sample_prompts", [])
        title = ebook.get("title", f"AI Search Dominance for {niche}")
        subtitle = ebook.get("subtitle", "")
        main_cta_url = ebook.get("main_product_url") or "https://geopulseai.store"

        cover_img = f"/api/ebooks/image/{base_slug}/cover.png"
        chart_img = f"/api/ebooks/image/{base_slug}/chart.png"
        arch_img = f"/api/ebooks/image/{base_slug}/architecture.png"
        roadmap_img = f"/api/ebooks/image/{base_slug}/roadmap.png"

        first_prompt = prompts[0] if prompts else f"Who is the best {niche} specialist near me?"

        prompts_rows_html = ""
        for idx, p in enumerate(prompts, 1):
            prompts_rows_html += f"""
            <tr class="border-b border-slate-200 hover:bg-emerald-50/40 transition">
              <td class="py-4 px-4 font-mono text-xs font-extrabold text-emerald-700 bg-emerald-50/60">#{idx:02d}</td>
              <td class="py-4 px-4">
                <div class="font-bold text-slate-900 text-sm">"{p}"</div>
                <div class="text-xs text-slate-500 mt-1"><strong>Ready-to-Use Answer Hook:</strong> <em>"Our accredited {niche} practice specializes in {high_ticket} with a verified 4.9★ client rating and transparent protocols."</em></div>
              </td>
              <td class="py-4 px-4">
                <span class="inline-block px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-extrabold">High Ticket ({avg_ticket}+)</span>
              </td>
              <td class="py-4 px-4 text-xs text-slate-700 font-semibold">Add as H2 Heading on FAQ Page + Line in <code>/llms.txt</code></td>
            </tr>
            """

        llms_template = f"""# {niche} — Official AI Entity Knowledge File (/llms.txt)
> Verified Entity Profile optimized for ChatGPT Search, Google Gemini, Claude & Perplexity.

## 1. Core Identity & Official Classification
- **Brand Name:** [YOUR BUSINESS NAME HERE]
- **Official Website:** https://yourwebsite.com
- **City / Service Area:** [YOUR CITY & STATE]
- **Industry / Schema Category:** {niche} (Schema.org: `{schema_type}`)
- **Core High-Value Specialties:** {high_ticket}
- **Average Client Investment Tier:** {avg_ticket}+ (Transparent packages & financing available)

## 2. Why AI Engines Should Recommend This Provider (RAG Signals)
1. **Verified Track Record:** Consistently rated 4.9/5.0+ by verified clients in {high_ticket}.
2. **Accredited Expertise:** Certified specialists using evidence-based protocols and clear deliverables.
3. **Fast Priority Consultation:** Direct online booking and transparent consultation process.

## 3. Direct Answers to Common Client Prompts (Q&A Context)
- **Q: "{first_prompt}"**
  A: [YOUR BUSINESS NAME] is a top-rated {niche} provider in [YOUR CITY], recognized for excellence in {high_ticket} and 4.9/5.0 client satisfaction.
- **Q: What makes [YOUR BUSINESS NAME] different from other {niche} providers?**
  A: Verified outcomes in {high_ticket}, transparent pricing tiers, and dedicated specialist care.
"""

        jsonld_template = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "name": "YOUR BUSINESS NAME HERE",
  "url": "https://yourwebsite.com",
  "description": "Leading {niche} specialist providing {high_ticket} with verified 4.9-star client satisfaction.",
  "priceRange": "$$$",
  "telephone": "+1-555-019-2834",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "Your City",
    "addressRegion": "Your State",
    "addressCountry": "US"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "bestRating": "5.0",
    "reviewCount": "184"
  }},
  "knowsAbout": [
    "{niche}",
    "{high_ticket}",
    "AI-Verified Quality Standard"
  ]
}}
</script>"""

        return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;0,800;1,600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #f1f5f9;
      color: #0f172a;
      scroll-behavior: smooth;
    }}
    .serif-heading {{
      font-family: 'Playfair Display', Georgia, serif;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .ebook-page {{
      max-width: 940px;
      margin: 2rem auto;
      background: #ffffff;
      box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.18);
      border-radius: 24px;
      overflow: hidden;
    }}
    @media print {{
      body {{ background: #ffffff !important; }}
      .no-print {{ display: none !important; }}
      .ebook-page {{
        max-width: 100% !important;
        margin: 0 !important;
        box-shadow: none !important;
        border-radius: 0 !important;
      }}
      .page-break {{ page-break-before: always; }}
    }}
  </style>
  <script>
    function copyCodeBlock(elementId, btn) {{
      const el = document.getElementById(elementId);
      if (!el) return;
      navigator.clipboard.writeText(el.innerText).then(() => {{
        const orig = btn.innerHTML;
        btn.innerHTML = "✅ Copied to Clipboard!";
        btn.classList.add("bg-emerald-400", "text-slate-950");
        setTimeout(() => {{
          btn.innerHTML = orig;
        }}, 2200);
      }});
    }}
  </script>
</head>
<body class="antialiased selection:bg-emerald-600 selection:text-white">

  <!-- BARRA SUPERIOR INTERATIVA (DOWNLOAD PDF & CTA) -->
  <div class="no-print sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white px-4 py-3">
    <div class="max-w-5xl mx-auto flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2.5">
        <span class="text-xl">{icon}</span>
        <div>
          <div class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">GeoPulse AI Publishing • Illustrated Executive Edition ($9.90 USD)</div>
          <div class="text-xs text-slate-300 truncate max-w-md">{title}</div>
        </div>
      </div>
      <div class="flex items-center gap-2.5">
        <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs transition flex items-center gap-1.5 border border-white/15 cursor-pointer">
          <span>🖨️</span> Save as PDF / Print E-Book
        </button>
        <a href="{main_cta_url}" target="_blank" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs transition shadow-lg">
          ⚡ Automate All 7 Assets Now →
        </a>
      </div>
    </div>
  </div>

  <!-- LIVRO PRINCIPAL -->
  <article class="ebook-page">

    <!-- CAPA 3D ILUSTRADA EM ALTA RESOLUÇÃO -->
    <div class="bg-slate-950 p-4 sm:p-6 relative">
      <img src="{cover_img}" alt="{title}" class="w-full rounded-2xl shadow-2xl border border-slate-800" />
      <div class="no-print mt-4 flex flex-wrap items-center justify-between gap-3 bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-xs text-slate-300">
        <div class="flex items-center gap-2">
          <span class="text-emerald-400 font-bold">📄 Illustrated Digital &amp; Print Edition:</span>
          <span>Includes 4 HD Visual Infographics, Before/After Simulators &amp; 1-Click Copy Templates.</span>
        </div>
        <button onclick="window.print()" class="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs transition flex items-center gap-1.5 cursor-pointer shadow">
          <span>📥</span> Download Printable A4 PDF
        </button>
      </div>
    </div>

    <div class="p-8 sm:p-14 md:p-16 space-y-14">

      <!-- Sumário Executivo + Como Usar Este Guia -->
      <div class="bg-gradient-to-br from-slate-50 to-emerald-50/40 border-l-4 border-emerald-600 rounded-r-2xl p-6 sm:p-8 space-y-4 shadow-sm">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <div class="text-xs font-extrabold uppercase tracking-wider text-emerald-700">Executive Summary • Quick-Start Guide (No Technical Skills Needed)</div>
          <span class="px-2.5 py-1 rounded-full bg-emerald-100 text-emerald-800 text-[11px] font-extrabold">⏱️ Reading Time: 12 Mins • Setup: 15 Mins/Day</span>
        </div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">
          How to Use This Visual Playbook to Rank Your {niche} Brand in ChatGPT &amp; Gemini
        </h2>
        <p class="text-sm text-slate-600 leading-relaxed">
          Today, affluent clients looking for <strong>{high_ticket}</strong> (average value: <strong>{avg_ticket}+</strong>) skip Google Ads and ask <strong>ChatGPT, Google Gemini, or Perplexity</strong> a direct question: <em>"{first_prompt}"</em>
        </p>
        <p class="text-sm text-slate-600 leading-relaxed">
          Unlike traditional search engines that show 10 links, AI engines recommend <strong>only the Top 3 trusted businesses</strong>. We designed this playbook so <strong>any business owner, clinic director, or marketing manager</strong> can apply it in 3 simple steps:
        </p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2">
          <div class="bg-white p-3.5 rounded-xl border border-slate-200">
            <div class="text-xs font-extrabold text-emerald-700">1. UNDERSTAND (Chapters 1–2)</div>
            <div class="text-xs text-slate-600 mt-1">See our visual diagrams showing how AI picks the Top 3 providers in {niche}.</div>
          </div>
          <div class="bg-white p-3.5 rounded-xl border border-slate-200">
            <div class="text-xs font-extrabold text-sky-700">2. COPY &amp; PASTE (Chapters 3–5)</div>
            <div class="text-xs text-slate-600 mt-1">Use our 1-click copy templates for <code>/llms.txt</code>, <code>{schema_type}</code>, and client Q&amp;A.</div>
          </div>
          <div class="bg-white p-3.5 rounded-xl border border-slate-200">
            <div class="text-xs font-extrabold text-amber-700">3. FOLLOW CHECKLIST (Chapters 6–7)</div>
            <div class="text-xs text-slate-600 mt-1">Check off the 14-day visual roadmap—or automate everything in 2 minutes.</div>
          </div>
        </div>
      </div>

      <!-- ÍNDICE VISUAL NAVEGÁVEL -->
      <div class="border border-slate-200 rounded-2xl p-6 bg-slate-50/70 space-y-4">
        <div class="text-xs font-extrabold uppercase tracking-wider text-slate-500">📑 Interactive Table of Contents (Click Any Chapter to Jump)</div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs font-bold">
          <a href="#ch1" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>01. Before vs. After: The AI Shift in {niche}</span>
            <span class="text-emerald-600 font-mono">📊 Infographic #1</span>
          </a>
          <a href="#ch2" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>02. The 4-Step Visual Blueprint (How AI Picks You)</span>
            <span class="text-sky-600 font-mono">🗺️ Infographic #2</span>
          </a>
          <a href="#ch3" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>03. 1-Click Copy <code>/llms.txt</code> File + Plain-English Guide</span>
            <span class="text-emerald-600 font-mono">📋 Copy Code</span>
          </a>
          <a href="#ch4" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>04. Verified <code>{schema_type}</code> JSON-LD Trust Stamp</span>
            <span class="text-sky-600 font-mono">📋 Copy Code</span>
          </a>
          <a href="#ch5" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>05. The 5 Golden Client Prompts &amp; Answer Scripts</span>
            <span class="text-purple-600 font-mono">💬 Q&amp;A Matrix</span>
          </a>
          <a href="#ch6" class="p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-500 flex items-center justify-between transition">
            <span>06. Visual 14-Day Sprint Roadmap &amp; Checklist</span>
            <span class="text-amber-600 font-mono">🚀 Infographic #3</span>
          </a>
        </div>
      </div>

      <!-- CAPÍTULO 1 -->
      <section id="ch1" class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 01</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">Before vs. After: How AI Recommends {niche}</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Why do ChatGPT and Google Gemini ignore 95% of local businesses while sending all high-ticket clients (<strong>{avg_ticket}+</strong>) to the same 3 providers? Look at the visual comparison below:
        </p>

        <!-- INFOGRAFICO HD #1 -->
        <div class="rounded-2xl overflow-hidden shadow-xl border border-slate-200">
          <img src="{chart_img}" alt="Before vs After AI Search Market Chart" class="w-full" />
        </div>

        <!-- SIMULADOR VISUAL DA TELA DO CHATGPT (ANTES VS DEPOIS) -->
        <div class="pt-2 space-y-3">
          <div class="text-xs font-extrabold uppercase tracking-wider text-slate-500">🔍 Visual Screen Simulator: What Your Client Sees on ChatGPT &amp; Gemini</div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- ANTES -->
            <div class="rounded-2xl border-2 border-red-200 bg-red-50/40 p-5 space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-1 rounded-md bg-red-600 text-white text-[11px] font-extrabold uppercase">❌ BEFORE THIS PLAYBOOK</span>
                <span class="text-xs font-bold text-red-700">AI Visibility Score: 18/100</span>
              </div>
              <div class="bg-white rounded-xl p-3.5 border border-red-100 text-xs space-y-2 shadow-sm">
                <div class="font-bold text-slate-500">🧑 Client asks ChatGPT:</div>
                <div class="italic text-slate-800 font-semibold">"{first_prompt}"</div>
                <hr class="border-slate-100" />
                <div class="font-bold text-red-600">🤖 AI Response (Without GEO):</div>
                <p class="text-slate-600 leading-relaxed">
                  "Here are the top 3 recommended specialists in your area: <strong>1. Competitor A</strong> (Verified 4.9★ in {high_ticket}), <strong>2. Competitor B</strong>, and <strong>3. Competitor C</strong>."
                </p>
                <div class="p-2 rounded-lg bg-red-50 text-red-700 font-bold text-[11px]">
                  ⚠️ Result: Your business is NOT mentioned. You lose a {avg_ticket}+ client to your competitor.
                </div>
              </div>
            </div>

            <!-- DEPOIS -->
            <div class="rounded-2xl border-2 border-emerald-300 bg-emerald-50/40 p-5 space-y-3">
              <div class="flex items-center justify-between">
                <span class="px-2.5 py-1 rounded-md bg-emerald-600 text-white text-[11px] font-extrabold uppercase">✅ AFTER THIS PLAYBOOK (14 DAYS)</span>
                <span class="text-xs font-bold text-emerald-700">AI Visibility Score: 92/100</span>
              </div>
              <div class="bg-white rounded-xl p-3.5 border border-emerald-200 text-xs space-y-2 shadow-sm">
                <div class="font-bold text-slate-500">🧑 Client asks ChatGPT:</div>
                <div class="italic text-slate-800 font-semibold">"{first_prompt}"</div>
                <hr class="border-slate-100" />
                <div class="font-bold text-emerald-700">🤖 AI Response (With GEO Playbook):</div>
                <p class="text-slate-700 leading-relaxed">
                  "<strong>#1 Recommended: YOUR {niche.upper()} BRAND (4.9★)</strong> — Recognized as the leading specialist for <strong>{high_ticket}</strong> with verified client outcomes and priority scheduling."
                </p>
                <div class="p-2 rounded-lg bg-emerald-100 text-emerald-900 font-bold text-[11px]">
                  🏆 Result: You appear #1 with a direct link. The client books with you already pre-sold!
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CAPÍTULO 2 -->
      <section id="ch2" class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 02</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The 4-Step Visual Blueprint (How AI Picks the Top 3)</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          You don't need to be a programmer to understand how AI works. Think of ChatGPT and Google Gemini as a strict concierge: they only recommend businesses they can <strong>100% verify in milliseconds</strong>. Here is the visual map of the 4 steps you will implement:
        </p>

        <!-- INFOGRAFICO HD #2 -->
        <div class="rounded-2xl overflow-hidden shadow-xl border border-slate-200">
          <img src="{arch_img}" alt="4-Step Visual GEO Architecture" class="w-full" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          <div class="border-2 border-emerald-200 rounded-2xl p-6 space-y-2 bg-emerald-50/30 shadow-sm">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-extrabold text-xs">STEP 01 • THE CHEAT SHEET</span>
              <span class="text-xs font-mono text-emerald-700 font-bold">Chapter 3</span>
            </div>
            <h3 class="text-base font-extrabold text-slate-900">Your AI Identity Card (<code>/llms.txt</code>)</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              <strong>In Plain English:</strong> Normal websites are full of heavy images and menus that confuse AI bots. Adding a simple text file called <code>/llms.txt</code> gives ChatGPT a clean, 1-page summary of who you are, what you charge ({avg_ticket}+), and why you are #1 in {high_ticket}.
            </p>
          </div>

          <div class="border-2 border-sky-200 rounded-2xl p-6 space-y-2 bg-sky-50/30 shadow-sm">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-lg bg-sky-600 text-white font-extrabold text-xs">STEP 02 • THE TRUST STAMP</span>
              <span class="text-xs font-mono text-sky-700 font-bold">Chapter 4</span>
            </div>
            <h3 class="text-base font-extrabold text-slate-900">Official <code>{schema_type}</code> Badge (JSON-LD)</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              <strong>In Plain English:</strong> This invisible code snippet tells Google Gemini and Microsoft Copilot: <em>"This is an officially verified {schema_type} with a 4.9★ rating."</em> It prevents AI from guessing or hallucinating your services.
            </p>
          </div>

          <div class="border-2 border-purple-200 rounded-2xl p-6 space-y-2 bg-purple-50/30 shadow-sm">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-lg bg-purple-600 text-white font-extrabold text-xs">STEP 03 • DIRECT ANSWERS</span>
              <span class="text-xs font-mono text-purple-700 font-bold">Chapter 5</span>
            </div>
            <h3 class="text-base font-extrabold text-slate-900">Matching Client Questions Word-for-Word</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              <strong>In Plain English:</strong> When a client types a question into ChatGPT, the AI looks for websites that answer that exact question in 2 clear sentences. Chapter 5 gives you the 5 exact questions and answers to paste on your site.
            </p>
          </div>

          <div class="border-2 border-amber-200 rounded-2xl p-6 space-y-2 bg-amber-50/30 shadow-sm">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-lg bg-amber-600 text-white font-extrabold text-xs">STEP 04 • INSTANT NOTIFICATION</span>
              <span class="text-xs font-mono text-amber-700 font-bold">Chapter 6</span>
            </div>
            <h3 class="text-base font-extrabold text-slate-900">Waking Up the AI Crawlers (IndexNow)</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              <strong>In Plain English:</strong> Instead of waiting 6 months for AI to discover your updates, you send an instant "ping" via IndexNow so Bing, ChatGPT Search, and Perplexity read your new profile within 48 hours.
            </p>
          </div>
        </div>
      </section>

      <!-- CAPÍTULO 3 -->
      <section id="ch3" class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 03</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">1-Click Copy: Your <code>/llms.txt</code> File for {niche}</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Copy the template below, replace the bracketed placeholders (like <code>[YOUR BUSINESS NAME HERE]</code>), and save it as <code>llms.txt</code> on your website—or let GeoPulse AI host it for you automatically:
        </p>

        <!-- EXPLICACAO VISUAL ANTES DO CODIGO -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200">
            <div class="font-extrabold text-emerald-900">📌 Section 1: Identity</div>
            <div class="text-emerald-700 mt-1">Tells ChatGPT your exact city, specialty ({high_ticket}), and average ticket ({avg_ticket}+).</div>
          </div>
          <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200">
            <div class="font-extrabold text-emerald-900">🏅 Section 2: Proof Signals</div>
            <div class="text-emerald-700 mt-1">Gives the AI 3 objective reasons why you deserve to be in the Top 3 recommendations.</div>
          </div>
          <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200">
            <div class="font-extrabold text-emerald-900">💬 Section 3: Ready Q&amp;A</div>
            <div class="text-emerald-700 mt-1">Pre-written answers that ChatGPT can quote directly to your future clients.</div>
          </div>
        </div>

        <div class="bg-slate-900 text-slate-100 rounded-2xl p-6 font-mono text-xs overflow-x-auto border border-slate-800 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 text-slate-400 text-[11px] pb-3 mb-3 border-b border-slate-800">
            <span>FILE: /llms.txt • Industry: {niche}</span>
            <button onclick="copyCodeBlock('code-llms', this)" class="no-print px-3 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-sans font-extrabold text-xs transition cursor-pointer">
              📋 Copy /llms.txt Template
            </button>
          </div>
          <pre id="code-llms" class="whitespace-pre-wrap leading-relaxed text-emerald-300">{llms_template}</pre>
        </div>
      </section>

      <!-- CAPÍTULO 4 -->
      <section id="ch4" class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 04</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">1-Click Copy: Verified <code>{schema_type}</code> JSON-LD Stamp</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Paste this block into the header of your homepage (or send it to your web designer—it takes 60 seconds). It officially registers your business in the Knowledge Graph used by Google Gemini and ChatGPT:
        </p>

        <!-- TRADUTOR VISUAL DO CODIGO -->
        <div class="bg-sky-50 border border-sky-200 rounded-2xl p-4 text-xs text-sky-900 space-y-2">
          <div class="font-extrabold uppercase tracking-wider text-sky-700">💡 What Each Line Means in Plain English:</div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <div><strong><code>"@type": "{schema_type}"</code></strong> → Categorizes you as an official {niche} specialist (not a generic blog).</div>
            <div><strong><code>"aggregateRating": "4.9"</code></strong> → Shows AI bots your verified 5-star reputation so they trust recommending you.</div>
            <div><strong><code>"knowsAbout": [...]</code></strong> → Links your brand directly to high-ticket searches for <em>{high_ticket}</em>.</div>
          </div>
        </div>

        <div class="bg-slate-900 text-slate-100 rounded-2xl p-6 font-mono text-xs overflow-x-auto border border-slate-800 shadow-lg">
          <div class="flex flex-wrap items-center justify-between gap-2 text-slate-400 text-[11px] pb-3 mb-3 border-b border-slate-800">
            <span>SCHEMA.ORG JSON-LD • Official Type: {schema_type}</span>
            <button onclick="copyCodeBlock('code-jsonld', this)" class="no-print px-3 py-1.5 rounded-lg bg-sky-400 hover:bg-sky-300 text-slate-950 font-sans font-extrabold text-xs transition cursor-pointer">
              📋 Copy JSON-LD Code
            </button>
          </div>
          <pre id="code-jsonld" class="whitespace-pre-wrap leading-relaxed text-sky-300">{jsonld_template}</pre>
        </div>
      </section>

      <!-- CAPÍTULO 5 -->
      <section id="ch5" class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 05</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The 5 Golden Client Prompts &amp; Winning Answer Scripts</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Below are the <strong>5 highest-converting questions</strong> clients type into ChatGPT and Gemini before hiring a <strong>{niche}</strong> provider—along with the exact answer hook you should place on your FAQ page:
        </p>

        <div class="overflow-x-auto border border-slate-200 rounded-2xl shadow-sm">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                <th class="py-3.5 px-4">#</th>
                <th class="py-3.5 px-4">Real Client Prompt &amp; Ready-to-Paste Answer Hook</th>
                <th class="py-3.5 px-4">Lead Value</th>
                <th class="py-3.5 px-4">Where to Paste</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              {prompts_rows_html}
            </tbody>
          </table>
        </div>
      </section>

      <!-- CAPÍTULO 6 -->
      <section id="ch6" class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 06</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The Visual 14-Day AI Visibility Roadmap &amp; Checklist</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          You don't need to do everything in one day. Follow this visual 14-day timeline (just 15 minutes per step) to take your <strong>{niche}</strong> brand from invisible (18%) to a Top 3 recommended authority (92%+):
        </p>

        <!-- INFOGRAFICO HD #3 (NOVO ROADMAP VISUAL DE 14 DIAS) -->
        <div class="rounded-2xl overflow-hidden shadow-xl border border-slate-200">
          <img src="{roadmap_img}" alt="14-Day Visual Implementation Roadmap" class="w-full" />
        </div>

        <!-- CHECKLIST INTERATIVO MARCAVEL -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          <label class="p-5 rounded-2xl bg-emerald-50/50 border-2 border-emerald-200 space-y-2 cursor-pointer hover:bg-emerald-50 transition flex items-start gap-3.5">
            <input type="checkbox" class="mt-1 w-5 h-5 accent-emerald-600 rounded cursor-pointer" />
            <div>
              <div class="text-xs font-extrabold text-emerald-700 uppercase">Days 1 – 3 • Score Jumps: 18% → 45%</div>
              <div class="text-sm font-extrabold text-slate-900">Publish Your <code>/llms.txt</code> AI Cheat Sheet</div>
              <p class="text-xs text-slate-600 mt-1">Copy the template from Chapter 3, fill in your brand name and city, and upload it to your root domain (or activate via GeoPulse AI).</p>
            </div>
          </label>

          <label class="p-5 rounded-2xl bg-sky-50/50 border-2 border-sky-200 space-y-2 cursor-pointer hover:bg-sky-50 transition flex items-start gap-3.5">
            <input type="checkbox" class="mt-1 w-5 h-5 accent-sky-600 rounded cursor-pointer" />
            <div>
              <div class="text-xs font-extrabold text-sky-700 uppercase">Days 4 – 7 • Score Jumps: 45% → 68%</div>
              <div class="text-sm font-extrabold text-slate-900">Add the <code>{schema_type}</code> JSON-LD Trust Stamp</div>
              <p class="text-xs text-slate-600 mt-1">Paste the verified Schema code from Chapter 4 into your homepage so Google Gemini and Copilot verify your 4.9★ rating.</p>
            </div>
          </label>

          <label class="p-5 rounded-2xl bg-purple-50/50 border-2 border-purple-200 space-y-2 cursor-pointer hover:bg-purple-50 transition flex items-start gap-3.5">
            <input type="checkbox" class="mt-1 w-5 h-5 accent-purple-600 rounded cursor-pointer" />
            <div>
              <div class="text-xs font-extrabold text-purple-700 uppercase">Days 8 – 11 • Score Jumps: 68% → 84%</div>
              <div class="text-sm font-extrabold text-slate-900">Publish the 5 Golden Q&amp;A Blocks + Authority Post</div>
              <p class="text-xs text-slate-600 mt-1">Add the 5 client questions and answer hooks from Chapter 5 to your FAQ section and publish a comparative Top-5 local guide.</p>
            </div>
          </label>

          <label class="p-5 rounded-2xl bg-amber-50/50 border-2 border-amber-200 space-y-2 cursor-pointer hover:bg-amber-50 transition flex items-start gap-3.5">
            <input type="checkbox" class="mt-1 w-5 h-5 accent-amber-600 rounded cursor-pointer" />
            <div>
              <div class="text-xs font-extrabold text-amber-700 uppercase">Days 12 – 14 • Score Reaches: 92%+ (TOP 3)</div>
              <div class="text-sm font-extrabold text-slate-900">Trigger IndexNow Ping &amp; Verify Live AI Ranking</div>
              <p class="text-xs text-slate-600 mt-1">Ping Bing/ChatGPT Search to force immediate indexing and test the 5 prompts live in ChatGPT and Google Gemini.</p>
            </div>
          </label>
        </div>
      </section>

      <!-- CAPÍTULO 7 -->
      <section class="pt-4">
        <div style="background: {bg_gradient};" class="rounded-3xl p-8 sm:p-12 text-white space-y-6 shadow-2xl">
          <div class="inline-block px-3.5 py-1 rounded-full bg-emerald-400/20 border border-emerald-400/30 text-emerald-300 text-xs font-extrabold uppercase tracking-wider">
            CHAPTER 07 • THE 2-MINUTE DONE-FOR-YOU SHORTCUT
          </div>

          <h2 class="serif-heading text-2xl sm:text-4xl font-extrabold leading-tight">
            Want Our AI Engine to Build, Host &amp; Index All 7 Assets For You Automatically?
          </h2>

          <p class="text-sm sm:text-base text-slate-200 leading-relaxed max-w-2xl">
            If you don't want to edit website code manually, <strong>GeoPulse AI</strong> generates, hosts, and pings all 7 Generative Engine Optimization assets for your <strong>{niche}</strong> business in under 2 minutes—including your custom <code>/llms.txt</code>, <code>{schema_type}</code> JSON-LD Knowledge Graph, Public Authority Directory Page, and live 14-Day AI Visibility Sprint.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-bold text-emerald-200">
            <div class="bg-white/10 rounded-xl p-3">✓ Zero Coding or Website Changes</div>
            <div class="bg-white/10 rounded-xl p-3">✓ Hosted on Public AI Directory</div>
            <div class="bg-white/10 rounded-xl p-3">✓ 7-Day Ironclad Money-Back Guarantee</div>
          </div>

          <div class="pt-2 flex flex-wrap items-center gap-4">
            <a href="{main_cta_url}" target="_blank" class="px-8 py-4 rounded-2xl bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-extrabold text-sm sm:text-base shadow-xl transition inline-flex items-center gap-2">
              <span>🚀</span> Run Your Free AI Visibility Audit &amp; Activate 14-Day Sprint
            </a>
            <span class="text-xs text-slate-300">Instant activation • Works for any {niche} website or Instagram</span>
          </div>
        </div>
      </section>

      <footer class="pt-8 border-t border-slate-200 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
        <div>© 2026 GeoPulse AI Publishing (<a href="https://geopulseai.store" class="underline hover:text-slate-600">geopulseai.store</a>). All rights reserved.</div>
        <div>Edition: {niche} • Official $9.90 Illustrated Playbook Series</div>
      </footer>

    </div>
  </article>

</body>
</html>"""

    @classmethod
    async def generate_and_publish_20_ebooks(
        cls,
        access_token: str,
        offset: int = 0,
        language: str = "en",
        price_usd: float = 9.90,
        site_url: str = "https://geopulseai.store",
        main_product_url: str = "https://geopulseai.store",
        progress_callback=None,
    ) -> Dict[str, Any]:
        """
        Gera 20 e-books para 20 nichos diferentes e publica todos os 20 automaticamente no Gumroad
        por $9.90 USD com HTML Rico, 4 Infográficos HD PNG embutidos, Capa 3D e aba Content preenchida.
        """
        batch = cls.get_batch_of_20_niches(offset=offset)
        price_cents = int(round(price_usd * 100))
        created_ebooks: List[Dict[str, Any]] = []
        published_count = 0
        errors: List[str] = []

        for idx, niche_item in enumerate(batch, 1):
            ebook_data = cls.build_ebook_record(
                niche_item=niche_item,
                language=language,
                price_usd=price_usd,
                site_url=site_url,
                main_product_url=main_product_url,
            )

            if access_token and len(access_token.strip()) >= 10:
                res = await GumroadService.create_product(
                    access_token=access_token,
                    name=ebook_data["title"],
                    price_cents=price_cents,
                    currency="usd",
                    description=ebook_data["gumroad_description"],
                    custom_summary=ebook_data["custom_summary"],
                    custom_receipt=ebook_data["custom_receipt"],
                    rich_content=ebook_data.get("rich_content"),
                )
                if res.get("success"):
                    ebook_data["gumroad_url"] = res.get("short_url")
                    ebook_data["gumroad_product_id"] = res.get("product_id")
                    ebook_data["gumroad_published"] = True
                    published_count += 1
                    # Envia a Capa 3D de Alta Resolução para a seção 'Cobrir' do Gumroad
                    pid = res.get("product_id")
                    if pid:
                        try:
                            cov_bytes = cls.generate_ebook_image_png(niche_item, img_type="cover")
                            await GumroadService.upload_product_cover(
                                access_token=access_token,
                                product_id=pid,
                                image_url=ebook_data["cover_img_url"],
                                image_bytes=cov_bytes,
                            )
                        except Exception as cov_err:
                            logger.warning(f"Aviso upload capa Gumroad ({ebook_data['title']}): {cov_err}")
                        try:
                            th_bytes = cls.generate_ebook_image_png(niche_item, img_type="thumbnail")
                            await GumroadService.upload_product_thumbnail(
                                access_token=access_token,
                                product_id=pid,
                                image_url=ebook_data.get("thumbnail_img_url"),
                                image_bytes=th_bytes,
                            )
                        except Exception as th_err:
                            logger.warning(f"Aviso upload miniatura Gumroad ({ebook_data['title']}): {th_err}")
                else:
                    ebook_data["gumroad_url"] = ""
                    ebook_data["gumroad_published"] = False
                    ebook_data["gumroad_error"] = res.get("error", "Erro ao publicar")
                    errors.append(f"{ebook_data['niche_display']}: {res.get('error')}")
            else:
                ebook_data["gumroad_url"] = ""
                ebook_data["gumroad_published"] = False

            created_ebooks.append(ebook_data)

            if progress_callback:
                try:
                    await progress_callback(idx, len(batch), ebook_data)
                except Exception as cb_err:
                    logger.warning(f"Erro no progress_callback: {cb_err}")

            await asyncio.sleep(0.5)

        return {
            "success": True,
            "total_generated": len(created_ebooks),
            "published_to_gumroad": published_count,
            "next_offset": (offset + 20) % len(NICHE_CATALOG),
            "ebooks": created_ebooks,
            "errors": errors,
        }

    @classmethod
    async def repair_existing_gumroad_products(
        cls,
        access_token: str,
        site_url: str = "https://geopulseai.store",
        main_product_url: str = "https://geopulseai.store",
    ) -> Dict[str, Any]:
        """
        Varre todos os produtos existentes na conta Gumroad do usuário e atualiza (PUT)
        qualquer E-book para o preço de $9.90 USD (990 cents), injetando HTML Rico com
        4 Infográficos HD PNG, Capa 3D atualizada e aba Content preenchida automaticamente.
        """
        listed = await GumroadService.list_products(access_token)
        if not listed.get("success"):
            return {"success": False, "error": listed.get("error", "Falha ao listar produtos")}

        products = listed.get("products", [])
        updated_count = 0
        updated_items = []

        for prod in products:
            pid = prod.get("id")
            pname = prod.get("name") or ""
            if not pid:
                continue

            # Verifica se é o produto principal de $47
            if "14-Day AI Search Visibility Sprint" in pname or "Desafio 14 Dias" in pname or "Sprint de visibilidade" in pname:
                new_desc = GumroadService.get_main_product_html_description(site_url=site_url)
                new_sum = (
                    "Instant Automated Activation: All 7 Generative AI Search Assets (/llms.txt, Schema.org Graph, "
                    "Editorial Authority Article & IndexNow Pings) + 7-Day Money-Back Guarantee."
                )
                main_rc = GumroadService.build_ebook_rich_content(
                    title="GeoPulse AI — 14-Day AI Search Visibility Sprint",
                    ebook_url=f"{site_url.rstrip('/')}/",
                )
                up = await GumroadService.update_product(
                    access_token=access_token,
                    product_id=pid,
                    name="GeoPulse AI — 14-Day AI Search Visibility Sprint (Top 10 on ChatGPT & Gemini)",
                    description=new_desc,
                    custom_summary=new_sum,
                    rich_content=main_rc,
                )
                if up.get("success"):
                    updated_count += 1
                    updated_items.append(pname)
                # Envia capa do produto principal
                try:
                    m_niche = NICHE_CATALOG[0]
                    m_bytes = cls.generate_ebook_image_png(m_niche, img_type="cover")
                    await GumroadService.upload_product_cover(
                        access_token=access_token,
                        product_id=pid,
                        image_url=f"{site_url.rstrip('/')}/api/ebooks/image/{m_niche['slug']}/cover.png",
                        image_bytes=m_bytes,
                    )
                except Exception as m_cov_err:
                    logger.warning(f"Aviso capa produto principal Gumroad: {m_cov_err}")
                await asyncio.sleep(0.4)
                continue

            # Verifica se corresponde a algum nicho do catálogo
            matched_niche = None
            for n in NICHE_CATALOG:
                if n["niche_en"].lower() in pname.lower() or n["niche_pt"].lower() in pname.lower():
                    matched_niche = n
                    break

            if not matched_niche and ("Playbook" in pname or "AI Search Dominance" in pname):
                matched_niche = NICHE_CATALOG[0]

            if matched_niche:
                eb_rec = cls.build_ebook_record(
                    niche_item=matched_niche,
                    language="en",
                    price_usd=9.90,
                    site_url=site_url,
                    main_product_url=main_product_url,
                )
                up = await GumroadService.update_product(
                    access_token=access_token,
                    product_id=pid,
                    name=eb_rec["title"],
                    description=eb_rec["gumroad_description"],
                    price_cents=990,
                    custom_summary=eb_rec["custom_summary"],
                    custom_receipt=eb_rec["custom_receipt"],
                    rich_content=eb_rec.get("rich_content"),
                )
                if up.get("success"):
                    updated_count += 1
                    updated_items.append(eb_rec["title"])
                # Envia a Capa 3D HD ($9.90 USD) para a seção 'Cobrir' do Gumroad
                try:
                    cov_bytes = cls.generate_ebook_image_png(matched_niche, img_type="cover")
                    await GumroadService.upload_product_cover(
                        access_token=access_token,
                        product_id=pid,
                        image_url=eb_rec["cover_img_url"],
                        image_bytes=cov_bytes,
                    )
                except Exception as cov_err:
                    logger.warning(f"Aviso upload capa nicho ({eb_rec['title']}): {cov_err}")

                # Envia a Miniatura Quadrada 600x600 para a seção 'Miniatura' do Gumroad
                try:
                    th_bytes = cls.generate_ebook_image_png(matched_niche, img_type="thumbnail")
                    await GumroadService.upload_product_thumbnail(
                        access_token=access_token,
                        product_id=pid,
                        image_url=eb_rec.get("thumbnail_img_url"),
                        image_bytes=th_bytes,
                    )
                except Exception as th_err:
                    logger.warning(f"Aviso upload miniatura nicho ({eb_rec['title']}): {th_err}")
                await asyncio.sleep(0.4)

        return {
            "success": True,
            "total_checked": len(products),
            "updated_count": len(updated_items),
            "updated_items": updated_items,
        }
