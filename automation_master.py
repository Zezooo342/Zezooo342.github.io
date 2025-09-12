from datetime import datetime
from self_optimization import SelfOptimizationEngine

class AutoPublisher:
    """
    نظام جدولة ونشر ذكي يعتمد على اقتراحات وتحسينات حية تلقائية
    """
    def __init__(self):
        self.optimizer = SelfOptimizationEngine()

    def get_publication_plan(self, traffic, social, conv, revenue):
        recs = self.optimizer.analyze_and_improve(traffic, social, conv, revenue)
        # مثال: جدولة النشر وضبط نوع المقال والكلمة المفتاحية
        topic = recs.get('content_focus','استثمار')
        keywords = recs.get('focus_keywords',['استثمار','مال'])
        time = recs.get('posting_schedule','8:00pm')
        print(f"الموضوع المقترح:{topic}\nالكلمات الرئيسية:{keywords}\nوقت النشر الأفضل:{time}")
        return topic, keywords, time

    def publish_content(self, title, html_content, file_name):
        # يمكن التوصيل مستقبلاً مع API، هنا فقط حفظ HTML
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"تم نشر: {file_name}")

if __name__ == "__main__":
    auto_pub = AutoPublisher()
    # بيانات تمثيلية للاختبار
    traffic = {'top_content_type': 'طرق ربح المال', 'top_keywords': ['أدسنس', 'مشاريع مربحة']}
    social = {'best_time': '10:00pm', 'engagement_rate': 0.13}
    conv = {'avg_rate': 0.021}
    revenue = {'rpm': 2.9}
    # الحصول على خطة نشر وتحسين
    topic, keywords, time = auto_pub.get_publication_plan(traffic, social, conv, revenue)
    # مثال: توليد مقال باسم دقيق
    title = f"أفضل أسرار {topic} في {datetime.today().year}"
    html = f"<html><body><h1>{title}</h1><p>محتوى ديناميكي احترافي بناء على توصية ذكية في أفضل توقيت للنشر.</p></body></html>"
    file_name = topic[:15].replace(' ', '_')+"_auto.html"
    auto_pub.publish_content(title, html, file_name)
