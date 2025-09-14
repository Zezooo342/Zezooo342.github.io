import requests
from googletrans import Translator
    
for url in RSS_FEEDS:
        d = feedparser.parse(url)
        translator = Translator()
        for entry in d.entries[:3]:
            text = entry.title + " " + getattr(entry, "summary", "")
            if len(text) > 30:
                articles.append({
                    "title": entry.title,
                    "summary": translator.translate(text, dest='ar').text if entry.title else "",
                    "link": entry.link
                })
    return articles
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
        html += f'  <a href="{link}">{link[1:-5]}</a>\n'
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
        with open(f"{main_topic[:15].replace(' ','_')}.html", "w", encoding="utf-8") as f:
            f.write(code)
        print(f"تم توليد مقال: {main_topic}")
