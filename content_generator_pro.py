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
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} | دليل المال العربي</title>
  <meta name="description" content="مقال شامل عن {topic} وتوصيات عملية لسنة {year}.">
  <meta name="keywords" content="{', '.join(keywords)}">
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="تفاصيل عملية حول {topic}."/>
  <meta property="og:image" content="https://zezooo342.github.io/assets/images/og-default.png"/>
  <meta property="og:type" content="article"/>
  <link rel="canonical" href="https://zezooo342.github.io/{topic[:15].replace(' ','_')}.html"/>
  <link rel="stylesheet" href="/assets/css/nav.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "تفاصيل مجربة ومقارنة حول {topic} في {year}.",
    "image": "https://zezooo342.github.io/assets/images/og-default.png",
    "datePublished": "{datetime.today().strftime('%Y-%m-%d')}",
    "author": {{"@type": "Person","name":"فريق دليل المال العربي"}}
  }}
  </script>
  <style>
    body{{font-family:'Cairo',Arial,sans-serif;background:#f7fcfa;margin:0;padding:0;color:#222;line-height:1.7;}}
    .container{{max-width:800px;margin:2rem auto;background:#fff;padding:2rem;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1);}}
    h1{{color:#082032;font-size:2rem;margin-bottom:1rem;}}
    h2{{color:#3bb273;font-size:1.5rem;margin-top:2rem;margin-bottom:1rem;}}
    p{{margin-bottom:1rem;text-align:justify;}}
    ul{{margin:1rem 0;padding-right:2rem;}}
    li{{margin-bottom:0.5rem;}}
    .related-links{{background:#f6f8fa;padding:1.5rem;border-radius:8px;margin-top:2rem;}}
    .related-links ul{{list-style:none;padding:0;}}
    .related-links li{{margin:0.8rem 0;}}
    .related-links a{{color:#3bb273;text-decoration:none;font-weight:500;}}
    .related-links a:hover{{text-decoration:underline;}}
  </style>
</head>
<body>
  <header id="site-header"></header>
  
  <div class="container">
    <h1>{title}</h1>
    <p>مقال تحليلي شامل حول {topic} لعام {year}: نصائح وخطوات عملية مجربة لتحقيق النجاح في الوطن العربي.</p>
    
    <h2>مقدمة حول {topic}</h2>
    <p>يعتبر {topic} من المجالات المهمة التي تحظى باهتمام متزايد في العالم العربي. هذا الدليل يقدم نظرة شاملة ومعمقة حول أفضل الممارسات والاستراتيجيات العملية.</p>
    
    <h2>نقاط رئيسية للنجاح:</h2>
    <ul>
      <li>كيف تبدأ فعلياً في مجال {topic}؟</li>
      <li>أخطاء شائعة يجب تجنبها وتجارب عملية حقيقية</li>
      <li>أبرز النصائح المدعومة بتوصيات خبراء عرب</li>
      <li>استراتيجيات التطوير والنمو المستدام</li>
    </ul>
    
    <h2>خطوات عملية للتطبيق</h2>
    <p>النجاح في {topic} يتطلب تخطيطاً محكماً وتنفيذاً دقيقاً. من خلال اتباع الخطوات المدروسة والاستفادة من التجارب الناجحة، يمكن تحقيق نتائج ملموسة ومستدامة.</p>
    
    <div class="related-links">
      <h3>مقالات ذات صلة:</h3>
      <ul>
        <li><a href="/index.html">الصفحة الرئيسية</a></li>
        <li><a href="/about.html">من نحن</a></li>
        <li><a href="/invest-arab.html">دليل الاستثمار العربي</a></li>
        <li><a href="/make-money-online.html">طرق الربح من الإنترنت</a></li>
        <li><a href="/privacy.html">سياسة الخصوصية</a></li>
      </ul>
    </div>
  </div>

  <footer id="site-footer"></footer>
  <script src="/assets/js/site-nav.min.js" defer></script>
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
        file_name = "".join(c for c in topic[:15] if c.isalnum() or c in (' ', '_')).replace(' ', '_') + ".html"
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
