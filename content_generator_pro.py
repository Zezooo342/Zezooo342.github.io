
import requests
import json
import os
import time
import random
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

class PerplexityContentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("مفتاح Perplexity Pro API مطلوب!")

        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # إعدادات قابلة للتخصيص
        self.batch_size = int(os.getenv('BATCH_SIZE', 20))
        self.delay = int(os.getenv('DELAY_BETWEEN_REQUESTS', 2))

        # تحميل قاعدة بيانات الكلمات المفتاحية
        with open('data/keywords.json', 'r', encoding='utf-8') as f:
            self.keywords_db = json.load(f)

        print(f"✅ تم تهيئة المولد بنجاح")
        print(f"📊 الإعدادات: {self.batch_size} مقال، تأخير {self.delay} ثانية")

    def generate_article(self, title: str, keyword: str, country: str) -> Dict:
        '''توليد مقال باستخدام Perplexity Pro API الحقيقي'''

        prompt = f'''
        اكتب مقال مالي محسن لـSEO باللغة العربية عن "{title}".

        متطلبات المقال:
        1. 800-1200 كلمة تقريباً
        2. استخدم عناوين فرعية واضحة (##, ###)
        3. أضف إحصائيات حديثة من عام 2024-2025 إن أمكن
        4. اكتب بأسلوب مهني ومفهوم للقارئ العادي
        5. اذكر نصائح عملية وقابلة للتطبيق
        6. تحدث عن المخاطر والفوائد بصراحة
        7. أضف معلومات خاصة بـ{country}

        هيكل المقال المطلوب:
        - مقدمة تشرح أهمية الموضوع (150 كلمة)
        - 3-4 عناوين رئيسية مع شرح مفصل
        - نصائح عملية للبدء
        - تحذيرات مهمة
        - خلاصة مع التوصيات النهائية

        اكتب محتوى أصلي ومفيد للقراء في {country} المهتمين بـ{keyword}.
        '''

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "sonar-pro",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                return {
                    "title": title,
                    "content": content,
                    "keyword": keyword,
                    "country": country,
                    "generated_at": datetime.now().isoformat(),
                    "status": "success",
                    "word_count": len(content.split())
                }
            else:
                error_msg = f"API Error {response.status_code}"
                if response.status_code == 429:
                    error_msg += " - Rate limit reached. زد التأخير بين الطلبات"
                elif response.status_code == 401:
                    error_msg += " - Invalid API key. تحقق من مفتاح API"

                return {
                    "title": title,
                    "error": error_msg,
                    "status": "error"
                }

        except requests.exceptions.Timeout:
            return {
                "title": title,
                "error": "Timeout - طلب استغرق وقت طويل",
                "status": "error"
            }
        except Exception as e:
            return {
                "title": title,
                "error": f"Unexpected error: {str(e)}",
                "status": "error"
            }

    def create_seo_html_page(self, article_data: Dict) -> str:
        '''إنشاء صفحة HTML محسنة لـSEO'''

        content_html = article_data['content']
        lines = content_html.split('\n')
        html_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            elif line.startswith('###'):
                html_content.append(f'<h3>{line.replace("###", "").strip()}</h3>')
            elif line.startswith('##'):
                html_content.append(f'<h2>{line.replace("##", "").strip()}</h2>')
            elif line.startswith('#'):
                html_content.append(f'<h1>{line.replace("#", "").strip()}</h1>')
            elif line.startswith('- '):
                if not html_content or not html_content[-1].startswith('<ul>'):
                    html_content.append('<ul>')
                html_content.append(f'<li>{line[2:].strip()}</li>')
            elif line.startswith('* '):
                if not html_content or not html_content[-1].startswith('<ul>'):
                    html_content.append('<ul>')
                html_content.append(f'<li>{line[2:].strip()}</li>')
            else:
                # إغلاق القائمة إذا كانت مفتوحة
                if html_content and html_content[-1].startswith('<li>'):
                    html_content.append('</ul>')
                html_content.append(f'<p>{line}</p>')

        # إغلاق آخر قائمة إن وجدت
        if html_content and html_content[-1].startswith('<li>'):
            html_content.append('</ul>')

        current_date = datetime.now().strftime('%Y-%m-%d')
        adsense_client = os.getenv('ADSENSE_CLIENT_ID', 'ca-pub-YOUR_PUBLISHER_ID')

        html_template = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']}</title>
    <meta name="description" content="دليل شامل عن {article_data['keyword']} في {article_data['country']} - نصائح واستراتيجيات للمستثمرين العرب">
    <meta name="keywords" content="{article_data['keyword']}, {article_data['country']}, استثمار, مال, اقتصاد, تداول">
    <meta name="robots" content="index, follow">
    <meta name="author" content="دليل المال العربي">

    <!-- Open Graph Tags -->
    <meta property="og:title" content="{article_data['title']}">
    <meta property="og:description" content="دليل شامل عن {article_data['keyword']} في {article_data['country']}">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="ar_AR">

    <link rel="stylesheet" href="../static/style.css">
    <link rel="canonical" href="https://yoursite.com/generated_pages/{article_data.get('filename', 'article')}.html">

    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_client}"
         crossorigin="anonymous"></script>

    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{article_data['title']}",
        "author": {{
            "@type": "Organization",
            "name": "دليل المال العربي"
        }},
        "datePublished": "{current_date}",
        "dateModified": "{current_date}",
        "description": "دليل شامل عن {article_data['keyword']} في {article_data['country']}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://yoursite.com/generated_pages/{article_data.get('filename', 'article')}.html"
        }}
    }}
    </script>
</head>
<body>
    <header>
        <nav>
            <h1><a href="../index.html">دليل المال العربي</a></h1>
            <p>مصدرك الموثوق للمعلومات المالية والاستثمارية</p>
        </nav>
    </header>

    <main>
        <article>
            <header class="article-header">
                <h1>{article_data['title']}</h1>
                <div class="article-meta">
                    <span>📅 {current_date}</span>
                    <span>🏷️ {article_data['keyword']}</span>
                    <span>🌍 {article_data['country']}</span>
                    <span>📖 {article_data.get('word_count', 0)} كلمة</span>
                </div>
            </header>

            <!-- إعلان أعلى المقال -->
            <div class="ad-container">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="{adsense_client}"
                     data-ad-slot="1234567890"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>

            <div class="article-content">
                {''.join(html_content)}
            </div>

            <!-- إعلان وسط المقال -->
            <div class="ad-container">
                <ins class="adsbygoogle"
                     style="display:block; text-align:center;"
                     data-ad-layout="in-article"
                     data-ad-format="fluid"
                     data-ad-client="{adsense_client}"
                     data-ad-slot="0987654321"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>

            <div class="article-footer">
                <p><strong>إخلاء مسؤولية:</strong> هذا المحتوى لأغراض تعليمية فقط. الاستثمار ينطوي على مخاطر، يرجى استشارة مختص مالي مؤهل قبل اتخاذ أي قرارات استثمارية.</p>
            </div>

        </article>

        <!-- مقالات ذات صلة -->
        <section class="related-articles">
            <h3>مقالات ذات صلة</h3>
            <p>المزيد من المقالات حول الاستثمار في المنطقة العربية...</p>
        </section>

    </main>

    <footer>
        <div class="footer-content">
            <p>&copy; 2025 دليل المال العربي - جميع الحقوق محفوظة</p>
            <p>📧 للاستفسارات: info@arabmoney.guide | 📱 للدعم الفني: support@arabmoney.guide</p>
        </div>
    </footer>
</body>
</html>'''

        return html_template

    def generate_batch(self, count: int = None):
        '''توليد مجموعة من المقالات'''

        count = count or self.batch_size
        generated = []
        topics = self.keywords_db['investment_topics']
        countries = self.keywords_db['countries']
        templates = self.keywords_db['article_templates']

        print(f"🚀 بدء توليد {count} مقال باستخدام Perplexity Pro...")
        print("=" * 60)

        for i in range(count):
            # اختيار عشوائي مع تجنب التكرار
            keyword = random.choice(topics)
            country = random.choice(countries)
            template = random.choice(templates)

            title = template.format(keyword=keyword, country=country)
            filename = f"{keyword.replace(' ', '_')}_{country.replace(' ', '_')}_{i+1:03d}.html"

            print(f"📝 توليد مقال {i+1}/{count}: {title}")

            # توليد المقال
            article = self.generate_article(title, keyword, country)

            if article['status'] == 'success':
                # إضافة اسم الملف لبيانات المقال
                article['filename'] = filename

                # إنشاء صفحة HTML محسنة
                html_content = self.create_seo_html_page(article)

                # حفظ الملف
                filepath = os.path.join('generated_pages', filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                generated.append({
                    'filename': filename,
                    'title': title,
                    'keyword': keyword,
                    'country': country,
                    'word_count': article.get('word_count', 0),
                    'status': 'success'
                })

                print(f"   ✅ تم الحفظ: {filename} ({article.get('word_count', 0)} كلمة)")
            else:
                print(f"   ❌ خطأ: {article.get('error', 'Unknown error')}")
                generated.append({
                    'title': title,
                    'status': 'error',
                    'error': article.get('error', 'Unknown error')
                })

            # تأخير لتجنب Rate Limiting
            if i < count - 1:  # لا تأخير بعد آخر طلب
                print(f"   ⏳ انتظار {self.delay} ثانية...")
                time.sleep(self.delay)

        return generated

    def generate_report(self, results: List[Dict]):
        '''إنشاء تقرير مفصل للتوليد'''

        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']

        total_words = sum(r.get('word_count', 0) for r in successful)
        avg_words = total_words / len(successful) if successful else 0

        report = {
            'generation_date': datetime.now().isoformat(),
            'total_requested': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': f"{len(successful)/len(results)*100:.1f}%",
            'total_words': total_words,
            'average_words_per_article': f"{avg_words:.0f}",
            'articles': results,
            'estimated_monthly_income': f"${len(successful) * 15 * 30 / 1000:.0f}" # تقدير بسيط
        }

        report_file = f"reports/generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('reports', exist_ok=True)

        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return report, report_file

def main():
    '''تشغيل النظام الرئيسي'''

    try:
        # إنشاء مولد المحتوى
        generator = PerplexityContentGenerator()

        # توليد المقالات
        results = generator.generate_batch()

        # إنشاء التقرير
        report, report_file = generator.generate_report(results)

        # طباعة النتائج
        print("\n" + "=" * 60)
        print("🎉 تقرير التوليد النهائي")
        print("=" * 60)
        print(f"📊 إجمالي المقالات المطلوبة: {report['total_requested']}")
        print(f"✅ نجح: {report['successful']} مقال")
        print(f"❌ فشل: {report['failed']} مقال")
        print(f"📈 معدل النجاح: {report['success_rate']}")
        print(f"📖 إجمالي الكلمات: {report['total_words']:,}")
        print(f"📄 متوسط الكلمات للمقال: {report['average_words_per_article']}")
        print(f"💰 الدخل المقدر شهرياً: {report['estimated_monthly_income']}")
        print(f"📁 الملفات محفوظة في: generated_pages/")
        print(f"📋 التقرير محفوظ في: {report_file}")

        if report['failed'] > 0:
            print("\n⚠️  مقالات فشل توليدها:")
            for i, result in enumerate([r for r in results if r['status'] == 'error'], 1):
                print(f"   {i}. {result['title']} - {result.get('error', 'خطأ غير معروف')}")

        print("\n🚀 نصائح للخطوات التالية:")
        print("1. ارفع المقالات على استضافة ويب")
        print("2. سجل في Google AdSense")
        print("3. شغل النظام يومياً لمحتوى جديد")
        print("4. راقب أداء المقالات في محركات البحث")

    except ValueError as e:
        print(f"❌ خطأ في الإعداد: {e}")
        print("تأكد من إضافة مفتاح Perplexity Pro API في ملف .env")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        print("تحقق من اتصالك بالإنترنت ومفتاح API")

if __name__ == "__main__":
    main()
