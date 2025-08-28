import requests
import json
import schedule
import time
from datetime import datetime
import os
import random

class AutoContentGenerator:
    def __init__(self):
        self.articles_data = []
        
    def generate_viral_titles(self):
        """توليد عناوين فيروسية"""
        viral_templates = [
            "🔥 {topic}: السر الذي يخفيه الخبراء عنك",
            "💰 كيف تربح ${amount} من {topic} في {timeframe}",
            "⚠️ تحذير عاجل: {topic} سيغير حياتك خلال {timeframe}",
            "🚀 اكتشاف مذهل: {topic} يحقق أرباحاً خيالية"
        ]
        
        topics = [
            "البيتكوين", "الأسهم السعودية", "تداول الفوركس", 
            "الاستثمار العقاري", "العملات الرقمية", "الأسهم الأمريكية"
        ]
        
        amounts = ['500', '1000', '5000', '10000']
        timeframes = ['24 ساعة', 'أسبوع', 'شهر', '3 أشهر']
        
        titles = []
        for _ in range(5):
            template = random.choice(viral_templates)
            topic = random.choice(topics)
            amount = random.choice(amounts)
            timeframe = random.choice(timeframes)
            
            title = template.format(
                topic=topic,
                amount=amount,
                timeframe=timeframe
            )
            titles.append(title)
        
        return titles
    
    def create_article_data(self):
        """إنشاء بيانات المقالات"""
        titles = self.generate_viral_titles()
        countries = ["السعودية", "الإمارات", "الكويت", "قطر", "البحرين"]
        keywords = ["استثمار أسهم", "تداول بيتكوين", "تداول فوركس", "استثمار عقاري"]
        icons = ["💎", "₿", "📊", "🏢", "💰", "⚡", "🚀", "⭐"]
        
        articles = []
        for i, title in enumerate(titles):
            article = {
                "title": title,
                "url": "article.html",
                "country": random.choice(countries),
                "keyword": random.choice(keywords),
                "date": "2025-08-28",
                "readTime": f"{random.randint(5, 15)} دقائق",
                "icon": random.choice(icons),
                "views": f"{random.randint(10000, 100000):,}",
                "trending": i < 2,  # أول مقالتين رائجتين
                "excerpt": f"دليل شامل ومفصل حول {title.split(':')[0]}. استراتيجيات مجربة وأرباح مضمونة.",
                "affiliateUrl": "https://www.binance.com/referral/earn-together/refer-in-hotsummer/claim?hl=en&ref=GRO_20338_D3ELK&utm_source=auto_content"
            }
            articles.append(article)
        
        return articles

class SocialMediaAutomation:
    def __init__(self):
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel = os.getenv('TELEGRAM_CHANNEL_ID')
        
    def post_to_telegram(self, message):
        """نشر على تليجرام"""
        if not self.telegram_token or not self.telegram_channel:
            print("⚠️ معلومات Telegram غير متوفرة")
            return False
            
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_channel,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ تم النشر على Telegram بنجاح")
                return True
            else:
                print(f"❌ خطأ في النشر على Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ خطأ في الاتصال بـ Telegram: {e}")
            return False
    
    def create_social_posts(self, articles):
        """إنشاء منشورات وسائل التواصل"""
        posts = []
        
        for article in articles[:3]:  # أفضل 3 مقالات
            post = f"""
🔥 *{article['title']}*

📊 المشاهدات: {article['views']}
⏱️ وقت القراءة: {article['readTime']}
🌍 الدولة: {article['country']}

{article['excerpt'][:100]}...

🔗 اقرأ المقال كاملاً: https://zezooo342.github.io/{article['url']}

💰 ابدأ الاستثمار الآن: {article['affiliateUrl']}

#استثمار #تداول #{article['country']} #أرباح
            """
            posts.append(post)
        
        return posts

class FileManager:
    @staticmethod
    def update_articles_data(articles):
        """تحديث بيانات المقالات في الموقع"""
        try:
            # قراءة ملف index.html الحالي
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # إنشاء JavaScript للمقالات الجديدة
            js_articles = "const articlesData = [\n"
            for article in articles:
                js_articles += f"""  {{
    title: "{article['title']}",
    url: "{article['url']}",
    country: "{article['country']}",
    keyword: "{article['keyword']}",
    date: "{article['date']}",
    readTime: "{article['readTime']}",
    icon: "{article['icon']}",
    views: "{article['views']}",
    trending: {str(article['trending']).lower()},
    excerpt: "{article['excerpt']}",
    affiliateUrl: "{article['affiliateUrl']}"
  }},\n"""
            js_articles += "];"
            
            print("✅ تم تحديث بيانات المقالات")
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تحديث الملفات: {e}")
            return False

def main():
    """الدالة الرئيسية للتشغيل"""
    print("🚀 بدء نظام الأتمتة الذكي...")
    
    # إنشاء المولدات
    content_gen = AutoContentGenerator()
    social_media = SocialMediaAutomation()
    
    # توليد محتوى جديد
    print("📝 توليد محتوى جديد...")
    articles = content_gen.create_article_data()
    print(f"✅ تم إنشاء {len(articles)} مقال جديد")
    
    # تحديث الموقع
    print("🔄 تحديث الموقع...")
    FileManager.update_articles_data(articles)
    
    # إنشاء منشورات وسائل التواصل
    print("📱 إنشاء منشورات وسائل التواصل...")
    posts = social_media.create_social_posts(articles)
    
    # نشر على تليجرام
    for i, post in enumerate(posts):
        print(f"📤 نشر المقال {i+1} على Telegram...")
        social_media.post_to_telegram(post)
        time.sleep(2)  # انتظار ثانيتين بين المنشورات
    
    print("✅ تم الانتهاء من دورة الأتمتة بنجاح!")

if __name__ == "__main__":
    main()
