#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت توليد sitemap.xml تلقائياً لموقع GitHub Pages
يقوم بفحص جميع ملفات HTML ويولد sitemap شامل مع أولويات مناسبة
"""

import os
import glob
import urllib.parse
from datetime import datetime
import xml.etree.ElementTree as ET


class SitemapGenerator:
    def __init__(self, base_url="https://zezooo342.github.io", output_file="sitemap.xml"):
        self.base_url = base_url.rstrip('/')
        self.output_file = output_file
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        
        # تصنيف الصفحات وأولوياتها مع تحسينات احترافية
        self.page_priorities = {
            # الصفحات الأساسية للموقع - أولوية عالية
            'index.html': {'priority': '1.0', 'changefreq': 'daily'},
            'about.html': {'priority': '0.9', 'changefreq': 'monthly'},
            'contact.html': {'priority': '0.9', 'changefreq': 'monthly'},
            'articles.html': {'priority': '0.9', 'changefreq': 'weekly'},
            
            # المحتوى المالي والاستثماري - أولوية عالية
            'invest-arab.html': {'priority': '0.9', 'changefreq': 'weekly'},
            'make-money-online.html': {'priority': '0.9', 'changefreq': 'weekly'},
            'crypto-guide.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'management.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'crypto-security.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'تداول_الأسهم.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'العملات_الرقمية.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'الاستثمار_في_مص.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'التسويق_بالعمول.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'مشاريع_صغيرة_لل.html': {'priority': '0.8', 'changefreq': 'weekly'},
            
            # الصفحات التقنية والذكاء الاصطناعي - أولوية متوسطة عالية
            'ai.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'article.html': {'priority': '0.7', 'changefreq': 'weekly'},
            'business-plan-simple.html': {'priority': '0.7', 'changefreq': 'weekly'},
            
            # الصفحات القانونية والمعلوماتية - أولوية متوسطة
            'privacy.html': {'priority': '0.7', 'changefreq': 'monthly'},
            'terms.html': {'priority': '0.7', 'changefreq': 'monthly'},
            'disclaimer.html': {'priority': '0.7', 'changefreq': 'monthly'},
            'faq.html': {'priority': '0.6', 'changefreq': 'monthly'},
            
            # الصفحات الثانوية
            'team.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'reviews.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'media.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'amp-article.html': {'priority': '0.5', 'changefreq': 'weekly'},
            
            # المحتوى العربي المتخصص - أولوية متوسطة عالية
            'طرق_ربح_المال_auto.html': {'priority': '0.8', 'changefreq': 'weekly'},
        }
        
        # تصنيفات المحتوى لتحديد الأولويات تلقائياً
        self.content_categories = {
            'high_priority_articles': {
                'keywords': ['AI_Tools', 'Top_10', 'CEO', 'profit', 'money', 'investment', 'crypto'],
                'priority': '0.8',
                'changefreq': 'weekly'
            },
            'business_articles': {
                'keywords': ['Business', 'CEO', 'Company', 'Startup', 'Management'],
                'priority': '0.7',
                'changefreq': 'weekly'
            },
            'tech_articles': {
                'keywords': ['AI', 'Tech', 'Data', 'System'],
                'priority': '0.7',
                'changefreq': 'weekly'
            },
            'general_articles': {
                'keywords': [],  # fallback for other articles
                'priority': '0.6',
                'changefreq': 'monthly'
            }
        }
        
        # الملفات المستثناة من sitemap
        self.excluded_files = ['404.html', 'index.html']  # استثناء index.html لأننا نضيف الصفحة الرئيسية يدوياً

    def get_html_files(self):
        """الحصول على جميع ملفات HTML في الجذر"""
        html_files = []
        for file in glob.glob("*.html"):
            if file not in self.excluded_files:
                html_files.append(file)
        return sorted(html_files)

    def get_page_info(self, filename):
        """الحصول على معلومات الصفحة مع تصنيف ذكي (الأولوية وتكرار التغيير)"""
        # إذا كان الملف مُعرَّف مسبقاً، استخدم تلك المعلومات
        if filename in self.page_priorities:
            return self.page_priorities[filename]
        
        # تصنيف ذكي للمقالات بناءً على المحتوى والاسم
        filename_lower = filename.lower()
        
        # فحص الكلمات المفتاحية للأولويات العالية
        for category, config in self.content_categories.items():
            if config['keywords']:  # تجنب الفئة العامة في هذه المرحلة
                for keyword in config['keywords']:
                    if keyword.lower() in filename_lower:
                        print(f"📊 تصنيف ذكي: {filename} -> فئة {category} (أولوية: {config['priority']})")
                        return {'priority': config['priority'], 'changefreq': config['changefreq']}
        
        # للملفات العربية، أعطها أولوية أعلى
        if any(ord(char) >= 0x0600 and ord(char) <= 0x06FF for char in filename):
            print(f"🔤 محتوى عربي: {filename} -> أولوية 0.7")
            return {'priority': '0.7', 'changefreq': 'weekly'}
        
        # القيم الافتراضية للمقالات والصفحات الأخرى
        return self.content_categories['general_articles']

    def url_encode_filename(self, filename):
        """ترميز أسماء الملفات للحروف الخاصة والعربية"""
        return urllib.parse.quote(filename, safe='/-_')

    def generate_sitemap(self):
        """توليد ملف sitemap.xml مع تحسينات احترافية"""
        print("🔍 بدء فحص ملفات HTML مع التصنيف الذكي...")
        
        # إنشاء عنصر جذر XML مع المعايير الصحيحة
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

        # إضافة الصفحة الرئيسية (/) - دائماً الأولوية القصوى
        print("🏠 إضافة الصفحة الرئيسية...")
        url_element = ET.SubElement(urlset, 'url')
        ET.SubElement(url_element, 'loc').text = f"{self.base_url}/"
        ET.SubElement(url_element, 'lastmod').text = self.current_date
        ET.SubElement(url_element, 'changefreq').text = 'daily'
        ET.SubElement(url_element, 'priority').text = '1.0'

        # الحصول على جميع ملفات HTML مع الفرز
        html_files = self.get_html_files()
        print(f"📄 تم العثور على {len(html_files)} ملف HTML")

        # تصنيف الملفات لإحصائيات أفضل
        priority_counts = {'1.0': 1, '0.9': 0, '0.8': 0, '0.7': 0, '0.6': 0, '0.5': 0}
        
        # إضافة كل ملف HTML إلى sitemap مع التصنيف المحسن
        for filename in html_files:
            page_info = self.get_page_info(filename)
            encoded_filename = self.url_encode_filename(filename)
            
            url_element = ET.SubElement(urlset, 'url')
            ET.SubElement(url_element, 'loc').text = f"{self.base_url}/{encoded_filename}"
            
            # استخدم وقت آخر تعديل فعلي للملف مع معالجة أفضل للأخطاء
            try:
                lastmod_date = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d')
                print(f"📅 تاريخ فعلي لـ {filename}: {lastmod_date}")
            except (OSError, FileNotFoundError) as e:
                lastmod_date = self.current_date
                print(f"⚠️  استخدام التاريخ الحالي لـ {filename}: {e}")
                
            ET.SubElement(url_element, 'lastmod').text = lastmod_date
            ET.SubElement(url_element, 'changefreq').text = page_info['changefreq']
            ET.SubElement(url_element, 'priority').text = page_info['priority']
            
            # تجميع إحصائيات الأولويات
            priority_counts[page_info['priority']] = priority_counts.get(page_info['priority'], 0) + 1
            
            print(f"✅ تمت إضافة: {filename} (أولوية: {page_info['priority']}, تحديث: {page_info['changefreq']})")

        # كتابة XML إلى ملف مع تحسينات التنسيق
        tree = ET.ElementTree(urlset)
        
        # إضافة تنسيق جميل ومنسق للـ XML
        self.indent(urlset)
        
        # كتابة الملف مع التصريح XML والترميز الصحيح
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                # تحويل إلى نص مع التنسيق الصحيح
                xml_string = ET.tostring(urlset, encoding='unicode')
                f.write(xml_string)
            
            print(f"🎉 تم إنشاء {self.output_file} بنجاح!")
            print(f"📊 إجمالي الروابط: {len(html_files) + 1}")  # +1 للصفحة الرئيسية
            
            # طباعة إحصائيات الأولويات
            print("\n📈 توزيع الأولويات:")
            for priority, count in sorted(priority_counts.items(), key=lambda x: float(x[0]), reverse=True):
                if count > 0:
                    print(f"   أولوية {priority}: {count} صفحة")
                    
        except Exception as e:
            print(f"❌ خطأ في كتابة الملف: {e}")
            raise

    def indent(self, elem, level=0):
        """إضافة مسافات لتنسيق XML مع ضمان تنسيق متسق"""
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self.indent(child, level+1)
            if not child.tail or not child.tail.strip():
                child.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
        # تنسيق العنصر الأخير
        if level == 0:
            elem.tail = "\n"

    def validate_sitemap(self):
        """التحقق المتقدم من صحة sitemap المولد"""
        print("\n🔍 بدء التحقق المتقدم من sitemap...")
        
        if not os.path.exists(self.output_file):
            print("❌ خطأ: لم يتم إنشاء ملف sitemap")
            return False
            
        try:
            # قراءة وتحليل XML
            tree = ET.parse(self.output_file)
            root = tree.getroot()
            
            # التحقق من namespace
            expected_ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
            if root.tag != f'{{{expected_ns}}}urlset':
                print(f"⚠️  تحذير: namespace غير متوقع في الجذر")
            
            urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            locs = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            
            print(f"✅ تم العثور على {len(urls)} URL في sitemap")
            print(f"✅ تم العثور على {len(locs)} عنصر loc")
            
            # التحقق من الأولويات والصيغة
            priorities = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}priority')
            priority_values = [float(p.text) for p in priorities if p.text]
            
            if priority_values:
                print(f"📊 نطاق الأولويات: {min(priority_values):.1f} - {max(priority_values):.1f}")
                
                # التحقق من وجود أولوية 1.0 للصفحة الرئيسية
                if 1.0 in priority_values:
                    print("✅ الصفحة الرئيسية لها أولوية 1.0")
                else:
                    print("⚠️  تحذير: لا توجد صفحة بأولوية 1.0")
            
            # التحقق من تواريخ آخر تعديل
            lastmods = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            if lastmods:
                print(f"✅ تم العثور على {len(lastmods)} تاريخ lastmod")
                # التحقق من صيغة التاريخ
                valid_dates = 0
                for lastmod in lastmods[:5]:  # فحص أول 5 فقط لتوفير الوقت
                    try:
                        datetime.strptime(lastmod.text, '%Y-%m-%d')
                        valid_dates += 1
                    except ValueError:
                        print(f"⚠️  تاريخ غير صحيح: {lastmod.text}")
                
                if valid_dates > 0:
                    print(f"✅ صيغة التواريخ صحيحة (تم فحص {valid_dates}/{min(5, len(lastmods))})")
            
            # التحقق من حجم الملف
            file_size = os.path.getsize(self.output_file)
            print(f"📏 حجم الملف: {file_size:,} بايت")
            
            if file_size > 50 * 1024 * 1024:  # 50MB حد Google
                print("⚠️  تحذير: حجم الملف كبير (أكثر من 50MB)")
            elif file_size > 10 * 1024 * 1024:  # 10MB تحذير مبكر
                print("⚠️  ملاحظة: حجم الملف كبير نسبياً (أكثر من 10MB)")
            else:
                print("✅ حجم الملف مناسب")
            
            # التحقق من الروابط المُكررة
            loc_texts = [loc.text for loc in locs]
            unique_locs = set(loc_texts)
            if len(loc_texts) != len(unique_locs):
                duplicates = len(loc_texts) - len(unique_locs)
                print(f"⚠️  تحذير: {duplicates} رابط مُكرر")
            else:
                print("✅ لا توجد روابط مُكررة")
            
            print(f"🎯 إجمالي النتيجة: sitemap صحيح مع {len(urls)} رابط")
            return True
            
        except ET.ParseError as e:
            print(f"❌ خطأ في تحليل XML: {e}")
            return False
        except Exception as e:
            print(f"❌ خطأ غير متوقع في التحقق: {e}")
            return False


def main():
    """الدالة الرئيسية"""
    print("🚀 مولد sitemap.xml للموقع")
    print("=" * 40)
    
    # إنشاء مولد sitemap
    generator = SitemapGenerator()
    
    # توليد sitemap
    generator.generate_sitemap()
    
    # التحقق من النتيجة
    if generator.validate_sitemap():
        print("\n✅ تم إنشاء sitemap.xml بنجاح!")
        print("🔗 يمكنك الآن رفع الملف إلى الموقع")
    else:
        print("\n❌ فشل في إنشاء sitemap صحيح")


if __name__ == "__main__":
    main()