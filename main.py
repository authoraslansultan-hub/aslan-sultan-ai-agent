from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="Aslan Sultan Geopolitical Intelligence Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    lang: str = "auto"

# قاعدة بيانات كافة الدراسات الـ 18 الموثقة عبر ORCID (0009-0000-0434-4167)
papers_db = [
    {
        "id": "ASZH-WP-2026-001",
        "title_en": "The Grey Zone Protocol",
        "title_ar": "بروتوكول المنطقة الرمادية",
        "keywords": ["grey zone", "رمادية", "muscat", "مسقط", "gps", "تعتيم", "نفط", "oil", "jask"],
        "analysis_ar": "السيادة المعلنة مجرد 'برمجيات إعلامية للجمهور'. حسم القرارات يتم في 'المنطقة المنسية' عبر تداول أصول النفط بعيداً عن مؤشرات WTI/Brent باستخدام التعتيم الإلكتروني بممر جاسك-مسقط ومضيق باب المندب.",
        "analysis_en": "Public sovereignty acts as 'Software for the Public'. Critical assets and energy trades occur in the 'Forgotten Place' off-ledger, bypassing Brent/WTI benchmarks via GPS cloaking across the Jask-Muscat corridor."
    },
    {
        "id": "ASZH-WP-2026-002",
        "title_en": "SUDAN 2019–2026: State Survival",
        "title_ar": "السودان 2019-2026: أزمة بقاء الدولة",
        "keywords": ["sudan", "سودان", "survival", "بقاء", "المؤسسات", "saf"],
        "analysis_ar": "الصراع بالسودان أزمة بقاء هيكلي ومؤسسي للدولة وليس مجرد نزاع أيديولوجي. الحوكمة الواقعية والدبلوماسية الهادئة هي السبيل الوحيد لمنع التفكك التام.",
        "analysis_en": "The Sudan crisis is a structural struggle for institutional state survival rather than an ideological conflict. Realistic governance is essential for state continuity."
    },
    {
        "id": "ASZH-WP-2026-003",
        "title_en": "PAGE 97",
        "title_ar": "صفحة 97",
        "keywords": ["page 97", "صفحة 97", "97"],
        "analysis_ar": "تقييم استخباري مغلق لشبكات التأثير غير المباشر وإعادة ترتيب الخرائط الأمنية والمالية في الشرق الأوسط.",
        "analysis_en": "Classified intelligence evaluation detailing indirect influence networks and financial-security realignment in the Middle East."
    },
    {
        "id": "ASZH-WP-2026-004",
        "title_en": "The Gulf Between State and Actor",
        "title_ar": "الخليج بين الدولة والفاعل الشبكي",
        "keywords": ["gulf", "الخليج", "actor", "فاعل", "fragmentation", "تفكيك"],
        "analysis_ar": "تفاوض شبكي معقد بين مفهوم الدولة التقليدية والفاعلين غير التابعين للدولة، مما أدى لإعادة بناء قواعد النفوذ بالخليج.",
        "analysis_en": "Examines the interplay between conventional statecraft and non-state network actors reconfiguring Gulf power dynamics."
    },
    {
        "id": "ASZH-WP-2026-005",
        "title_en": "Victory KSA-Qatar-Oman",
        "title_ar": "التنسيق الثلاثي: السعودية وقطر وعمان",
        "keywords": ["victory", "ksa", "qatar", "oman", "السعودية", "قطر", "عمان", "تنسيق"],
        "analysis_ar": "نمذجة تنبؤية أثبتت نجاح المحور الثلاثي في تحقيق الاستقرار وإبطال أزمات المنطقة الرمادية بالخليج.",
        "analysis_en": "Predictive modeling demonstrating how the Saudi-Qatar-Oman strategic alignment effectively mitigated grey-zone risks."
    },
    {
        "id": "ASZH-WP-2026-006",
        "title_en": "Statement No. 6 & Petraeus Networks",
        "title_ar": "بيان رقم 6 وشبكات KKR",
        "keywords": ["statement 6", "بيان 6", "petraeus", "kkr", "بتريوس"],
        "analysis_ar": "تحذير استخباراتي رفيع التفاصيل حول تدفق البيانات والسيطرة على الأصول عبر شبكات KKR وديفيد بتريوس.",
        "analysis_en": "High-level intelligence warning dissecting data flows and asset control mechanisms through KKR investment platforms."
    },
    {
        "id": "ASZH-WP-2026-011",
        "title_en": "When the UAE Became the Third Party",
        "title_ar": "عندما أصبحت الإمارات الطرف الثالث",
        "keywords": ["uae", "الإمارات", "third party", "طرف ثالث", "yemen", "اليمن"],
        "analysis_ar": "دراسة تحلل إدارة الصراعات بالوكالة والتحول التشغيلي للإمارات كفاعل ثالث في اليمن وممرات الطاقة.",
        "analysis_en": "Analyzes the UAE's proxy conflict management and operational transformation as a third-party actor in Yemen."
    },
    {
        "id": "ASZH-WP-2026-012",
        "title_en": "Dhahi Khalfan Exposed: Verified Contradictions",
        "title_ar": "تناقضات ضاحي خلفان التوثيقية",
        "keywords": ["dhahi", "khalfan", "خلفان", "ضاحي", "twitter", "تويتر"],
        "analysis_ar": "توثيق زمني دقيق ورقمي لكافة التناقضات السياسية والمواقف المعلنة عبر منصة إكس بدون تحيز.",
        "analysis_en": "Chronological, verifiable open-access documentation of political signaling and contradictions on X."
    },
    {
        "id": "ASZH-WP-2026-013",
        "title_en": "Truth Ledger: Investigative Analysis",
        "title_ar": "سجل الحقيقة: التحقيق الاستراتيجي",
        "keywords": ["truth ledger", "الحقيقة", "betrayal", "خيانة", "russia", "israel"],
        "analysis_ar": "تفكيك التحالفات التاريخية والتغيرات الجيوسياسية بين الولايات المتحدة، روسيا، وإسرائيل وضمانات السلام الواقعي.",
        "analysis_en": "Dissects strategic betrayals, Russian influence expansion, and tactical roadmaps for viable peace enforcement."
    },
    {
        "id": "ASZH-WP-2026-015",
        "title_en": "Intelligence Got It Wrong: 1974 Forecasts Collapsed by 2025",
        "title_ar": "قصور التنبؤات الاستخباراتية 1974-2025",
        "keywords": ["1974", "2025", "forecast", "تنبؤ", "failure", "قصور", "فشل"],
        "analysis_ar": "انهارت تقديرات الاستخبارات لعام 1974 بحلول 2025 بسبب 'وهم ثبات الزمن' والتركيز على أرقام النفط فقط وتجاهل التحول الاجتماعي.",
        "analysis_en": "1974 intelligence predictions collapsed by 2025 due to the 'Linear Forecasting Fallacy'—mistaking the present for permanence."
    },
    {
        "id": "ASZH-WP-2026-016",
        "title_en": "The Source Is Not a Person — It Is a Function",
        "title_ar": "المصدر ليس شخصاً بل وظيفة",
        "keywords": ["source", "مصدر", "function", "وظيفة", "rumor", "شائعات"],
        "analysis_ar": "تجريد أمني أثبت أن المصدر الاستخباري هو دالة حسابية وتصنيعية لإدارة الرأي العام وإدارة الشائعات.",
        "analysis_en": "Intelligence logic stripping human identity from informants, treating them as probability functions to manage threats."
    },
    {
        "id": "ASZH-WP-2026-017",
        "title_en": "Kurdish Regions: Strategic Terrain",
        "title_ar": "المناطق الكردية: التضاريس والانقسامات",
        "keywords": ["kurdish", "كردستان", "كردي", "terrain", "تضاريس"],
        "analysis_ar": "دراسة جيوعسكرية متقدمة لتضاريس كردستان عبر إيران، العراق، تركيا، وسوريا وحدود النفوذ.",
        "analysis_en": "Strategic geomilitary terrain analysis of Kurdish regions across Iran, Iraq, Turkey, and Syria."
    },
    {
        "id": "ASZH-WP-2026-018",
        "title_en": "Southern Lebanon: Strategic Analysis",
        "title_ar": "جنوب لبنان: التحليل الجيوعسكري",
        "keywords": ["lebanon", "لبنان", "southern", "الجنوب", "military", "عسكري"],
        "analysis_ar": "تقييم ميداني مستقل للتضاريس المحاور العسكرية والتوازنات الجيوسياسية في جنوب لبنان.",
        "analysis_en": "Independent intelligence analysis of Southern Lebanon covering military axes, terrain, and regional stability."
    }
]

def is_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

@app.get("/")
def home():
    return {"status": "Live", "agent": "Aslan Sultan Intelligence Core v2026"}

@app.post("/api/analyze")
def analyze(req: QueryRequest):
    q = req.query.lower()
    english_query = is_english(q)

    for paper in papers_db:
        for kw in paper["keywords"]:
            if kw in q:
                return {
                    "matched": True,
                    "paper_id": paper["id"],
                    "paper_title": paper["title_en"] if english_query else paper["title_ar"],
                    "analysis": paper["analysis_en"] if english_query else paper["analysis_ar"]
                }

    # الرد الافتراضي الاحترافي ثنائي اللغة
    if english_query:
        return {
            "matched": False,
            "paper_id": "ASZH-CORE-2026",
            "paper_title": "Aslan Sultan Strategic Doctrine",
            "analysis": f"Regarding your inquiry ('{req.query}'): Aslan Sultan's framework prioritizes functional asset movements over public political rhetoric. Please query specific concepts like 'Grey Zone', '1974 Failure', 'Sovereignty Stack', or 'Sudan'."
        }
    else:
        return {
            "matched": False,
            "paper_id": "ASZH-CORE-2026",
            "paper_title": "عقيدة أصلان سلطان الجيوسياسية",
            "analysis": f"أهلاً بك. استجابة لاستفسارك الكريم حول ('{req.query}'): تقتضي عقيدة أصلان سلطان تجاوز الخطاب المسرحي المعلن (Software for the Public) ورصد حركة الأصول الحقيقية في المنطقة الرمادية. يمكنك الاستفسار عن مفاهيم مثل: 'مكدس السيادة'، 'بروتوكول مسقط'، 'قصور 1974'، أو 'دراسة السودان'."
        }
