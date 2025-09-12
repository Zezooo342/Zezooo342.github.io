from datetime import datetime
import random

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

def render_article(title, topic, year, keywords):
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
  <link rel="canonical" href="https://zezooo342.github.io/{topic[:15].replace(' ','_')}.html"/>
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
  </style>
</head>
<body>
  <div class="main">
    <h1>{title}</h1>
    <p>مقال تحليلي حول {topic} لعام {year}: نصائح وخطوات بنجاح حقيقي في الوطن العربي.</p>
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
        file_name = topic[:15].replace(' ', '_') + ".html"
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
