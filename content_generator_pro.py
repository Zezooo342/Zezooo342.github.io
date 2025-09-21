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
    
    # إنشاء slug آمن ومفهوم للـ URL
    canonical_slug = re.sub(r'[^\w\u0600-\u06FF\s]', '', topic)
    canonical_slug = re.sub(r'\s+', '_', canonical_slug.strip())[:50]
    if not canonical_slug:
        canonical_slug = "article_" + str(hash(topic))[:8]
    
    # محتوى أكثر تنوعاً وجودة
    content_sections = [
        f"فهم أساسيات {topic} بطريقة عملية ومبسطة للمبتدئين والمحترفين.",
        f"الاستراتيجيات المجربة والفعالة في مجال {topic} مع أمثلة حقيقية من السوق العربي.",
        f"التحديات الشائعة في {topic} وكيفية التغلب عليها بطرق مبتكرة.",
        f"نصائح متقدمة من خبراء {topic} لتحقيق أفضل النتائج الممكنة."
    ]
    
    faq_questions = [
        f"ما هي أفضل طريقة للبدء في {topic}؟",
        f"كم التكلفة المتوقعة للاستثمار في {topic}؟",
        f"ما هي المخاطر الرئيسية في {topic} وكيف نتجنبها؟",
        f"كيف يمكن قياس النجاح في {topic}؟"
    ]
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title} | دليل المال العربي</title>
  <meta name="description" content="دليل شامل ومفصل عن {topic} مع نصائح عملية وتوصيات الخبراء لعام {year}.">
  <meta name="keywords" content="{', '.join(keywords)}">
  <link rel="canonical" href="https://zezooo342.github.io/{canonical_slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="دليل شامل ومفصل عن {topic} مع نصائح عملية وتوصيات الخبراء.">
  <meta property="og:image" content="https://zezooo342.github.io/assets/images/og-default.png">
  <meta property="og:type" content="article">
  <link rel="preload" href="assets/css/common.min.css" as="style" onload="this.rel='stylesheet'">
  <noscript><link rel="stylesheet" href="assets/css/common.min.css"></noscript>
  <link rel="stylesheet" href="assets/css/nav.min.css">
  <meta name="theme-color" content="#0c7954">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "دليل شامل ومفصل عن {topic} مع نصائح عملية وتوصيات الخبراء لعام {year}.",
    "author": {{
      "@type": "Organization",
      "name": "فريق دليل المال العربي"
    }},
    "datePublished": "{datetime.today().strftime('%Y-%m-%d')}",
    "dateModified": "{datetime.today().strftime('%Y-%m-%d')}",
    "publisher": {{
      "@type": "Organization",
      "name": "دليل المال العربي",
      "url": "https://zezooo342.github.io",
      "logo": "https://zezooo342.github.io/assets/images/og-default.png"
    }},
    "mainEntityOfPage": "https://zezooo342.github.io/{canonical_slug}.html",
    "image": "https://zezooo342.github.io/assets/images/og-default.png",
    "inLanguage": "ar"
  }}
  </script>
</head>
<body>
<header class="site-header">
  <nav class="site-nav">
    <a href="/index.html" class="logo">دليل المال العربي</a>
    <a href="/articles.html">المقالات</a>
    <a href="/about.html">عن الموقع</a>
    <a href="/contact.html">اتصل بنا</a>
  </nav>
</header>

<main class="main" data-ld-article>
  <h1>{title}</h1>
  <div class="article-meta" style="margin: 1em 0; padding: 1em; background: #f8f9fa; border-radius: 8px; font-size: 0.9em; color: #666;">
    <span><strong>المؤلف:</strong> فريق دليل المال العربي</span> | 
    <span><strong>تاريخ النشر:</strong> {datetime.today().strftime('%d %B %Y')}</span>
  </div>
  <p class="article-summary">دليل شامل ومفصل عن {topic} مع أحدث المعلومات والاستراتيجيات العملية لعام {year}. تعرف على أفضل الطرق والنصائح من الخبراء.</p>

  <h2>مقدمة شاملة عن {topic}</h2>
  <p>{content_sections[0]}</p>

  <h2>الاستراتيجيات والطرق العملية</h2>
  <p>{content_sections[1]}</p>

  <h2>التحديات وكيفية التغلب عليها</h2>
  <p>{content_sections[2]}</p>

  <h2>نصائح متقدمة من الخبراء</h2>
  <p>{content_sections[3]}</p>

  <h2>الأسئلة الشائعة</h2>
  <div class="faq-section">
"""
    
    for q in faq_questions:
        html += f"""    <h3>{q}</h3>
    <p>هذا سؤال مهم يحتاج إجابة مفصلة تأخذ في الاعتبار الظروف المحلية والإمكانيات المتاحة. ننصح بالتشاور مع الخبراء المختصين للحصول على استشارة مخصصة.</p>
"""
    
    html += f"""  </div>

  <h2>المصادر والمراجع</h2>
  <ul class="sources-list">
    <li><a href="https://www.investopedia.com" target="_blank" rel="nofollow noopener">Investopedia</a></li>
    <li><a href="https://www.entrepreneur.com" target="_blank" rel="nofollow noopener">Entrepreneur</a></li>
    <li><a href="https://www.forbes.com/business" target="_blank" rel="nofollow noopener">Forbes Business</a></li>
  </ul>

  <h2>مقالات ذات صلة</h2>
  <ul class="related-links">
    <li><a href="index.html">الصفحة الرئيسية</a></li>
    <li><a href="articles.html">جميع المقالات</a></li>
    <li><a href="about.html">من نحن</a></li>
    <li><a href="privacy.html">سياسة الخصوصية</a></li>
  </ul>
</main>

<footer>
  <div style="background: #0c7954; color: #fff; padding: 2em 1em; text-align: center;">
    <div style="max-width: 1200px; margin: 0 auto;">
      <div style="margin-bottom: 1em;">
        <a href="privacy.html" style="color: #a8d5c1; margin: 0 1em;">سياسة الخصوصية</a>
        <a href="terms.html" style="color: #a8d5c1; margin: 0 1em;">شروط الاستخدام</a>
        <a href="disclaimer.html" style="color: #a8d5c1; margin: 0 1em;">إخلاء المسؤولية</a>
        <a href="sitemap.xml" style="color: #a8d5c1; margin: 0 1em;">خريطة الموقع</a>
      </div>
      <div style="border-top: 1px solid #28654c; padding-top: 1em; font-size: 0.9em; color: #a8d5c1;">
        <p>جميع الحقوق محفوظة &copy; {year} دليل المال العربي | المحتوى لأغراض تعليمية وإعلامية فقط</p>
        <p style="margin-top: 0.5em;">يحتوي هذا الموقع على روابط تابعة. قد نحصل على عمولة من عمليات الشراء المؤهلة.</p>
      </div>
    </div>
  </div>
</footer>

<script src="/assets/js/site-nav.min.js" defer></script>
<script src="/assets/js/cookie-consent.js" defer></script>
</body>
</html>"""
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
