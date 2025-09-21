import requests
try:
    import feedparser as _feedparser  # type: ignore
except Exception:
    _feedparser = None  # type: ignore
    # Minimal fallback if feedparser is not installed
    import xml.etree.ElementTree as ET
    from types import SimpleNamespace
    import html
    import re

    class FeedparserFallback:  # fallback shim with a parse(url) API
        @staticmethod
        def parse(url: str):
            try:
                resp = requests.get(
                    url,
                    timeout=(5, 15),  # 5s connect, 15s read timeout
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                    }
                )
                # Parse XML with namespaces preserved
                text = resp.text
                root = ET.fromstring(text)
                entries = []

                # Helper to find elements regardless of namespace
                def findall_ns(root, tag):
                    results = []
                    for elem in root.iter():
                        if elem.tag.endswith(tag):
                            results.append(elem)
                    return results

                # RSS items
                for it in findall_ns(root, "item"):
                    title = (it.findtext(".//title") or "").strip()
                    summary = (it.findtext(".//description") or "").strip()
                    link = (it.findtext(".//link") or "").strip()
                    entries.append(
                        SimpleNamespace(
                            title=html.unescape(title),
                            summary=html.unescape(summary),
                            link=link,
                        )
                    )

                # Atom entries
                if not entries:
                    for it in findall_ns(root, "entry"):
                        title = (it.findtext(".//title") or "").strip()
                        link_el = None
                        # Find link element regardless of namespace
                        for child in it:
                            if child.tag.endswith("link"):
                                link_el = child
                                break
                        link = ""
                        if link_el is not None:
                            link = link_el.attrib.get("href") or (link_el.text or "")
                        summary = (it.findtext(".//summary") or it.findtext(".//content") or "").strip()
                        entries.append(
                            SimpleNamespace(
                                title=html.unescape(title),
                                summary=html.unescape(summary),
                                link=link,
                            )
                        )

                return SimpleNamespace(entries=entries)
            except Exception:
                return SimpleNamespace(entries=[])
import random
import re
try:
    # محاولة استيراد googletrans مع التعامل مع غيابه
    from googletrans import Translator  # type: ignore
except Exception:
    Translator = None  # سيتم التعامل مع ذلك في translate_text

# Constants and configuration
RSS_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch",
    "https://rss.cnn.com/rss/money_news_international.rss",
    "https://www.entrepreneur.com/latest.rss"
]

SEO_TITLES = [
    "دليل شامل: {} في عام {} - كل ما تحتاج معرفته",
    "أفضل طرق {} للمبتدئين في {}",
    "كيفية النجاح في {} خطوة بخطوة {}",
    "أسرار {} المربحة في {} - دليل عملي",
    "{}  في {}: فرص ذهبية للربح والاستثمار"
]

# قائمة افتراضية للكلمات المحظورة مع محاولة قراءة قيمة مخصصة من ملف config.py إن وجد
DEFAULT_BANNED_KEYWORDS = [
    "adult", "weapon", "drugs", "gambling", "violence", "hate", "sex", "porn"
]
try:
    import importlib
    _cfg = importlib.import_module("config")  # ملف اختياري
    BANNED_KEYWORDS = getattr(_cfg, "BANNED_KEYWORDS", DEFAULT_BANNED_KEYWORDS)
except Exception:
    BANNED_KEYWORDS = DEFAULT_BANNED_KEYWORDS

def get_topic_trends():
    """جلب الاتجاهات والمواضيع الرائجة من RSS feeds"""
    articles = []
    
    for url in RSS_FEEDS:
        try:
            parse_func = _feedparser.parse if '_feedparser' in globals() and _feedparser is not None else FeedparserFallback.parse
            d = parse_func(url)
            for entry in d.entries[:3]:
                text = entry.title + " " + getattr(entry, "summary", "")
                if len(text) <= 30:
                    continue
                # فلترة المواضيع الممنوعة وفق سياسة مبسطة
                if any(b in text.lower() for b in BANNED_KEYWORDS):
                    continue
                # ترجمة عربية مع fallback عبر دالة مساعدة
                ar_text = translate_text(text)
                # إزالة علامات HTML ومنع النسخ الحرفي
                ar_text = re.sub(r"<[^>]+>", " ", ar_text)
                ar_text = re.sub(r"\s+", " ", ar_text).strip()
                articles.append({
                    "title": entry.title,
                    "summary": ar_text[:400] + ("..." if len(ar_text) > 400 else ""),
                    "link": entry.link
                })
        except Exception as e:
            print(f"خطأ في جلب البيانات من {url}: {e}")
            continue
    
    return articles

def _contains_arabic(text: str) -> bool:
    """التحقق من وجود أحرف عربية لتفادي الترجمة غير اللازمة."""
    return bool(re.search(r"[\u0600-\u06FF]", text or ""))

def translate_text(text: str, dest: str = 'ar', src: str = 'auto') -> str:
    """
    ترجمة آمنة إلى العربية مع تحسينات جودة AdSense:
    - تعيد النص كما هو إذا كان عربيًا بالفعل أو فارغًا.
    - تتعامل مع غياب googletrans أو أخطاء الشبكة دون كسر التنفيذ.
    - تعطي ترجمات محتملة للعناوين الإنجليزية الشائعة.
    """
    if not text:
        return ""
    if _contains_arabic(text):
        return text
    
    # قاموس ترجمة للعناوين الشائعة (لجودة أفضل بدون اعتماد على APIs خارجية)
    common_translations = {
        "Why Most Founders Fail on Social Media": "لماذا يفشل معظم المؤسسين في وسائل التواصل الاجتماعي",
        "How to Fix It Fast": "كيفية إصلاحها بسرعة",
        "These Are the Top 10 Children's Franchises": "هذه أفضل 10 امتيازات تجارية للأطفال",
        "How Lavazza and the US Open Brewed the Perfect Marketing Campaign": "كيف صنعت لافازا والبطولة الأمريكية المفتوحة حملة تسويقية مثالية",
        "Top Business Trends": "أبرز اتجاهات الأعمال",
        "Investment Strategies": "استراتيجيات الاستثمار",
        "Make Money Online": "الربح من الإنترنت",
        "Financial Planning": "التخطيط المالي",
        "Startup Guide": "دليل الشركات الناشئة"
    }
    
    # البحث عن ترجمة في القاموس المحلي أولاً
    for en_phrase, ar_phrase in common_translations.items():
        if en_phrase.lower() in text.lower():
            text = text.replace(en_phrase, ar_phrase)
    
    # محاولة استخدام googletrans إذا كان متاحاً
    if Translator is not None:
        try:
            tr = Translator()
            res = tr.translate(text, dest=dest, src=src)
            return res.text or text
        except Exception:
            pass
    
    # إذا لم تنجح الترجمة، نطبق تطبيعاً بسيطاً للنص الإنجليزي
    # لجعله أكثر قابلية للقراءة في السياق العربي
    text = re.sub(r'\b(and|or|the|a|an|in|on|at|to|for|of|with|by)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def fetch_google_trends(topic):
    """جلب الكلمات المفتاحية المرتبطة بالموضوع"""
    # محاكاة جلب الكلمات المفتاحية - يمكن ربطها بـ Google Trends API لاحقاً
    base_keywords = ["استثمار", "ربح", "مال", "تجارة", "أعمال"]
    topic_keywords = topic.split()
    return base_keywords + topic_keywords[:3]
# توليد خطة/مخطط مقال كاملة محسنة لـ AdSense
def generate_article_plan(main_topic: str, year: str = "2025"):
    # ترجمة العنوان إلى العربية أولاً لجودة أفضل
    ar_topic = translate_text(main_topic)
    
    keywords = fetch_google_trends(ar_topic)
    headline = random.choice(SEO_TITLES).format(ar_topic, year)
    
    # محتوى أكثر تنوعاً وجودة لتجنب الـ duplicate content
    outline_templates = [
        [
            "مقدمة شاملة عن {}",
            "الفوائد والمميزات الرئيسية لـ {}",
            "التحديات والعقبات في {}",
            "دليل التطبيق العملي خطوة بخطوة",
            "نصائح الخبراء وأفضل الممارسات",
            "الخلاصة والتوصيات"
        ],
        [
            "ما تحتاج معرفته عن {}",
            "كيفية الاستفادة من {} بأقصى قدر",
            "الأخطاء الشائعة وكيفية تجنبها",
            "استراتيجيات متقدمة في {}",
            "قصص نجاح وتجارب عملية",
            "المستقبل والاتجاهات الجديدة"
        ]
    ]
    
    selected_outline = random.choice(outline_templates)
    outline = [section.format(ar_topic) for section in selected_outline]
    
    # أسئلة أكثر تنوعاً وإفادة
    question_sets = [
        [
            "ما هي أهم فوائد {}؟",
            "كيف أبدأ في {} كمبتدئ؟",
            "ما هي التكاليف المتوقعة لـ {}؟",
            "كم من الوقت أحتاج لإتقان {}؟"
        ],
        [
            "هل {} مناسب للمبتدئين؟",
            "ما هي المخاطر المحتملة في {}؟",
            "كيف أقيس نجاح {} بطريقة صحيحة؟",
            "أين أجد المصادر الموثوقة عن {}؟"
        ]
    ]
    
    questions = random.choice(question_sets)
    questions = [q.format(ar_topic) for q in questions]
    
    # مصادر ومراجع افتراضية لتعزيز المصداقية
    default_sources = [
        "https://www.investopedia.com",
        "https://www.entrepreneur.com", 
        "https://www.forbes.com/business",
        "https://www.bloomberg.com"
    ]
    
    article = {
        "headline": headline,
        "summary": f"دليل شامل ومفصل عن {ar_topic} مع أحدث المعلومات والاستراتيجيات العملية لعام {year}. تعرف على أفضل الطرق والنصائح من الخبراء.",
        "outline": outline,
        "seo_keywords": keywords,
        "internal_links": ["/index.html", "/about.html", "/articles.html"],
        "questions": questions,
        "sources": default_sources,
        "author": "فريق دليل المال العربي",
        "publish_date": "2024-12-19"
    }
    return article
# أجزاء توليد المقال الرئيسي محسنة لـ AdSense
def render_article_template(article):
    # إنشاء slug آمن ومفهوم للـ URL
    ar_title = article['headline']
    slug = re.sub(r'[^\w\u0600-\u06FF\s]', '', ar_title)  # إبقاء الأحرف العربية والإنجليزية فقط
    slug = re.sub(r'\s+', '_', slug.strip())[:50]  # تحويل المسافات إلى شرطات سفلية وتقليص الطول
    if not slug:  # fallback إذا كان العنوان لا يحتوي على أحرف صالحة
        slug = "article_" + str(hash(ar_title))[:8]
    
    canonical_url = f"https://zezooo342.github.io/{slug}.html"
    
    html = [
        "<!DOCTYPE html>",
        '<html lang="ar" dir="rtl">',
        '<head>',
        f'  <meta charset="utf-8">',
        f'  <meta name="viewport" content="width=device-width,initial-scale=1">',
        f'  <title>{article["headline"]} | دليل المال العربي</title>',
        f'  <meta name="description" content="{article["summary"]}">',
        f'  <meta name="keywords" content="{", ".join(article["seo_keywords"])}">',
        f'  <link rel="canonical" href="{canonical_url}">',
        f'  <meta property="og:title" content="{article["headline"]}">',
        f'  <meta property="og:description" content="{article["summary"]}">',
        f'  <meta property="og:image" content="https://zezooo342.github.io/assets/images/og-default.png">',
        f'  <meta property="og:type" content="article">',
        '  <link rel="preload" href="assets/css/common.min.css" as="style" onload="this.rel=\'stylesheet\'">',
        '  <noscript><link rel="stylesheet" href="assets/css/common.min.css"></noscript>',
        '  <link rel="stylesheet" href="assets/css/nav.min.css">',
        '  <meta name="theme-color" content="#0c7954">',
        '  <script type="application/ld+json">',
        '  {',
        '    "@context": "https://schema.org",',
        '    "@type": "Article",',
        f'    "headline": "{article["headline"]}",',
        f'    "description": "{article["summary"]}",',
        '    "author": {',
        '      "@type": "Organization",',
        f'      "name": "{article.get("author", "دليل المال العربي")}"',
        '    },',
        f'    "datePublished": "{article.get("publish_date", "2024-12-19")}",',
        f'    "dateModified": "{article.get("publish_date", "2024-12-19")}",',
        '    "publisher": {',
        '      "@type": "Organization",',
        '      "name": "دليل المال العربي",',
        '      "url": "https://zezooo342.github.io",',
        '      "logo": "https://zezooo342.github.io/assets/images/og-default.png"',
        '    },',
        f'    "mainEntityOfPage": "{canonical_url}",',
        '    "image": "https://zezooo342.github.io/assets/images/og-default.png",',
        '    "inLanguage": "ar"',
        '  }',
        '  </script>',
        '</head>',
        '<body>',
        '<header class="site-header">',
        '  <nav class="site-nav">',
        '    <a href="/index.html" class="logo">دليل المال العربي</a>',
        '    <a href="/articles.html">المقالات</a>',
        '    <a href="/about.html">عن الموقع</a>',
        '    <a href="/contact.html">اتصل بنا</a>',
        '  </nav>',
        '</header>',
        '',
        '<main class="main" data-ld-article>',
        f'  <h1>{article["headline"]}</h1>',
        '  <div class="article-meta">',
        f'    <span><strong>المؤلف:</strong> {article.get("author", "فريق دليل المال العربي")}</span>',
        f'    <span><strong>تاريخ النشر:</strong> {article.get("publish_date", "2024-12-19")}</span>',
        '  </div>',
        f'  <p class="article-summary">{article["summary"]}</p>',
    ]
    
    # محتوى أكثر تنوعاً لكل قسم
    content_variations = [
        "يُعتبر هذا الموضوع من الأمور المهمة التي تحتاج فهماً عميقاً وتطبيقاً عملياً مدروساً.",
        "من خلال الخبرة والممارسة، يمكن تحقيق نتائج إيجابية ملموسة في هذا المجال.",
        "الاستراتيجية الصحيحة والتخطيط المدروس هما مفتاح النجاح في هذا الاتجاه.",
        "التعلم المستمر ومتابعة أحدث التطورات ضروريان لتحقيق الأهداف المرجوة."
    ]
    
    for i, section in enumerate(article["outline"]):
        html.append(f"  <h2>{section}</h2>")
        content = random.choice(content_variations)
        html.append(f"  <p>{content} في هذا السياق، نركز على الجوانب العملية والقابلة للتطبيق مع مراعاة الخصوصية الثقافية والاقتصادية للمنطقة العربية.</p>")
    
    # قسم الأسئلة الشائعة
    html.append("  <h2>الأسئلة الشائعة</h2>")
    html.append("  <div class=\"faq-section\">")
    for q in article["questions"]:
        html.append(f"    <h3>{q}</h3>")
        html.append("    <p>هذا سؤال مهم يحتاج إجابة مفصلة تأخذ في الاعتبار الظروف المحلية والإمكانيات المتاحة. ننصح بالاستعانة بالخبراء المختصين للحصول على نصائح مخصصة.</p>")
    html.append("  </div>")
    
    # قسم المصادر والمراجع (مهم لـ AdSense)
    if "sources" in article and article["sources"]:
        html.append("  <h2>المصادر والمراجع</h2>")
        html.append("  <ul class=\"sources-list\">")
        for source in article["sources"]:
            html.append(f'    <li><a href="{source}" target="_blank" rel="nofollow noopener">{source}</a></li>')
        html.append("  </ul>")
    
    # روابط ذات صلة
    html.append("  <h2>مقالات ذات صلة</h2>")
    html.append("  <ul class=\"related-links\">")
    for link in article["internal_links"]:
        link_text = link.replace("/", "").replace(".html", "").replace("-", " ").title()
        if link_text == "Index": link_text = "الصفحة الرئيسية"
        elif link_text == "About": link_text = "من نحن"
        elif link_text == "Articles": link_text = "جميع المقالات"
        html.append(f'    <li><a href="{link}">{link_text}</a></li>')
    html.append("  </ul>")
    
    html.extend([
        '</main>',
        '',
        '<footer>',
        '  <div style="background: #0c7954; color: #fff; padding: 2em 1em; text-align: center;">',
        '    <div style="max-width: 1200px; margin: 0 auto;">',
        '      <div style="margin-bottom: 1em;">',
        '        <a href="privacy.html" style="color: #a8d5c1; margin: 0 1em;">سياسة الخصوصية</a>',
        '        <a href="terms.html" style="color: #a8d5c1; margin: 0 1em;">شروط الاستخدام</a>',
        '        <a href="disclaimer.html" style="color: #a8d5c1; margin: 0 1em;">إخلاء المسؤولية</a>',
        '        <a href="sitemap.xml" style="color: #a8d5c1; margin: 0 1em;">خريطة الموقع</a>',
        '      </div>',
        '      <div style="border-top: 1px solid #28654c; padding-top: 1em; font-size: 0.9em; color: #a8d5c1;">',
        '        <p>جميع الحقوق محفوظة &copy; 2024 دليل المال العربي | المحتوى لأغراض تعليمية وإعلامية فقط</p>',
        '        <p style="margin-top: 0.5em;">يحتوي هذا الموقع على روابط تابعة. قد نحصل على عمولة من عمليات الشراء المؤهلة.</p>',
        '      </div>',
        '    </div>',
        '  </div>',
        '</footer>',
        '',
        '<script src="/assets/js/site-nav.min.js" defer></script>',
        '<script src="/assets/js/cookie-consent.js" defer></script>',
        '</body>',
        '</html>'
    ])
    
    return "\n".join(html)
# التنفيذ الرئيسي (مثال لتوليد خطة + مقال)
if __name__ == "__main__":
    trends = get_topic_trends()
    for trend in trends[:3]:
        main_topic = trend['title']
        article = generate_article_plan(main_topic)
        code = render_article_template(article)
        filename = "".join(c for c in main_topic[:15] if c.isalnum() or c in (' ', '_')).replace(' ','_') + ".html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"تم توليد مقال: {main_topic}")
