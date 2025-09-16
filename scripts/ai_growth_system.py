#!/usr/bin/env python3
"""
AI Growth System for Arabic Financial Content
نظام نمو ذكي لتوليد المحتوى المالي العربي
"""

import requests
import feedparser
import random
from googletrans import Translator

# RSS feeds للحصول على الاتجاهات
RSS_FEEDS = [
    "https://feeds.feedburner.com/oreilly/radar",
    "https://techcrunch.com/feed/"
]

# قوالب عناوين SEO
SEO_TITLES = [
    "دليل {} الشامل لعام {}",
    "أسرار {} المربحة في {}",
    "كيفية تحقيق النجاح في {} لعام {}"
]

def get_topic_trends():
    """جلب الاتجاهات الحالية من RSS feeds"""
    articles = []
    try:
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
    except Exception as e:
        print(f"Error fetching trends: {e}")
        # fallback topics
        articles = [
            {"title": "الاستثمار الذكي", "summary": "استراتيجيات الاستثمار", "link": "#"},
            {"title": "العملات الرقمية", "summary": "دليل التداول", "link": "#"}
        ]
    return articles

def fetch_google_trends(topic):
    """محاكاة جلب الكلمات المفتاحية الشائعة"""
    return [f"{topic}", f"استثمار {topic}", f"ربح من {topic}"]

def generate_article_plan(main_topic: str, year: str = "2025"):
    """توليد خطة/مخطط مقال كاملة"""
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

def render_article_template(article):
    """أجزاء توليد المقال الرئيسي (العنوان + الأقسام + الكلمات المفتاحية)"""
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

if __name__ == "__main__":
    """التنفيذ الرئيسي (مثال لتوليد خطة + مقال)"""
    trends = get_topic_trends()
    for trend in trends[:3]:
        main_topic = trend['title']
        article = generate_article_plan(main_topic)
        code = render_article_template(article)
        with open(f"{main_topic[:15].replace(' ','_')}.html", "w", encoding="utf-8") as f:
            f.write(code)
        print(f"تم توليد مقال: {main_topic}")