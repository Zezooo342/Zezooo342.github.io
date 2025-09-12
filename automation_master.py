import random
from datetime import datetime

class AutoContentGenerator:
    def __init__(self):
        self.topics = [
            "الاستثمار في مصر",
            "الربح من الانترنت",
            "العملات الرقمية",
            "سوق الأسهم السعودية",
            "مشاريع صغيرة في 2025",
            "التسويق بالعمولة"
        ]
        self.viral_templates = [
            "دليل شامل: كيف تبدأ في {topic} وتحقق أرباحًا حقيقة في 2025",
            "أفضل أسرار الخبراء في {topic} لن يخبرك بها أحد!",
            "خطوة بخطوة: كيف ربحت {amount}$ من {topic} خلال {timeframe}",
            "تحقيق الأمان المالي عبر {topic}: الخطة الشاملة",
            "كيف تتجنب أخطاء المبتدئين في {topic} وتتفوق بسرعة؟",
            "أسهل طرق النجاح في {topic} للعرب"
        ]
        self.amounts = ['500', '2000', '10000', '15000']
        self.timeframes = ['أسبوع', 'شهر', '3 أشهر', 'سنة']

    def generate_viral_titles(self, n=5):
        titles = []
        for _ in range(n):
            topic = random.choice(self.topics)
            template = random.choice(self.viral_templates)
            amount = random.choice(self.amounts)
            timeframe = random.choice(self.timeframes)
            title = template.format(topic=topic, amount=amount, timeframe=timeframe)
            titles.append(title)
        return titles

    def generate_article_outline(self, topic):
        return [
            f"مقدمة عن {topic}",
            f"أهم النصائح للنجاح في {topic}",
            f"أخطاء شائعة يجب تجنبها",
            f"تجارب حقيقية من السوق",
            "أسئلة شائعة وإجابات مفصّلة",
            f"خلاصة واستنتاجات نهائية عن {topic}"
        ]

    def suggest_keywords(self, topic):
        base_keywords = [
            "استثمار", "ربح", "مال", "مبتدئين", "شرح", "2025", "أسرار", "شرح عملي"
        ]
        return list(set([topic] + base_keywords))

    def generate_faq(self, topic):
        return [
            f"كيف أبدأ في {topic} من الصفر؟",
            f"ما أفضل طرق تحقيق ربح سريع من {topic}؟",
            f"ما هي المخاطر في {topic}؟ وكيف أتجنبها؟",
            f"هل {topic} مناسب لكل الأعمار؟"
        ]

    def render_article(self, title, topic):
        outline = self.generate_article_outline(topic)
        keywords = self.suggest_keywords(topic)
        faq = self.generate_faq(topic)
        html = f"<h1>{title}</h1>\n"
        html += f"<p>مقال حصري عن {topic}. أحدث المعلومات والتجارب العملية لتسهيل نجاحك في هذا المجال في 2025.</p>\n"
        for section in outline:
            html += f"<h2>{section}</h2>\n<p>.... (ضع هنا فقرة أصلية).</p>\n"
        html += "<h3>الأسئلة الشائعة</h3>\n<ul>\n"
        for q in faq:
            html += f"  <li>{q}</li>\n"
        html += "</ul>\n"
        html += "<!-- كلمات مفتاحية: " + ", ".join(keywords) + " -->\n"
        html += "<hr><small>تاريخ النشر: {}</small>\n".format(datetime.today().strftime("%Y-%m-%d"))
        return html

# مثال على توليد عناوين ومقال كامل:
if __name__ == "__main__":
    acg = AutoContentGenerator()
    print("عناوين مقترحة:")
    for t in acg.generate_viral_titles(3):
        print("- " + t)
    print("\nمثال ملف HTML لمقال:")
    title = acg.generate_viral_titles(1)[0]
    html = acg.render_article(title, "الربح من الانترنت")
    with open("make-money-online.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("تم توليد الملف make-money-online.html بنجاح.")
