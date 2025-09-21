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
    html = f"<h1>{article['headline']}</h1>\n"
    html += f"<p>{article['summary']}</p>\n"
    for section in article["outline"]:
        html += f"<h2>{section}</h2>\n.... (أضف فقرة أصلية هنا)\n"
    html += "الأسئلة الشائعة\n<ul>\n"
    for q in article["questions"]:
        html += f"  <li>{q}</li>\n"
    html += "</ul>\n"
    html += "مواضيع متعلقة:\n<ul>\n"
    for link in article["internal_links"]:
        link_text = link.replace("/", "").replace(".html", "") if link.startswith("/") and link.endswith(".html") else link
        html += f'  <a href="{link}">{link_text}</a>\n'
    html += "</ul>\n"
    html += "<!-- كلمات مفتاحية مقترحة: " + ", ".join(article["seo_keywords"]) + " -->\n"
    return html
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
