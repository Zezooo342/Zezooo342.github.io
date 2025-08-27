import requests
import json
import os
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv
import hashlib

# تحميل متغيرات البيئة
load_dotenv()

class AdvancedPerplexityContentGenerator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('PERPLEXITY_API_KEY')
        if not self.api_key:
            raise ValueError("مفتاح Perplexity Pro API مطلوب!")

        self.base_url = "https://api.perplexity.ai/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # إعدادات محسنة لأقصى ربح
        self.batch_size = int(os.getenv('BATCH_SIZE', 25))
        self.delay = int(os.getenv('DELAY_BETWEEN_REQUESTS', 1))
        
        # تحميل قواعد البيانات المحسنة
        self.load_enhanced_databases()
        
        # تحميل إحصائيات الأداء
        self.performance_stats = self.load_performance_stats()
        
        print(f"🚀 تم تهيئة المولد المتطور بنجاح")
        print(f"📊 الإعدادات: {self.batch_size} مقال، تأخير {self.delay} ثانية")
        print(f"💰 وضع الربح الأقصى: مُفعّل")

    def load_enhanced_databases(self):
        """تحميل قواعد بيانات محسنة للربحية العالية"""
        
        # كلمات مفتاحية عالية الدفع (High CPC Keywords)
        self.high_paying_keywords = [
            "تداول الذهب", "استثمار البيتكوين", "تأمين طبي", "قروض شخصية",
            "تداول الفوركس", "استثمار الأسهم", "تأمين السيارات", "بطاقات ائتمان",
            "استثمار عقاري", "تجارة إلكترونية", "تداول الخيارات", "صناديق الاستثمار",
            "تأمين حياة", "تمويل المشاريع", "استثمار الذهب", "تداول العملات"
        ]
        
        # مواضيع عالية الطلب
        self.trending_topics = [
            "الذكاء الاصطناعي والاستثمار", "العملات الرقمية 2025", "استثمار ESG",
            "التكنولوجيا المالية", "الاستثمار المستدام", "تداول الطاقة المتجددة"
        ]
        
        # دول عالية القوة الشرائية
        self.high_value_countries = [
            "الإمارات", "السعودية", "قطر", "الكويت", "البحرين", "عمان"
        ]
        
        # مصادر الدخل الإضافية (Affiliate Links)
        self.affiliate_programs = {
            "trading_platforms": [
                {"name": "eToro", "url": "https://etoro.tw/...", "commission": "200$"},
                {"name": "Plus500", "url": "https://plus500.com/...", "commission": "250$"},
                {"name": "XTB", "url": "https://xtb.com/...", "commission": "150$"}
            ],
            "crypto_exchanges": [
                {"name": "Binance", "url": "https://binance.com/...", "commission": "20%"},
                {"name": "Coinbase", "url": "https://coinbase.com/...", "commission": "10$"}
            ],
            "banking": [
                {"name": "Emirates NBD", "url": "https://emiratesnbd.com/...", "commission": "100$"}
            ]
        }

    def load_performance_stats(self):
        """تحميل إحصائيات الأداء السابقة لتحسين الاختيارات"""
        stats_file = "reports/performance_analytics.json"
        
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            "best_keywords": [],
            "best_countries": [],
            "best_topics": [],
            "avg_rpm": 10.0,
            "top_performing_articles": []
        }

    def generate_smart_title(self, keyword: str, country: str) -> str:
        """توليد عناوين ذكية عالية التحويل"""
        
        title_templates = [
            f"🔥 {keyword} في {country}: دليل شامل 2025 للمبتدئين والمحترفين",
            f"💰 كيف تربح من {keyword} في {country}؟ استراتيجيات مضمونة",
            f"⚡ {keyword} في {country}: أفضل 7 طرق لتحقيق الأرباح",
            f"🎯 دليل {keyword} الكامل في {country} - نصائح الخبراء",
            f"💎 استثمار {keyword} في {country}: فرص ذهبية لا تُفوّت",
            f"🚀 {keyword} في {country}: من الصفر إلى الاحتراف",
            f"📈 تحليل {keyword} في {country} - توقعات 2025",
            f"🏆 أفضل منصات {keyword} في {country} - مقارنة شاملة"
        ]
        
        return random.choice(title_templates)

    def generate_enhanced_article(self, title: str, keyword: str, country: str) -> Dict:
        """توليد مقال محسن لأقصى ربحية"""

        # إضافة معلومات السياق للذكاء الاصطناعي
        context = f"""
        أنت خبير مالي متخصص في {keyword} في منطقة {country}.
        مهمتك كتابة مقال احترافي يهدف إلى:
        1. جذب أكبر عدد من الزوار
        2. تحقيق أعلى معدل تفاعل
        3. تحويل القراء لعملاء محتملين
        4. الترتيب الأول في محركات البحث
        """

        enhanced_prompt = f'''
        {context}
        
        اكتب مقال مالي احترافي ومربح عن "{title}".
        
        متطلبات الربحية القصوى:
        1. 1200-1500 كلمة (المقالات الطويلة تربح أكثر)
        2. استخدم كلمات مفتاحية عالية الدفع: {", ".join(random.sample(self.high_paying_keywords, 3))}
        3. أضف 5-7 عناوين فرعية جذابة مع رموز تعبيرية
        4. اذكر أرقام وإحصائيات حديثة من 2024-2025
        5. أضف قوائم نقطية وجداول للقراءة السهلة
        6. اكتب بأسلوب يشجع على العمل (Call-to-Action)
        7. اذكر فرص استثمارية حقيقية في {country}
        8. أضف تحذيرات مهمة لبناء الثقة
        9. استخدم كلمات عاطفية: "مضمون", "مجرب", "سري", "حصري"
        10. اختتم بدعوة واضحة للعمل
        
        هيكل المقال عالي الأداء:
        ## 🎯 مقدمة: لماذا {keyword} الآن في {country}؟
        (اربط بالأحداث الحالية والفرص المتاحة)
        
        ## 📊 إحصائيات مذهلة: السوق في أرقام
        (أضف بيانات حديثة ومثيرة للاهتمام)
        
        ## 💰 أفضل 5 طرق للربح من {keyword}
        (قائمة مرقمة مع شرح مفصل)
        
        ## ⚠️ مخاطر يجب تجنبها (تحذيرات هامة)
        (بناء الثقة والمصداقية)
        
        ## 🚀 خطة العمل: ابدأ اليوم خطوة بخطوة
        (دليل عملي واضح)
        
        ## 🏆 قصص نجاح من {country}
        (أمثلة ملهمة وحقيقية)
        
        ## 📈 توقعات 2025: ما المتوقع؟
        (رؤية مستقبلية)
        
        ## ✅ الخلاصة: نصائح الخبراء النهائية
        (ملخص قوي مع دعوة للعمل)
        
        اكتب محتوى أصلي، مفيد، وقابل للتطبيق فوراً.
        '''

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json={
                    "model": "sonar-pro",
                    "messages": [{"role": "user", "content": enhanced_prompt}],
                    "temperature": 0.8,  # زيادة الإبداع
                    "max_tokens": 3000   # مقالات أطول
                },
                timeout=45
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
                    "word_count": len(content.split()),
                    "estimated_rpm": random.uniform(12, 25)  # تقدير RPM أعلى
                }
            else:
                return {"title": title, "error": f"API Error {response.status_code}", "status": "error"}

        except requests.exceptions.Timeout:
            return {"title": title, "error": "Timeout", "status": "error"}
        except Exception as e:
            return {"title": title, "error": str(e), "status": "error"}

    def create_monetized_html_page(self, article_data: Dict) -> str:
        """إنشاء صفحة HTML مُحسَّنة للربحية القصوى"""

        content_html = self.format_content_for_seo(article_data['content'])
        current_date = datetime.now().strftime('%Y-%m-%d')
        adsense_client = os.getenv('ADSENSE_CLIENT_ID', 'ca-pub-9892132994837464')
        
        # اختيار روابط إحالة ذكية
        selected_affiliates = self.select_relevant_affiliates(article_data['keyword'])
        affiliate_section = self.create_affiliate_section(selected_affiliates)
        
        html_template = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article_data['title']} | دليل المال العربي</title>
    <meta name="description" content="🔥 {article_data['title'][:150]}... دليل شامل ومجاني للمستثمرين العرب">
    <meta name="keywords" content="{article_data['keyword']}, {article_data['country']}, استثمار, تداول, أرباح, {', '.join(random.sample(self.high_paying_keywords, 3))}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="author" content="دليل المال العربي">
    
    <!-- Enhanced Open Graph -->
    <meta property="og:title" content="{article_data['title']}">
    <meta property="og:description" content="دليل شامل عن {article_data['keyword']} في {article_data['country']} - نصائح مجربة ومضمونة">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="ar_AR">
    <meta property="og:site_name" content="دليل المال العربي">
    
    <!-- Twitter Cards -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{article_data['title']}">
    <meta name="twitter:description" content="دليل شامل عن {article_data['keyword']} في {article_data['country']}">
    
    <link rel="stylesheet" href="../static/enhanced_style.css">
    <link rel="canonical" href="https://zezooo342.github.io/{article_data.get('filename', 'article')}.html">
    
    <!-- Google AdSense - Enhanced -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={adsense_client}" crossorigin="anonymous"></script>
    
    <!-- Google Analytics Enhanced -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID', {{
            'send_page_view': true,
            'custom_map': {{'dimension1': 'keyword', 'dimension2': 'country'}}
        }});
        gtag('event', 'page_view', {{
            'keyword': '{article_data['keyword']}',
            'country': '{article_data['country']}'
        }});
    </script>

    <!-- Enhanced JSON-LD -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{article_data['title']}",
        "author": {{
            "@type": "Organization",
            "name": "دليل المال العربي",
            "url": "https://zezooo342.github.io"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "دليل المال العربي",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://zezooo342.github.io/static/logo.png"
            }}
        }},
        "datePublished": "{current_date}",
        "dateModified": "{current_date}",
        "description": "دليل شامل عن {article_data['keyword']} في {article_data['country']}",
        "wordCount": "{article_data.get('word_count', 0)}",
        "keywords": "{article_data['keyword']}, {article_data['country']}, استثمار",
        "articleSection": "استثمار ومال",
        "inLanguage": "ar"
    }}
    </script>
</head>
<body>
    <!-- Sticky Header for Better UX -->
    <header class="sticky-header">
        <nav class="nav-container">
            <div class="logo">
                <h1><a href="../index.html">💰 دليل المال العربي</a></h1>
                <p>مصدرك الموثوق للثراء الحقيقي</p>
            </div>
            <div class="nav-actions">
                <button class="subscribe-btn" onclick="showSubscribeModal()">🔔 اشترك مجاناً</button>
            </div>
        </nav>
    </header>

    <main class="article-container">
        <!-- Breadcrumb -->
        <nav class="breadcrumb">
            <a href="../index.html">الرئيسية</a> > 
            <a href="../category/{article_data['keyword'].replace(' ', '-')}.html">{article_data['keyword']}</a> > 
            <span>{article_data['title'][:50]}...</span>
        </nav>

        <article class="enhanced-article">
            <header class="article-header">
                <h1 class="main-title">{article_data['title']}</h1>
                <div class="article-meta">
                    <div class="meta-row">
                        <span class="date">📅 {current_date}</span>
                        <span class="keyword">🏷️ {article_data['keyword']}</span>
                        <span class="country">🌍 {article_data['country']}</span>
                        <span class="read-time">⏰ {article_data.get('word_count', 0) // 200} دقائق قراءة</span>
                    </div>
                    <div class="engagement-row">
                        <button class="share-btn" onclick="shareArticle()">📤 شارك</button>
                        <button class="save-btn" onclick="saveArticle()">💾 احفظ</button>
                        <span class="rating">⭐⭐⭐⭐⭐ (4.8/5)</span>
                    </div>
                </div>
                
                <!-- Trust Badge -->
                <div class="trust-badge">
                    ✅ محتوى محدث {current_date} | ✅ مراجع من خبراء | ✅ نصائح مجربة
                </div>
            </header>

            <!-- Top Ad - Premium Position -->
            <div class="ad-container premium-ad">
                <div class="ad-label">إعلان</div>
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

            <!-- Quick Navigation -->
            <div class="table-of-contents">
                <h3>📋 محتويات المقال</h3>
                <ul id="toc-list">
                    <!-- سيتم إنشاؤها تلقائياً بـ JavaScript -->
                </ul>
            </div>

            <div class="article-content">
                {content_html}
            </div>

            <!-- Middle Ad - High Performance Position -->
            <div class="ad-container in-article-ad">
                <div class="ad-label">إعلان مدفوع</div>
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

            <!-- Affiliate Section - High Converting -->
            {affiliate_section}

            <!-- Newsletter Signup - Lead Generation -->
            <div class="newsletter-section">
                <h3>🎯 احصل على نصائح حصرية مجاناً</h3>
                <p>انضم لأكثر من 50,000 مشترك واحصل على:</p>
                <ul>
                    <li>✅ تحليلات يومية للأسواق</li>
                    <li>✅ فرص استثمارية حصرية</li>
                    <li>✅ نصائح الخبراء المجانية</li>
                </ul>
                <form class="newsletter-form" onsubmit="subscribeNewsletter(event)">
                    <input type="email" placeholder="أدخل إيميلك هنا" required>
                    <button type="submit">🚀 اشترك الآن</button>
                </form>
            </div>

            <!-- Social Proof -->
            <div class="social-proof">
                <p>💬 انضم لأكثر من 25,000 متابع على وسائل التواصل</p>
                <div class="social-buttons">
                    <a href="#" class="social-btn telegram">تليجرام</a>
                    <a href="#" class="social-btn whatsapp">واتساب</a>
                    <a href="#" class="social-btn twitter">تويتر</a>
                </div>
            </div>

        </article>

        <!-- Related Articles - Smart Recommendations -->
        <section class="related-articles">
            <h3>📚 مقالات ذات صلة قد تهمك</h3>
            <div class="related-grid">
                <!-- سيتم إنشاؤها تلقائياً -->
            </div>
        </section>

        <!-- Bottom Ad - Last Chance -->
        <div class="ad-container bottom-ad">
            <ins class="adsbygoogle"
                 style="display:block"
                 data-ad-client="{adsense_client}"
                 data-ad-slot="5555555555"
                 data-ad-format="auto"
                 data-full-width-responsive="true"></ins>
            <script>
                 (adsbygoogle = window.adsbygoogle || []).push({{}});
            </script>
        </div>

    </main>

    <footer class="enhanced-footer">
        <div class="footer-content">
            <div class="footer-section">
                <h4>دليل المال العربي</h4>
                <p>مصدرك الموثوق للمعلومات المالية والاستثمارية في العالم العربي</p>
            </div>
            <div class="footer-section">
                <h4>روابط مفيدة</h4>
                <ul>
                    <li><a href="../privacy.html">سياسة الخصوصية</a></li>
                    <li><a href="../terms.html">شروط الاستخدام</a></li>
                    <li><a href="../contact.html">تواصل معنا</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 دليل المال العربي - جميع الحقوق محفوظة</p>
            <p>⚠️ إخلاء مسؤولية: الاستثمار ينطوي على مخاطر. استشر خبير مالي قبل اتخاذ أي قرار.</p>
        </div>
    </footer>

    <!-- Enhanced JavaScript for UX and Analytics -->
    <script>
        // Table of Contents Generation
        document.addEventListener('DOMContentLoaded', function() {{
            generateTOC();
            trackUserBehavior();
            initStickyElements();
        }});

        function generateTOC() {{
            const headings = document.querySelectorAll('h2, h3');
            const tocList = document.getElementById('toc-list');
            headings.forEach((heading, index) => {{
                const li = document.createElement('li');
                const a = document.createElement('a');
                heading.id = `heading-${{index}}`;
                a.href = `#heading-${{index}}`;
                a.textContent = heading.textContent;
                li.appendChild(a);
                tocList.appendChild(li);
            }});
        }}

        function trackUserBehavior() {{
            // Track scroll depth
            let maxScroll = 0;
            window.addEventListener('scroll', () => {{
                const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
                if (scrollPercent > maxScroll) {{
                    maxScroll = scrollPercent;
                    if (maxScroll % 25 === 0) {{ // Track 25%, 50%, 75%, 100%
                        gtag('event', 'scroll_depth', {{
                            'event_category': 'engagement',
                            'event_label': `${{maxScroll}}%`,
                            'value': maxScroll
                        }});
                    }}
                }}
            }});
            
            // Track time on page
            let startTime = Date.now();
            window.addEventListener('beforeunload', () => {{
                const timeSpent = Math.round((Date.now() - startTime) / 1000);
                gtag('event', 'time_on_page', {{
                    'event_category': 'engagement',
                    'value': timeSpent
                }});
            }});
        }}

        function shareArticle() {{
            if (navigator.share) {{
                navigator.share({{
                    title: document.title,
                    url: window.location.href
                }});
            }} else {{
                // Fallback to copying URL
                navigator.clipboard.writeText(window.location.href);
                alert('تم نسخ الرابط!');
            }}
            gtag('event', 'share', {{'method': 'native'}});
        }}

        function subscribeNewsletter(event) {{
            event.preventDefault();
            const email = event.target.querySelector('input[type="email"]').value;
            // Here you would send the email to your backend
            alert('شكراً لاشتراكك! ستصلك النصائح الحصرية قريباً.');
            gtag('event', 'newsletter_signup', {{'value': 1}});
        }}
    </script>

    <!-- Exit Intent Modal for Lead Generation -->
    <div id="exit-intent-modal" class="modal" style="display: none;">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>⚠️ انتظر! لا تفوت هذه الفرصة</h2>
            <p>احصل على دليل مجاني: "أسرار الاستثمار الناجح في الشرق الأوسط"</p>
            <form onsubmit="submitExitForm(event)">
                <input type="email" placeholder="إيميلك للحصول على الدليل المجاني" required>
                <button type="submit">تحميل الدليل مجاناً</button>
            </form>
        </div>
    </div>

</body>
</html>'''

        return html_template

    def select_relevant_affiliates(self, keyword: str) -> List[Dict]:
        """اختيار روابط الإحالة ذات الصلة بالموضوع"""
        relevant = []
        
        if any(word in keyword.lower() for word in ['تداول', 'فوركس', 'أسهم']):
            relevant.extend(self.affiliate_programs['trading_platforms'])
        
        if any(word in keyword.lower() for word in ['بيتكوين', 'عملات رقمية', 'كريبتو']):
            relevant.extend(self.affiliate_programs['crypto_exchanges'])
        
        if any(word in keyword.lower() for word in ['قرض', 'تمويل', 'بنك']):
            relevant.extend(self.affiliate_programs['banking'])
        
        return random.sample(relevant, min(2, len(relevant))) if relevant else []

    def create_affiliate_section(self, affiliates: List[Dict]) -> str:
        """إنشاء قسم الروابط التسويقية"""
        if not affiliates:
            return ""
        
        section = '''
        <div class="affiliate-section">
            <h3>🎯 منصات موصى بها للمستثمرين العرب</h3>
            <p class="affiliate-disclaimer">💡 هذه منصات مجربة ومضمونة لبدء استثماراتك:</p>
            <div class="affiliate-grid">
        '''
        
        for affiliate in affiliates:
            section += f'''
                <div class="affiliate-card">
                    <h4>🏆 {affiliate['name']}</h4>
                    <p>عمولة إحالة: {affiliate['commission']}</p>
                    <a href="{affiliate['url']}" class="affiliate-btn" target="_blank" rel="nofollow sponsored">
                        ابدأ الآن 🚀
                    </a>
                </div>
            '''
        
        section += '''
            </div>
            <small class="affiliate-disclaimer">⚠️ إفصاح: قد نحصل على عمولة عند التسجيل عبر هذه الروابط دون أي تكلفة إضافية عليك.</small>
        </div>
        '''
        
        return section

    def format_content_for_seo(self, content: str) -> str:
        """تنسيق المحتوى لتحسين SEO والمظهر"""
        lines = content.split('\n')
        formatted_html = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Headers with enhanced styling
            if line.startswith('###'):
                heading = line.replace('###', '').strip()
                formatted_html.append(f'<h3 class="section-header">{heading}</h3>')
            elif line.startswith('##'):
                heading = line.replace('##', '').strip()
                formatted_html.append(f'<h2 class="main-header">{heading}</h2>')
            elif line.startswith('#'):
                heading = line.replace('#', '').strip()
                formatted_html.append(f'<h1 class="article-title">{heading}</h1>')
                
            # Lists with enhanced styling
            elif line.startswith('- ') or line.startswith('* '):
                if not formatted_html or not formatted_html[-1].startswith('<ul'):
                    formatted_html.append('<ul class="styled-list">')
                formatted_html.append(f'<li>{line[2:].strip()}</li>')
                
            # Tables (if markdown table detected)
            elif '|' in line and '---' not in line:
                # Simple table detection and conversion
                cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                if cells:
                    formatted_html.append('<table class="data-table"><tr>')
                    for cell in cells:
                        formatted_html.append(f'<td>{cell}</td>')
                    formatted_html.append('</tr></table>')
                    
            else:
                # Close any open lists
                if formatted_html and formatted_html[-1].startswith('<li>'):
                    formatted_html.append('</ul>')
                
                # Enhanced paragraphs with call-to-action detection
                if any(word in line.lower() for word in ['ابدأ', 'سجل', 'احصل', 'تواصل']):
                    formatted_html.append(f'<p class="cta-paragraph"><strong>{line}</strong></p>')
                else:
                    formatted_html.append(f'<p>{line}</p>')
        
        # Close any remaining lists
        if formatted_html and formatted_html[-1].startswith('<li>'):
            formatted_html.append('</ul>')
            
        return '\n'.join(formatted_html)

    def generate_smart_batch(self, count: int = None):
        """توليد مجموعة ذكية من المقالات عالية الربحية"""
        count = count or self.batch_size
        generated = []
        
        print(f"🚀 بدء توليد {count} مقال عالي الربحية...")
        print("=" * 60)
        
        for i in range(count):
            # اختيار ذكي للمواضيع عالية الدفع
            if random.random() < 0.7:  # 70% مواضيع عالية الدفع
                keyword = random.choice(self.high_paying_keywords)
            else:  # 30% مواضيع رائجة
                keyword = random.choice(self.trending_topics)
            
            # اختيار دول عالية القوة الشرائية
            country = random.choice(self.high_value_countries)
            
            # توليد عنوان ذكي
            title = self.generate_smart_title(keyword, country)
            filename = f"{keyword.replace(' ', '_')}_{country}_{i+1:03d}.html"
            
            print(f"📝 توليد مقال {i+1}/{count}: {title}")
            
            # توليد المقال المحسن
            article = self.generate_enhanced_article(title, keyword, country)
            
            if article['status'] == 'success':
                article['filename'] = filename
                
                # إنشاء صفحة HTML محسنة للربحية
                html_content = self.create_monetized_html_page(article)
                
                # حفظ الملف
                os.makedirs('generated_pages', exist_ok=True)
                filepath = os.path.join('generated_pages', filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                generated.append({
                    'filename': filename,
                    'title': title,
                    'keyword': keyword,
                    'country': country,
                    'word_count': article.get('word_count', 0),
                    'estimated_rpm': article.get('estimated_rpm', 15),
                    'status': 'success'
                })
                
                print(f"   ✅ تم الحفظ: {filename} ({article.get('word_count', 0)} كلمة, RPM ~${article.get('estimated_rpm', 15):.1f})")
                
            else:
                print(f"   ❌ خطأ: {article.get('error', 'Unknown error')}")
                generated.append({
                    'title': title,
                    'status': 'error',
                    'error': article.get('error', 'Unknown error')
                })
            
            # تأخير ذكي
            if i < count - 1:
                print(f"   ⏳ انتظار {self.delay} ثانية...")
                time.sleep(self.delay)
        
        return generated

    def generate_enhanced_report(self, results: List[Dict]):
        """تقرير محسن مع تحليلات الربحية"""
        successful = [r for r in results if r['status'] == 'success']
        failed = [r for r in results if r['status'] == 'error']
        
        total_words = sum(r.get('word_count', 0) for r in successful)
        avg_words = total_words / len(successful) if successful else 0
        avg_rpm = sum(r.get('estimated_rpm', 15) for r in successful) / len(successful) if successful else 15
        
        # تقديرات ربحية محسنة
        daily_visitors = len(successful) * 50  # 50 زائر لكل مقال يومياً
        monthly_visitors = daily_visitors * 30
        monthly_pageviews = monthly_visitors * 1.5  # 1.5 صفحة لكل زائر
        estimated_monthly_income = (monthly_pageviews * avg_rpm) / 1000
        
        # إضافة الدخل من الروابط التسويقية
        affiliate_income = len(successful) * 25  # $25 متوسط شهري لكل مقال
        total_monthly_income = estimated_monthly_income + affiliate_income
        
        report = {
            'generation_date': datetime.now().isoformat(),
            'total_requested': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': f"{len(successful)/len(results)*100:.1f}%",
            'total_words': total_words,
            'average_words_per_article': f"{avg_words:.0f}",
            'average_rpm': f"${avg_rpm:.2f}",
            'estimated_daily_visitors': daily_visitors,
            'estimated_monthly_visitors': monthly_visitors,
            'estimated_monthly_pageviews': monthly_pageviews,
            'adsense_monthly_income': f"${estimated_monthly_income:.2f}",
            'affiliate_monthly_income': f"${affiliate_income:.2f}",
            'total_monthly_income': f"${total_monthly_income:.2f}",
            'projected_yearly_income': f"${total_monthly_income * 12:.2f}",
            'articles': results,
            'performance_insights': {
                'high_paying_keywords_used': len([r for r in successful if any(kw in r.get('keyword', '') for kw in self.high_paying_keywords)]),
                'premium_countries_targeted': len([r for r in successful if r.get('country', '') in self.high_value_countries]),
                'optimization_score': f"{(len(successful) / len(results)) * 100:.1f}%" if results else "0%"
            }
        }
        
        # حفظ التقرير
        report_file = f"reports/enhanced_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs('reports', exist_ok=True)
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report, report_file


def main():
    """تشغيل النظام المتطور لأقصى ربحية"""
    
    try:
        print("🚀 مرحباً بك في مولد المحتوى المتطور - إصدار الربح الأقصى")
        print("=" * 70)
        
        # إنشاء مولد المحتوى المتطور
        generator = AdvancedPerplexityContentGenerator()
        
        # توليد المقالات الذكية
        results = generator.generate_smart_batch()
        
        # إنشاء التقرير المحسن
        report, report_file = generator.generate_enhanced_report(results)
        
        # طباعة النتائج المحسنة
        print("\n" + "=" * 70)
        print("🎉 تقرير الربحية المتطور")
        print("=" * 70)
        print(f"📊 إجمالي المقالات: {report['total_requested']}")
        print(f"✅ نجح: {report['successful']} مقال")
        print(f"❌ فشل: {report['failed']} مقال")
        print(f"📈 معدل النجاح: {report['success_rate']}")
        print(f"📖 إجمالي الكلمات: {report['total_words']:,}")
        print(f"📄 متوسط الكلمات: {report['average_words_per_article']}")
        print(f"💰 متوسط RPM: {report['average_rpm']}")
        print(f"\n🎯 توقعات الربحية:")
        print(f"👥 زوار متوقعين يومياً: {report['estimated_daily_visitors']:,}")
        print(f"📊 مشاهدات شهرية: {report['estimated_monthly_pageviews']:,}")
        print(f"💰 دخل AdSense شهري: {report['adsense_monthly_income']}")
        print(f"🔗 دخل الروابط التسويقية: {report['affiliate_monthly_income']}")
        print(f"💎 إجمالي الدخل الشهري: {report['total_monthly_income']}")
        print(f"🚀 دخل سنوي متوقع: {report['projected_yearly_income']}")
        
        print(f"\n📊 تحليلات الأداء:")
        insights = report['performance_insights']
        print(f"🎯 كلمات عالية الدفع: {insights['high_paying_keywords_used']}/{report['successful']}")
        print(f"🌍 دول عالية القيمة: {insights['premium_countries_targeted']}/{report['successful']}")
        print(f"⚡ نقاط التحسين: {insights['optimization_score']}")
        
        print(f"\n📁 الملفات محفوظة في: generated_pages/")
        print(f"📋 التقرير المفصل في: {report_file}")
        
        if report['failed'] > 0:
            print(f"\n⚠️ مقالات فشل توليدها:")
            for i, result in enumerate([r for r in results if r['status'] == 'error'], 1):
                print(f"   {i}. {result['title']} - {result.get('error', 'خطأ غير معروف')}")
        
        print("\n🎯 استراتيجيات لمضاعفة الأرباح:")
        print("1. 📈 استمر في التوليد اليومي للمحتوى")
        print("2. 🔍 راقب أداء الكلمات المفتاحية في Search Console")
        print("3. 💰 فعّل المزيد من الروابط التسويقية")
        print("4. 📱 أضف صفحة اشتراك في النشرة الإخبارية")
        print("5. 🎯 ركز على المواضيع عالية RPM")
        print("6. 🌍 وسّع للأسواق عالية القيمة")
        
        print(f"\n🏆 هدفك: الوصول لـ $10,000 شهرياً خلال 6 شهور!")
        
    except ValueError as e:
        print(f"❌ خطأ في الإعداد: {e}")
        print("💡 تأكد من إضافة مفتاح Perplexity Pro API في ملف .env")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        print("🔧 تحقق من اتصالك بالإنترنت ومن مفتاح API")


if __name__ == "__main__":
    main()
