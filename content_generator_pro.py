from datetime import datetime
import random
import re

from self_optimization import SelfOptimizationEngine

TOPICS = [
    "الاستثمار في مصر",
    "الربح من الانترنت",
    "مشاريع صغيرة للشباب",
    "العملات الرقمية",
    "تداول الأسهم",
    "التسويق بالعمولة"
]

TEMPLATES = [
    "دليل شامل: كيف تبدأ في {topic} وتحقق دخل ثابت في {year}",
    "أفضل 10 نصائح للنجاح في {topic} في الوطن العربي",
    "كل ما تحتاج معرفته عن {topic} للمبتدئين",
    "{topic}: فرص وتحديات في {year}",
    "خطوة بخطوة لبناء مستقبل مالي عبر {topic}"
]

def suggest_keywords(topic, add=None):
    base = ["استثمار", "مال", "ريادة أعمال", "دخل إضافي"]
    topic_words = topic.split()
    if add:
        base += list(add)
    return list(set(base + topic_words))

# قوائم الحظر حسب سياسات جوجل أدسنس (مصنفة وموسعة)
PROHIBITED_KEYWORDS = {
    "adult": [
        "إباحية", "علاقات غير شرعية", "مواقع تعارف مشبوهة", "صور غير لائقة"
    ],
    "violence": [
        "عنف", "إرهاب", "تهديد", "اعتداء", "إيذاء"
    ],
    "drugs": [
        "مخدرات", "تعاطي", "اتجار غير قانوني"
    ],
    "weapons": [
        "سلاح", "أسلحة نارية", "متفجرات"
    ],
    "hate": [
        "كراهية", "تمييز", "عنصرية"
    ],
    "illegal": [
        "اختراق", "قرصنة", "انتحال", "قمار", "رهان", "تزييف", "تزوير"
    ]
}

def is_topic_allowed(text: str) -> bool:
    """التحقق من خلو الموضوع من الكلمات المحظورة"""
    t = (text or '').strip()
    for category in PROHIBITED_KEYWORDS.values():
        for bad in category:
            if bad in t:
                return False
    return True

def enforce_arabic(text: str) -> str:
    """التأكد من أن النص عربي وإزالة بقايا ترجمات آلية سيئة"""
    # إزالة أسطر إنجليزية قصيرة شائعة
    text = re.sub(r"\b(?:the|and|for|with|from|by|to|of)\b", "", text, flags=re.IGNORECASE)
    return text

def render_article(title, topic, year, keywords):
    # حماية: منع توليد مقالات لمواضيع محظورة
    if not is_topic_allowed(topic):
        raise ValueError("🚫 الموضوع يحتوي على كلمات محظورة وفق سياسات النشر")
    title = enforce_arabic(title)
    topic = enforce_arabic(topic)
    canonical_slug = re.sub(r"\s+", "_", topic[:40])
    canonical_slug = re.sub(r"[^\w\u0600-\u06FF_]+", "", canonical_slug)
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>{title} | دليل المال العربي</title>
  <meta name="description" content="مقال شامل عن {topic} وتوصيات عملية لسنة {year}.">
  <meta name="keywords" content="{', '.join(keywords)}">
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="تفاصيل عملية حول {topic}."/>
  <meta property="og:image" content="https://zezooo342.github.io/myogimage.jpg"/>
  <link rel="canonical" href="https://zezooo342.github.io/{canonical_slug}.html"/>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "تفاصيل مجربة ومقارنة حول {topic} في {year}.",
    "image": "https://zezooo342.github.io/myogimage.jpg",
    "datePublished": "{datetime.today().strftime('%Y-%m-%d')}",
    "author": {{"@type": "Person","name":"فريق دليل المال العربي"}}
  }}
  </script>
  <style>
    body{{font-family:'Tajawal',Arial,sans-serif;background:#f6fcfa;}}
    .main{{background:#fff;max-width:700px;margin:2em auto;padding:2em 1.4em;border-radius:14px;box-shadow:0 2px 8px #e1eee9;}}
    h1{{color:#0c7954;}}
    img{{max-width:100%;height:auto;}}
  </style>
</head>
<body>
  <div class="main">
    <h1>{title}</h1>
    <p>مقال تحليلي حول {topic} لعام {year}: نصائح وخطوات بنجاح حقيقي في الوطن العربي.</p>
    <p class="meta">بواسطة <strong>فريق دليل المال العربي</strong> • <time datetime="{datetime.today().strftime('%Y-%m-%d')}">{datetime.today().strftime('%Y-%m-%d')}</time></p>
    <h2>نقاط رئيسية:</h2>
    <ul>
      <li>كيف تبدأ فعليًا في {topic}؟</li>
      <li>أخطاء شائعة وتجارب عملية حقيقية.</li>
      <li>أبرز نصائح مدعومة بتوصيات خبراء عرب.</li>
    </ul>
    <h2>مقالات ذات صلة</h2>
    <ul>
      <li><a href="index.html">الرئيسية</a></li>
      <li><a href="about.html">من نحن</a></li>
      <li><a href="privacy.html">سياسة الخصوصية</a></li>
    </ul>
    <h2>المراجع</h2>
    <ul>
      <li><a href="https://www.investopedia.com/" rel="noopener noreferrer nofollow" target="_blank">Investopedia</a></li>
      <li><a href="https://www.imf.org/" rel="noopener noreferrer nofollow" target="_blank">IMF</a></li>
    </ul>
  </div>
</body>
</html>
"""
    return html

def generate_articles(n=3, year="2025", improvement_dict=None):
    for i in range(n):
        topic = random.choice(TOPICS)
        # استخدم اقتراح الكلمات المفتاحية والتحسين الذاتي لو توفر
        add_keywords = improvement_dict.get('focus_keywords', []) if improvement_dict else []
        title = random.choice(TEMPLATES).format(topic=topic, year=year)
        keywords = suggest_keywords(topic, add=add_keywords)
        html = render_article(title, topic, year, keywords)
        file_name = re.sub(r"\s+", "_", topic[:40])
        file_name = re.sub(r"[^\w\u0600-\u06FF_]+", "", file_name) + ".html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"تم إنشاء المقال: {file_name} - {title}")

if __name__ == "__main__":
    # ربط سكربت التحسين الذاتي
    optimizer = SelfOptimizationEngine()
    traffic = {'top_content_type': 'دليل عملي', 'top_keywords': ['سيو', 'ربح المال']}
    social = {'best_time': '9:00pm', 'engagement_rate': 0.11}
    conversion = {'avg_rate': 0.018}
    revenue = {'rpm': 2.4}
    improvements = optimizer.analyze_and_improve(traffic, social, conversion, revenue)
    # توليد مقالات مقترحة طبقًا للتطوير
    generate_articles(n=3, year="2025", improvement_dict=improvements)
