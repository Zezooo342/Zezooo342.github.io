import random
from datetime import datetime

# قائمة بأقوى مجالات المال والاستثمار للويب العربي
TOPICS = [
    "الاستثمار في مصر",
    "الربح من الانترنت",
    "مشاريع صغيرة للشباب",
    "العملات الرقمية",
    "تداول الأسهم",
    "التسويق بالعمولة",
    "استثمار الذهب",
    "فرص مالية للسعوديين"
]

ARTICLE_TEMPLATES = [
    "دليل شامل: كيف تبدأ في {topic} وتحقق دخل ثابت في {year}",
    "أفضل 10 نصائح للنجاح في {topic} في العالم العربي",
    "كل ما تحتاج معرفته عن {topic} للمبتدئين",
    "{topic}: فرص وتحديات في {year}",
    "خطوة بخطوة لبناء مستقبل مالي عبر {topic}"
]

KEYWORDS_BASE = [
    "استثمار", "ريادة أعمال", "المال", "دخل", "ربح", "مشاريع ناجحة", "أفكار مشاريع", "تحليل الأسواق", "نصائح مالية"
]

def suggest_keywords(topic):
    topic_words = topic.split()
    return list(set(KEYWORDS_BASE + topic_words))

def generate_outline(topic):
    return [
        f"ما هو {topic}؟",
        f"مميزات وعيوب {topic}",
        f"كيف تبدأ في {topic} اليوم؟",
        f"أخطاء شائعة في {topic} وكيف تتجنبها",
        f"تجارب واقعية وآراء الخبراء حول {topic}",
        "أسئلة شائعة وإجابات عملية",
        "خلاصة ونصائح أخيرة"
    ]

def generate_faq(topic):
    return [
        f"كيف أبدأ في {topic}؟",
        f"ما العائد المتوسط من {topic} سنوياً؟",
        f"هل يمكن البدء في {topic} برأس مال صغير؟",
        f"ما المخاطر الأساسية في {topic}؟"
    ]

def render_article(title, topic, year="2025"):
    outline = generate_outline(topic)
    keywords = suggest_keywords(topic)
    faq = generate_faq(topic)
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <title>{title} - دليل المال العربي</title>
  <meta name="description" content="كل ما تحتاجه عن {topic}، دليل عملي واستراتيجيات مضمونة لتحقيق الربح والدخل الإضافي.">
  <meta name="keywords" content="{', '.join(keywords)}">
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="طرق واستراتيجيات عملية لتحقيق دخل من {topic}."/>
  <meta property="og:image" content="https://zezooo342.github.io/myogimage.jpg"/>
  <meta property="og:type" content="article"/>
  <link rel="canonical" href="https://zezooo342.github.io/{topic[:15].replace(' ','_')}.html"/>
  <!-- Article Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "كل ما تحتاج معرفته عن {topic} للربح بأمان.",
    "image": "https://zezooo342.github.io/myogimage.jpg",
    "datePublished": "{datetime.today().strftime("%Y-%m-%d")}",
    "author": {{"@type": "Person", "name": "فريق دليل المال العربي"}}
  }}
  </script>
  <style>
    body {{ font-family: 'Tajawal', Arial, sans-serif; background: #f9f9f9; color: #222; margin: 1em; }}
    h1,h2,h3 {{color:#076e4d;}}
    .box {{background:#fff;padding:1.5em;max-width:740px;margin:2em auto;border-radius:10px;box-shadow:0 2px 6px #eee;}}
    ul {{margin-right:2em;}}
    .faq {{margin:2em 0;}}
    a {{color:#046e56;}}
  </style>
</head>
<body>
  <div class="box">
    <h1>{title}</h1>
    <p>هذا المقال يقدم الدليل العملي الكامل حول {topic} وأهم النصائح للمبتدئين والمحترفين في العالم العربي.</p>
"""
    for section in outline:
        html += f"<h2>{section}</h2>\n<p>... (اكتب فقرتك الأصلية هنا أو استخدم ذكائك وخبرتك لصياغة محتوى قيم).</p>\n"
    html += "<div class='faq'><h3>أسئلة شائعة:</h3><ul>\n"
    for q in faq:
        html += f"  <li>{q}</li>\n"
    html += "</ul></div>\n"
    html += """<h3>روابط داخلية:</h3>
<ul>
  <li><a href="index.html">الرئيسية</a></li>
  <li><a href="about.html">من نحن</a></li>
  <li><a href="privacy.html">سياسة الخصوصية</a></li>
</ul>
</div>
</body>
</html>
"""
    return html

def generate_articles(n=3, year="2025"):
    for i in range(n):
        topic = random.choice(TOPICS)
        title = random.choice(ARTICLE_TEMPLATES).format(topic=topic, year=year)
        html = render_article(title, topic, year)
        file_name = topic[:15].replace(' ', '_') + ".html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"تم إنشاء المقال: {file_name} - {title}")

if __name__ == "__main__":
    generate_articles(n=5)
