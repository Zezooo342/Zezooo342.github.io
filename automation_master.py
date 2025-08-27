import requests
import json
import schedule
import time
from datetime import datetime
import tweepy
import facebook

class SocialMediaAutomation:
    def __init__(self):
        self.setup_apis()
        
    def setup_apis(self):
        """إعداد APIs لوسائل التواصل"""
        # Twitter API (مجاني)
        self.twitter_api = tweepy.API(
            tweepy.OAuth1UserHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET'),
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_SECRET')
            )
        )
        
        # Telegram Bot (مجاني)
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_channel = os.getenv('TELEGRAM_CHANNEL_ID')
        
    def auto_post_to_twitter(self, content):
        """نشر تلقائي على تويتر"""
        try:
            # تقسيم المحتوى لخيوط تويتر
            tweets = self.split_content_for_twitter(content)
            
            last_tweet = None
            for tweet_text in tweets:
                if last_tweet:
                    tweet = self.twitter_api.update_status(
                        tweet_text, 
                        in_reply_to_status_id=last_tweet.id
                    )
                else:
                    tweet = self.twitter_api.update_status(tweet_text)
                last_tweet = tweet
                time.sleep(5)  # تجنب Rate Limiting
                
            return True
        except Exception as e:
            print(f"خطأ في النشر على تويتر: {e}")
            return False
    
    def auto_post_to_telegram(self, content):
        """نشر تلقائي على تليجرام"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            payload = {
                'chat_id': self.telegram_channel,
                'text': content,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"خطأ في النشر على تليجرام: {e}")
            return False
    
    def auto_engage_with_trending(self):
        """تفاعل تلقائي مع المحتوى الرائج"""
        try:
            # البحث عن تويتات رائجة بكلمات مفتاحية
            trending_keywords = ['استثمار', 'بيتكوين', 'أسهم', 'تداول']
            
            for keyword in trending_keywords:
                tweets = tweepy.Cursor(
                    self.twitter_api.search_tweets,
                    q=keyword,
                    lang='ar',
                    result_type='popular'
                ).items(5)
                
                for tweet in tweets:
                    # إعجاب + إعادة تغريد + تعليق ذكي
                    self.twitter_api.create_favorite(tweet.id)
                    self.twitter_api.retweet(tweet.id)
                    
                    smart_reply = self.generate_smart_reply(tweet.text)
                    self.twitter_api.update_status(
                        smart_reply,
                        in_reply_to_status_id=tweet.id
                    )
                    
                    time.sleep(60)  # دقيقة بين كل تفاعل
                    
        except Exception as e:
            print(f"خطأ في التفاعل: {e}")

class IntelligentScheduler:
    def __init__(self):
        self.content_generator = AutoContentGenerator()
        self.social_media = SocialMediaAutomation()
        
    def schedule_smart_posting(self):
        """جدولة ذكية للنشر"""
        
        # أوقات مثلى للنشر (بناءً على الإحصائيات)
        optimal_times = [
            "08:00",  # صباح العمل
            "12:30",  # استراحة الغداء
            "18:00",  # نهاية العمل
            "21:00"   # وقت الراحة
        ]
        
        for time_slot in optimal_times:
            schedule.every().day.at(time_slot).do(self.execute_smart_posting)
        
        # نشر أسبوعي مكثف
        schedule.every().sunday.at("10:00").do(self.weekly_content_blast)
        
        # تحليل شهري وتحسين
        schedule.every().month.do(self.monthly_optimization)
        
    def execute_smart_posting(self):
        """تنفيذ النشر الذكي"""
        # توليد محتوى جديد
        articles = self.content_generator.generate_daily_content(1)
        article = articles[0]
        
        # إنشاء منشورات متنوعة
        twitter_post = self.create_twitter_version(article)
        telegram_post = self.create_telegram_version(article)
        
        # نشر تلقائي
        self.social_media.auto_post_to_twitter(twitter_post)
        self.social_media.auto_post_to_telegram(telegram_post)
        
        # تحديث الموقع
        self.update_website_content(article)
        
    def create_twitter_version(self, article):
        """إنشاء نسخة تويتر مُحسّنة"""
        
        twitter_templates = [
            f"🔥 {article['title']}\n\n💡 نصيحة سريعة:\n{self.extract_quick_tip(article)}\n\n🔗 التفاصيل الكاملة:",
            f"⚡ عاجل: {article['title']}\n\n📊 الإحصائيات تقول:\n- نمو 25% هذا الشهر\n- فرصة استثمارية نادرة\n\n🎯 اقرأ التحليل الكامل:",
            f"💰 سر الاستثمار الذكي:\n{article['title']}\n\n✅ مجرب وآمن\n✅ نتائج سريعة\n✅ مناسب للمبتدئين\n\n📖 الدليل الشامل:"
        ]
        
        return random.choice(twitter_templates)
