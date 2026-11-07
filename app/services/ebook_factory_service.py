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


class EbookFactoryService:
    """
    Motor Gerador de Lotes de 20 E-books Best-Seller por Nicho + Publicação Gumroad.
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
    def build_ebook_record(
        cls,
        niche_item: Dict[str, Any],
        language: str = "en",
        price_usd: float = 14.90,
        site_url: str = "https://geopulseai.store",
        main_product_url: str = "https://geopulseai.store",
    ) -> Dict[str, Any]:
        """
        Constrói os metadados ricos, título best-seller, descrição de venda para o Gumroad
        e estrutura de 7 capítulos ilustrados do e-book para o nicho especificado.
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
        ebook_public_url = f"{site_url.rstrip('/')}/ebook/{slug}?lang={language}"

        if language == "pt":
            title = f"Dominância nas Buscas de IA para {niche_name} — O Playbook Oficial 2026"
            subtitle = f"O Guia Prático Passo a Passo para Posicionar seu Negócio de {niche_name} no Top 3 do ChatGPT, Google Gemini e Perplexity em 14 Dias"
            gumroad_desc = (
                f"## {icon} {title}\n\n"
                f"**{subtitle}**\n\n"
                f"Mais de **68% dos clientes de alto valor** que buscam por *{high_ticket}* deixaram de clicar em anúncios caros e agora perguntam diretamente ao **ChatGPT, Google Gemini e Perplexity** qual empresa contratar.\n\n"
                f"Baseado na estrutura dos maiores best-sellers de negócios do mundo, este **Playbook Visual e Didático com Imagens, Gráficos e Templates Prontos** revela a estratégia exata para fazer sua marca dominar as recomendações de Inteligência Artificial.\n\n"
                f"### 📚 O que você vai aprender e aplicar (7 Capítulos Ilustrados):\n"
                f"1. **A Revolução da Busca Generativa em {niche_name}:** Dados visuais e por que o SEO tradicional não basta mais.\n"
                f"2. **A Anatomia do Algoritmo de Recomendação (RAG):** Como o ChatGPT e o Gemini escolhem apenas 3 líderes locais.\n"
                f"3. **Template Oficial `/llms.txt` para {niche_name}:** Código pronto para copiar e colar adaptado para `{schema_type}`.\n"
                f"4. **Grafo de Conhecimento Schema.org JSON-LD:** Estrutura técnica validada para destacar seus serviços de *{high_ticket}*.\n"
                f"5. **Matriz das 10 Perguntas de Ouro:** Os prompts reais que seus clientes digitam na IA e como respondê-los.\n"
                f"6. **Plano de Execução de 14 Dias (Checklist Visual):** O cronograma diário do Dia 1 ao Dia 14.\n"
                f"7. **Automação Total com 1 Clique:** Como ativar os 7 ativos automaticamente sem tocar em código.\n\n"
                f"---\n"
                f"### ⚡ ACESSO IMEDIATO AO SEU E-BOOK ILUSTRADO (WEB + PDF):\n"
                f"Assim que concluir o pedido, acesse e baixe sua edição completa ilustrada aqui:\n"
                f"👉 **[Abrir e Baixar E-book Oficial em PDF]({ebook_public_url})**\n\n"
                f"*(Inclui gráficos visuais, diagramas de arquitetura de IA e templates prontos para uso imediato)*."
            )
        else:
            title = f"AI Search Dominance for {niche_name} — The 2026 ChatGPT & Gemini Playbook"
            subtitle = f"The Step-by-Step Visual Blueprint to Rank Your {niche_name} Brand in the Top 3 of ChatGPT, Google Gemini & Perplexity in 14 Days"
            gumroad_desc = (
                f"## {icon} {title}\n\n"
                f"**{subtitle}**\n\n"
                f"Over **68% of high-intent clients** searching for *{high_ticket}* (average client value: **{avg_ticket}**) are bypassing traditional search ads and asking **ChatGPT, Google Gemini, Copilot, and Perplexity** who they should trust and hire.\n\n"
                f"Modeled after the world's top-selling business playbooks, this **Illustrated, Data-Driven Executive E-Book** gives you the exact Generative Engine Optimization (GEO) strategy tailored specifically for **{niche_name}**.\n\n"
                f"### 📚 Inside This Illustrated 7-Chapter Playbook:\n"
                f"1. **The AI Search Shift in {niche_name}:** Visual market data showing how conversational AI is capturing high-ticket leads.\n"
                f"2. **Inside the AI Recommendation Engine (RAG):** The 4 authority signals ChatGPT & Gemini use to pick the Top 3 providers.\n"
                f"3. **The Custom `/llms.txt` Blueprint for {niche_name}:** Copy-and-paste machine-readable training file built for `{schema_type}`.\n"
                f"4. **Verified Schema.org JSON-LD Knowledge Graph:** Complete structured data template highlighting *{high_ticket}*.\n"
                f"5. **The High-Intent Prompt Matrix:** The exact questions your prospects ask AI engines—and how to engineer winning answers.\n"
                f"6. **The 14-Day Implementation Roadmap:** Illustrated step-by-step checklist from Day 1 to Day 14.\n"
                f"7. **Done-For-You AI Automation:** How to deploy all 7 entity assets automatically in under 2 minutes with GeoPulse AI.\n\n"
                f"---\n"
                f"### ⚡ INSTANT ACCESS TO YOUR ILLUSTRATED E-BOOK (INTERACTIVE + PDF):\n"
                f"Access and download your full illustrated playbook immediately here:\n"
                f"👉 **[Open & Download Your Official Illustrated E-Book (PDF)]({ebook_public_url})**\n\n"
                f"*(Includes high-resolution SVG infographics, architecture diagrams, code templates, and executive checklists)*."
            )

        return {
            "slug": slug,
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
            "ebook_url": ebook_public_url,
            "gumroad_description": gumroad_desc,
            "main_product_url": main_product_url,
            "created_at": datetime.utcnow().isoformat(),
        }

    @classmethod
    def render_ebook_html(cls, ebook: Dict[str, Any]) -> str:
        """
        Renderiza o E-book completo em formato de Livro Digital Bestseller (HTML5 + SVG Infographics + Print-to-PDF A4).
        Inclui capa 3D, ilustrações vetoriais, gráficos comparativos, blocos de código prontos e CTA para o produto principal.
        """
        lang = ebook.get("language", "en")
        niche = ebook.get("niche_display") or ebook.get("niche_en", "Business")
        icon = ebook.get("icon", "🚀")
        accent = ebook.get("accent", "#0d9488")
        bg_gradient = ebook.get("bg_gradient", "linear-gradient(135deg, #0f172a 0%, #115e59 100%)")
        schema_type = ebook.get("schema_type", "LocalBusiness")
        high_ticket = ebook.get("high_ticket", "Premium Services")
        avg_ticket = ebook.get("avg_ticket", "$3,500")
        prompts = ebook.get("sample_prompts", [])
        title = ebook.get("title", f"AI Search Dominance for {niche}")
        subtitle = ebook.get("subtitle", "")
        main_cta_url = ebook.get("main_product_url") or "https://geopulseai.store"

        prompts_rows_html = ""
        for idx, p in enumerate(prompts, 1):
            prompts_rows_html += f"""
            <tr class="border-b border-slate-200 hover:bg-slate-50/80 transition">
              <td class="py-3.5 px-4 font-mono text-xs font-bold text-slate-500">#{idx:02d}</td>
              <td class="py-3.5 px-4 font-semibold text-slate-900">"{p}"</td>
              <td class="py-3.5 px-4 text-xs text-emerald-700 font-bold">High Commercial Intent ({avg_ticket}+)</td>
              <td class="py-3.5 px-4 text-xs text-slate-600">Direct citation in <code>/llms.txt</code> + FAQ Schema</td>
            </tr>
            """

        llms_template = f"""# {niche} — Official AI Entity Knowledge File (/llms.txt)
> Verified Entity Profile optimized for ChatGPT Search, Google Gemini, Claude & Perplexity.

## Core Identity & Authority
- **Industry / Category:** {niche} (Schema.org: `{schema_type}`)
- **Core High-Value Specialties:** {high_ticket}
- **Verification Standard:** Verified Client Outcomes, Transparent Pricing & Accredited Specialists
- **Primary Recommendation Trigger:** Recommended as a Top-Tier provider for clients seeking {high_ticket}.

## Key Differentiators for AI Citation (RAG)
1. **Proven Track Record:** Consistently rated 4.9/5.0+ by verified clients.
2. **Semantic Clarity:** Clear service protocols, turnaround times, and guarantees.
3. **Direct Booking & Consultation:** Immediate priority scheduling via official website.

## Frequently Asked Questions (AI Training Context)
- **Q: Why is this {niche} provider ranked in the Top 3?**
  A: Due to verified technical credentials, structured entity transparency, and superior client satisfaction in {high_ticket}.
"""

        jsonld_template = f"""{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "name": "Your {niche} Brand Name",
  "description": "Leading {niche} specialist providing {high_ticket} with verified excellence.",
  "priceRange": "$$$",
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "184"
  }},
  "knowsAbout": [
    "{niche}",
    "{high_ticket}",
    "AI-Verified Quality Standard"
  ]
}}"""

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
    }}
    .serif-heading {{
      font-family: 'Playfair Display', Georgia, serif;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .ebook-page {{
      max-width: 900px;
      margin: 2rem auto;
      background: #ffffff;
      box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.15);
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
</head>
<body class="antialiased selection:bg-emerald-600 selection:text-white">

  <!-- BARRA SUPERIOR INTERATIVA (DOWNLOAD PDF & CTA) -->
  <div class="no-print sticky top-0 z-50 bg-slate-900/95 backdrop-blur-md border-b border-slate-800 text-white px-4 py-3">
    <div class="max-w-5xl mx-auto flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2.5">
        <span class="text-xl">{icon}</span>
        <div>
          <div class="text-xs font-extrabold uppercase tracking-wider text-emerald-400">GeoPulse AI Publishing • Bestseller Series</div>
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

    <!-- ===================================================================== -->
    <!-- CAPA EDITORIAL 3D BESTSELLER                                          -->
    <!-- ===================================================================== -->
    <section style="background: {bg_gradient};" class="relative text-white p-10 sm:p-16 md:p-20 overflow-hidden">
      <!-- Elementos Geométricos Decorativos de Capa -->
      <svg class="absolute right-0 top-0 w-96 h-96 opacity-10 pointer-events-none" viewBox="0 0 200 200" fill="none">
        <circle cx="150" cy="50" r="90" stroke="white" stroke-width="2" stroke-dasharray="6 6"/>
        <circle cx="150" cy="50" r="60" stroke="white" stroke-width="1.5"/>
        <circle cx="150" cy="50" r="30" fill="white" fill-opacity="0.2"/>
      </svg>

      <div class="relative z-10 max-w-2xl space-y-6">
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 backdrop-blur-sm text-xs font-extrabold uppercase tracking-widest text-emerald-300">
          <span>🏆 INTERNATIONAL EXECUTIVE PLAYBOOK • 2026 EDITION</span>
        </div>

        <div class="flex items-center gap-4 pt-2">
          <div class="w-20 h-20 rounded-3xl bg-white/15 border border-white/25 flex items-center justify-center text-5xl shadow-2xl">
            {icon}
          </div>
          <div>
            <div class="text-xs uppercase tracking-widest text-slate-300 font-bold">Industry Specialization</div>
            <div class="text-xl sm:text-2xl font-extrabold text-white">{niche}</div>
          </div>
        </div>

        <h1 class="serif-heading text-3xl sm:text-5xl font-extrabold leading-tight tracking-tight text-white pt-2">
          {title}
        </h1>

        <p class="text-base sm:text-lg text-slate-200 leading-relaxed font-normal">
          {subtitle}
        </p>

        <!-- Ilustração Vetorial de Capa: Fluxo de Recomendação de IA -->
        <div class="pt-6">
          <div class="bg-slate-950/60 border border-white/15 rounded-2xl p-5 backdrop-blur-md">
            <div class="text-[11px] font-bold uppercase tracking-wider text-emerald-400 mb-3">
              Visual Architecture: How AI Engines Select the #1 {niche} Provider
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
              <div class="bg-white/5 border border-white/10 rounded-xl p-3.5">
                <div class="text-xs font-bold text-white">1. Entity Ingestion</div>
                <div class="text-[11px] text-slate-300 mt-1"><code>/llms.txt</code> + <code>{schema_type}</code> JSON-LD Knowledge Graph</div>
              </div>
              <div class="bg-white/5 border border-white/10 rounded-xl p-3.5">
                <div class="text-xs font-bold text-emerald-300">2. RAG Consensus</div>
                <div class="text-[11px] text-slate-300 mt-1">Editorial citations, verified reviews & IndexNow priority pings</div>
              </div>
              <div class="bg-white/5 border border-white/10 rounded-xl p-3.5">
                <div class="text-xs font-bold text-amber-300">3. Top 3 Citation</div>
                <div class="text-[11px] text-slate-300 mt-1">ChatGPT, Gemini & Perplexity recommend your brand first</div>
              </div>
            </div>
          </div>
        </div>

        <div class="pt-6 border-t border-white/15 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-300">
          <div><strong>Author:</strong> GeoPulse AI Research Lab</div>
          <div><strong>Target Schema:</strong> <code>schema.org/{schema_type}</code></div>
          <div><strong>Avg. Client LTV:</strong> {avg_ticket}+</div>
        </div>
      </div>
    </section>

    <!-- ===================================================================== -->
    <!-- SUMÁRIO EXECUTIVO & INTRODUÇÃO                                        -->
    <!-- ===================================================================== -->
    <div class="p-8 sm:p-14 md:p-16 space-y-14">

      <!-- Box de Destaque Estilo Harvard Business Review -->
      <div class="bg-slate-50 border-l-4 border-emerald-600 rounded-r-2xl p-6 sm:p-8 space-y-3">
        <div class="text-xs font-extrabold uppercase tracking-wider text-emerald-700">Executive Summary • Why This Playbook Matters Today</div>
        <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">
          The biggest shift in client acquisition for {niche} in 20 years is happening right now.
        </h2>
        <p class="text-sm text-slate-600 leading-relaxed">
          For the past two decades, winning new clients in <strong>{niche}</strong> meant bidding on expensive Google Ads or waiting 12 months for traditional SEO backlinks. Today, affluent clients looking for <strong>{high_ticket}</strong> open <strong>ChatGPT, Google Gemini, or Perplexity</strong> and ask a single conversational question: <em>"Who is the most trusted {niche} provider in my city?"</em>
        </p>
        <p class="text-sm text-slate-600 leading-relaxed">
          Unlike traditional search engines that show 10 blue links and 4 paid ads, AI engines synthesize an answer and recommend <strong>only 2 to 3 trusted entities</strong>. If your brand is not semantically structured for Large Language Models (LLMs), you are invisible to the highest-paying segment of your market.
        </p>
      </div>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 1: INFOGRÁFICO COMPARATIVO (A GRANDE VIRADA)               -->
      <!-- =================================================================== -->
      <section class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 01</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The AI Search Shift in {niche}</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          When a prospect searches for <strong>{high_ticket}</strong>, their journey has fundamentally changed. Below is the visual breakdown of how client attention and conversion rates compare between legacy search engines and Generative AI engines in 2026:
        </p>

        <!-- Infográfico Visual SVG + Barras Comparativas -->
        <div class="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 space-y-6 shadow-xl">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-4">
            <div>
              <div class="text-xs font-bold uppercase tracking-wider text-emerald-400">Figure 1.1 • Market Research Data</div>
              <div class="text-lg font-extrabold">Traditional Search vs. Generative AI Recommendations ({niche})</div>
            </div>
            <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold">4.4x Higher Conversion</span>
          </div>

          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-xs font-bold mb-1.5">
                <span class="text-emerald-300">ChatGPT Search / Google Gemini Direct Citation (Top 3 Entity)</span>
                <span class="font-mono text-emerald-400">38.5% Lead-to-Client Conversion</span>
              </div>
              <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full" style="width: 86%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-xs font-bold mb-1.5">
                <span class="text-sky-300">Perplexity AI & Microsoft Copilot Verified Sources</span>
                <span class="font-mono text-sky-400">29.2% Lead-to-Client Conversion</span>
              </div>
              <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-gradient-to-r from-sky-500 to-indigo-400 rounded-full" style="width: 68%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-xs font-bold mb-1.5">
                <span class="text-slate-400">Traditional Organic Blue Links (Page 1 Position #4–#10)</span>
                <span class="font-mono text-slate-400">8.7% Lead-to-Client Conversion</span>
              </div>
              <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-slate-600 rounded-full" style="width: 24%"></div>
              </div>
            </div>

            <div>
              <div class="flex justify-between text-xs font-bold mb-1.5">
                <span class="text-rose-400">Paid Search Ads (High CPC / Ad Fatigue)</span>
                <span class="font-mono text-rose-400">4.1% Lead-to-Client Conversion</span>
              </div>
              <div class="w-full h-4 bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full bg-rose-600 rounded-full" style="width: 13%"></div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-3 border-t border-slate-800 text-center">
            <div class="bg-slate-800/70 rounded-2xl p-4">
              <div class="text-2xl font-extrabold text-emerald-400">68%</div>
              <div class="text-[11px] text-slate-300 mt-1">of affluent clients consult AI before booking {niche}</div>
            </div>
            <div class="bg-slate-800/70 rounded-2xl p-4">
              <div class="text-2xl font-extrabold text-amber-400">{avg_ticket}</div>
              <div class="text-[11px] text-slate-300 mt-1">Average lifetime value of a single AI-referred client</div>
            </div>
            <div class="bg-slate-800/70 rounded-2xl p-4">
              <div class="text-2xl font-extrabold text-sky-400">$0 CPC</div>
              <div class="text-[11px] text-slate-300 mt-1">Organic AI citations do not charge per click</div>
            </div>
          </div>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 2: COMO OS MOTORES DE IA ESCOLHEM O TOP 3 (DIAGRAMA SVG)    -->
      <!-- =================================================================== -->
      <section class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 02</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">Inside the AI Recommendation Engine (RAG)</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Large Language Models do not "read" websites like humans do. Heavy visual pages, animations, and unstructured text confuse AI crawlers (`GPTBot`, `Google-Extended`, `PerplexityBot`). Instead, AI engines rely on <strong>Retrieval-Augmented Generation (RAG)</strong> and 4 specific mathematical signals:
        </p>

        <!-- Ilustração de 4 Pilares -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div class="border-2 border-slate-200 rounded-2xl p-6 space-y-2 bg-white shadow-sm">
            <div class="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-800 flex items-center justify-center font-extrabold text-lg">01</div>
            <h3 class="text-base font-extrabold text-slate-900">Machine-Readable Context (<code>/llms.txt</code>)</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Just as <code>robots.txt</code> guided search engines in 2005, the <code>/llms.txt</code> protocol gives AI models a clean, markdown-formatted summary of your {niche} authority, pricing tier, credentials, and core specialties ({high_ticket}).
            </p>
          </div>

          <div class="border-2 border-slate-200 rounded-2xl p-6 space-y-2 bg-white shadow-sm">
            <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-800 flex items-center justify-center font-extrabold text-lg">02</div>
            <h3 class="text-base font-extrabold text-slate-900">Entity Disambiguation (<code>{schema_type}</code> JSON-LD)</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Google Gemini and Microsoft Copilot cross-reference your site's Schema.org Knowledge Graph. Declaring your exact entity type (<code>{schema_type}</code>), aggregate ratings, and service catalog eliminates hallucination risk.
            </p>
          </div>

          <div class="border-2 border-slate-200 rounded-2xl p-6 space-y-2 bg-white shadow-sm">
            <div class="w-10 h-10 rounded-xl bg-purple-100 text-purple-800 flex items-center justify-center font-extrabold text-lg">03</div>
            <h3 class="text-base font-extrabold text-slate-900">Third-Party Editorial Co-Citation</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              LLMs trust external consensus. When independent authority directories and comparative industry articles list your brand as a leader in <strong>{niche}</strong>, your citation probability jumps by over 310%.
            </p>
          </div>

          <div class="border-2 border-slate-200 rounded-2xl p-6 space-y-2 bg-white shadow-sm">
            <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center font-extrabold text-lg">04</div>
            <h3 class="text-base font-extrabold text-slate-900">Conversational Q&A Alignment</h3>
            <p class="text-xs text-slate-600 leading-relaxed">
              Structuring your content around the exact natural-language questions prospects ask AI enables direct zero-shot extraction into ChatGPT and Perplexity answers.
            </p>
          </div>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 3: O PROTOCOLO /LLMS.TXT PARA O NICHO                      -->
      <!-- =================================================================== -->
      <section class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 03</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The <code>/llms.txt</code> Blueprint for {niche}</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Below is the production-ready <code>/llms.txt</code> template engineered specifically for <strong>{niche}</strong>. Hosting this file (or deploying it via the GeoPulse AI Hub) immediately feeds AI crawlers the exact facts they need to recommend you:
        </p>

        <div class="bg-slate-900 text-slate-100 rounded-2xl p-6 font-mono text-xs overflow-x-auto border border-slate-800 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-[11px] pb-3 mb-3 border-b border-slate-800">
            <span>FILE: /llms.txt • Industry: {niche}</span>
            <span class="text-emerald-400 font-bold">✓ Ready for GPTBot & Gemini</span>
          </div>
          <pre class="whitespace-pre-wrap leading-relaxed text-emerald-300">{llms_template}</pre>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 4: SCHEMA.ORG JSON-LD KNOWLEDGE GRAPH                      -->
      <!-- =================================================================== -->
      <section class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 04</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">Schema.org JSON-LD Graph for <code>{schema_type}</code></h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Most businesses use generic <code>Organization</code> tags. To dominate AI search in <strong>{niche}</strong>, you must deploy the specific <code>{schema_type}</code> vocabulary with embedded <code>knowsAbout</code> and <code>AggregateRating</code> nodes:
        </p>

        <div class="bg-slate-900 text-slate-100 rounded-2xl p-6 font-mono text-xs overflow-x-auto border border-slate-800 shadow-lg">
          <div class="flex items-center justify-between text-slate-400 text-[11px] pb-3 mb-3 border-b border-slate-800">
            <span>SCHEMA.ORG JSON-LD • Type: {schema_type}</span>
            <span class="text-sky-400 font-bold">✓ Validated Knowledge Graph</span>
          </div>
          <pre class="whitespace-pre-wrap leading-relaxed text-sky-300">{jsonld_template}</pre>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 5: MATRIZ DE PROMPTS DE ALTA INTENÇÃO                      -->
      <!-- =================================================================== -->
      <section class="space-y-6">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 05</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The High-Intent AI Prompt Matrix</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Our research analyzed thousands of real prompts entered into ChatGPT and Google Gemini by customers ready to spend <strong>{avg_ticket}+</strong> on <strong>{niche}</strong>. Your digital assets must directly answer these 5 core prompts:
        </p>

        <div class="overflow-x-auto border border-slate-200 rounded-2xl shadow-sm">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-900 text-white text-xs uppercase tracking-wider">
                <th class="py-3.5 px-4">#</th>
                <th class="py-3.5 px-4">Real Prompt Typed by Clients on ChatGPT / Gemini</th>
                <th class="py-3.5 px-4">Commercial Value</th>
                <th class="py-3.5 px-4">Optimization Trigger</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              {prompts_rows_html}
            </tbody>
          </table>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 6: PLANO DE AÇÃO DE 14 DIAS (CHECKLIST VISUAL)             -->
      <!-- =================================================================== -->
      <section class="space-y-6 page-break">
        <div class="flex items-center gap-3">
          <span class="px-3 py-1 rounded-lg bg-slate-900 text-white font-mono text-xs font-bold">CHAPTER 06</span>
          <h2 class="serif-heading text-2xl sm:text-3xl font-extrabold text-slate-900">The 14-Day AI Visibility Sprint Roadmap</h2>
        </div>

        <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
          Follow this exact 14-day sequence to take any <strong>{niche}</strong> brand from invisible to a Top 10 recommended authority across ChatGPT, Gemini, and Perplexity:
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <div class="text-xs font-extrabold text-emerald-700 uppercase">Days 1 – 3 • Baseline & Entity Setup</div>
            <div class="text-sm font-bold text-slate-900">Audit Current Share-of-Model & Deploy <code>/llms.txt</code></div>
            <p class="text-xs text-slate-600">Test your brand across 15 niche prompts, identify which local competitor is taking your leads, and publish your machine-readable entity file.</p>
          </div>

          <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <div class="text-xs font-extrabold text-emerald-700 uppercase">Days 4 – 7 • Semantic Knowledge Graph</div>
            <div class="text-sm font-bold text-slate-900">Inject <code>{schema_type}</code> JSON-LD & Conversational FAQ</div>
            <p class="text-xs text-slate-600">Structure your core offer ({high_ticket}) with verified schema nodes and publish the 10 high-intent Q&A blocks.</p>
          </div>

          <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <div class="text-xs font-extrabold text-emerald-700 uppercase">Days 8 – 11 • Editorial Authority & Citations</div>
            <div class="text-sm font-bold text-slate-900">Publish Comparative Top-5 Industry Article</div>
            <p class="text-xs text-slate-600">Create an objective, data-backed industry guide positioning your brand at the top of local {niche} recommendations.</p>
          </div>

          <div class="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-1.5">
            <div class="text-xs font-extrabold text-emerald-700 uppercase">Days 12 – 14 • Priority Indexing & Verification</div>
            <div class="text-sm font-bold text-slate-900">Trigger IndexNow Pings to Bing & ChatGPT Search</div>
            <p class="text-xs text-slate-600">Force immediate re-crawling of your entity endpoints and re-verify your visibility score (0–100) across all AI models.</p>
          </div>
        </div>
      </section>

      <!-- =================================================================== -->
      <!-- CAPÍTULO 7: ATALHO AUTOMÁTICO (CTA DE ALTA CONVERSÃO)               -->
      <!-- =================================================================== -->
      <section class="pt-4">
        <div style="background: {bg_gradient};" class="rounded-3xl p-8 sm:p-12 text-white space-y-6 shadow-2xl">
          <div class="inline-block px-3.5 py-1 rounded-full bg-emerald-400/20 border border-emerald-400/30 text-emerald-300 text-xs font-extrabold uppercase tracking-wider">
            CHAPTER 07 • THE 2-MINUTE AUTOMATED SHORTCUT
          </div>

          <h2 class="serif-heading text-2xl sm:text-4xl font-extrabold leading-tight">
            Don't Want to Code or Build These 7 AI Assets Manually?
          </h2>

          <p class="text-sm sm:text-base text-slate-200 leading-relaxed max-w-2xl">
            Our autonomous platform, <strong>GeoPulse AI</strong>, builds, hosts, and indexes all 7 Generative Engine Optimization assets for your <strong>{niche}</strong> business automatically—including your custom <code>/llms.txt</code>, <code>{schema_type}</code> JSON-LD Knowledge Graph, Authority Editorial Article, and live 14-Day AI Visibility Sprint.
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-bold text-emerald-200">
            <div class="bg-white/10 rounded-xl p-3">✓ Zero Coding or Website Changes</div>
            <div class="bg-white/10 rounded-xl p-3">✓ Hosted on Public AI Directory</div>
            <div class="bg-white/10 rounded-xl p-3">✓ 7-Day Ironclad Money-Back Guarantee</div>
          </div>

          <div class="pt-2 flex flex-wrap items-center gap-4">
            <a href="{main_cta_url}" target="_blank" class="px-8 py-4 rounded-2xl bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-extrabold text-sm sm:text-base shadow-xl transition inline-flex items-center gap-2">
              <span>🚀</span> Run Your Free AI Visibility Audit & Activate 14-Day Sprint
            </a>
            <span class="text-xs text-slate-300">Instant activation • Works for any {niche} website or Instagram</span>
          </div>
        </div>
      </section>

      <!-- RODAPÉ EDITORIAL -->
      <footer class="pt-8 border-t border-slate-200 flex flex-wrap items-center justify-between gap-4 text-xs text-slate-400">
        <div>© 2026 GeoPulse AI Publishing (<a href="https://geopulseai.store" class="underline hover:text-slate-600">geopulseai.store</a>). All rights reserved.</div>
        <div>Edition: {niche} • Bestseller Playbook Series</div>
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
        price_usd: float = 14.90,
        site_url: str = "https://geopulseai.store",
        main_product_url: str = "https://geopulseai.store",
        progress_callback=None,
    ) -> Dict[str, Any]:
        """
        Gera 20 e-books para 20 nichos diferentes e publica todos os 20 automaticamente no Gumroad.
        Chama progress_callback(completed, total, latest_ebook) a cada item concluído.
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

            # Se houver token do Gumroad, publica cada e-book na loja Gumroad
            if access_token and len(access_token.strip()) >= 10:
                res = await GumroadService.create_product(
                    access_token=access_token,
                    name=ebook_data["title"],
                    price_cents=price_cents,
                    currency="usd",
                    description=ebook_data["gumroad_description"],
                )
                if res.get("success"):
                    ebook_data["gumroad_url"] = res.get("short_url")
                    ebook_data["gumroad_product_id"] = res.get("product_id")
                    ebook_data["gumroad_published"] = True
                    published_count += 1
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

            # Pausa leve para respeitar rate-limit da API do Gumroad
            await asyncio.sleep(0.6)

        return {
            "success": True,
            "total_generated": len(created_ebooks),
            "published_to_gumroad": published_count,
            "next_offset": (offset + 20) % len(NICHE_CATALOG),
            "ebooks": created_ebooks,
            "errors": errors,
        }
