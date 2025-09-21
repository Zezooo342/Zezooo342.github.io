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
    ترجمة آمنة إلى العربية:
    - تعيد النص كما هو إذا كان عربيًا بالفعل أو فارغًا.
    - تتعامل مع غياب googletrans أو أخطاء الشبكة دون كسر التنفيذ.
    """
    if not text:
        return ""
    if _contains_arabic(text):
        return text
    if Translator is None:
        return text
    try:
        tr = Translator()  # استخدام الإعدادات الافتراضية للمكتبة
        res = tr.translate(text, dest=dest, src=src)
        return res.text or text
    except Exception:
        return text

def fetch_google_trends(topic):
    """جلب الكلمات المفتاحية المرتبطة بالموضوع"""
    # محاكاة جلب الكلمات المفتاحية - يمكن ربطها بـ Google Trends API لاحقاً
    base_keywords = ["استثمار", "ربح", "مال", "تجارة", "أعمال"]
    topic_keywords = topic.split()
    return base_keywords + topic_keywords[:3]
# توليد خطة/مخطط مقال كاملة
def generate_article_plan(main_topic: str, year: str = "2025"):
    keywords = fetch_google_trends(main_topic)
    headline = random.choice(SEO_TITLES).format(main_topic, year)
    outline = [
        "مقدمة عن {}".format(main_topic),
        "أهم مميزات {}".format(main_topic),
        "أخطاء شائعة يجب تجنبها في {}".format(main_topic),
        "دليل خطوة بخطوة لتحقيق النجاح في {}".format(main_topic),
        "أسئلة الباحثين وملخص نهائي"
    ]
    questions = [
        "ما هي أهم نصائح {}؟".format(main_topic),
        "كيف أبدأ {} بنجاح؟".format(main_topic),
        "ما المخاطر وكيف يمكن تفاديها؟"
    ]
    article = {
        "headline": headline,
        "summary": f"كل ما تريد معرفته عن {main_topic} وأهم الأسرار والتوصيات العملية لعام {year}.",
        "outline": outline,
        "seo_keywords": keywords,
        "internal_links": ["/index.html", "/about.html"],
        "questions": questions
    }
    return article
# أجزاء توليد المقال الرئيسي (العنوان + الأقسام + الكلمات المفتاحية)
def render_article_template(article):
    # غلاف HTML بسيط مع وسم عربي وcanonical وروابط سياسة
    slug = re.sub(r"\s+", "_", article['headline'][:40])
    slug = re.sub(r"[^\w\u0600-\u06FF_]+", "", slug)
    html = [
        "<!DOCTYPE html>",
        '<html lang="ar" dir="rtl">',
        '<head>',
        f"  <meta charset=\"utf-8\">",
        f"  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
        f"  <title>{article['headline']} | دليل المال العربي</title>",
        f"  <meta name=\"description\" content=\"{article['summary']}\">",
        f"  <link rel=\"canonical\" href=\"https://zezooo342.github.io/{slug}.html\">",
        '  <link rel="stylesheet" href="/assets/css/common.min.css">',
        '</head>',
        '<body>',
        '  <header id="site-header"></header>',
        '  <div class="main" data-ld-article>',
        f"    <h1>{article['headline']}</h1>",
        f"    <p>{article['summary']}</p>",
    ]
    for section in article["outline"]:
        html.append(f"    <h2>{section}</h2>")
        html.append("    <p>هذا القسم مكتوب بمحتوى عربي أصلي يشرح الفكرة ببساطة ووضوح.</p>")
    html.append("    <h2>الأسئلة الشائعة</h2>")
    html.append("    <ul>")
    for q in article["questions"]:
        html.append(f"      <li>{q}</li>")
    html.append("    </ul>")
    html.append("    <h2>روابط مهمة</h2>")
    html.append("    <ul>")
    for link in article["internal_links"]:
        link_text = link.replace("/", "").replace(".html", "") if link.startswith("/") and link.endswith(".html") else link
        html.append(f'      <li><a href="{link}">{link_text}</a></li>')
    html.append("    </ul>")
    html.append("  </div>")
    html.append('  <footer id="site-footer"></footer>')
    html.append('  <script src="/assets/js/site-nav.min.js" defer></script>')
    html.append('  <script src="/assets/js/cookie-consent.js" defer></script>')
    html.append('</body>')
    html.append('</html>')
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
