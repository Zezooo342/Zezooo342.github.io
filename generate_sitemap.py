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
        
        # تصنيف الصفحات وأولوياتها
        self.page_priorities = {
            'index.html': {'priority': '1.0', 'changefreq': 'daily'},
            'about.html': {'priority': '0.9', 'changefreq': 'monthly'},
            'contact.html': {'priority': '0.9', 'changefreq': 'monthly'},
            'articles.html': {'priority': '0.9', 'changefreq': 'weekly'},
            'privacy.html': {'priority': '0.8', 'changefreq': 'monthly'},
            
            # المحتوى المالي الأساسي
            'invest-arab.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'make-money-online.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'crypto-guide.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'management.html': {'priority': '0.8', 'changefreq': 'weekly'},
            'crypto-security.html': {'priority': '0.7', 'changefreq': 'weekly'},
            
            # الصفحات المهمة
            'ai.html': {'priority': '0.7', 'changefreq': 'weekly'},
            'article.html': {'priority': '0.7', 'changefreq': 'weekly'},
            'business-plan-simple.html': {'priority': '0.7', 'changefreq': 'weekly'},
            
            # الصفحات الثانوية
            'faq.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'team.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'reviews.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'media.html': {'priority': '0.6', 'changefreq': 'monthly'},
            'amp-article.html': {'priority': '0.5', 'changefreq': 'weekly'},
            
            # المحتوى العربي
            'طرق_ربح_المال_auto.html': {'priority': '0.7', 'changefreq': 'weekly'},
        }
        
        # الملفات المستثناة من sitemap
        # ملاحظة: يتم استبعاد '404.html' فقط لأن باقي الصفحات يجب أن تظهر في sitemap.
        # يتم إضافة عنوان الجذر '/' يدوياً في مكان آخر في الكود. يتم تضمين 'index.html' تلقائياً إذا لم يكن مستبعداً.
        self.excluded_files = ['404.html']

    def get_html_files(self):
        """الحصول على جميع ملفات HTML في الجذر"""
        html_files = []
        for file in glob.glob("*.html"):
            if file not in self.excluded_files:
                html_files.append(file)
        return sorted(html_files)

    def get_page_info(self, filename):
        """الحصول على معلومات الصفحة (الأولوية وتكرار التغيير)"""
        if filename in self.page_priorities:
            return self.page_priorities[filename]
        else:
            # القيم الافتراضية للمقالات والصفحات الأخرى
            return {'priority': '0.6', 'changefreq': 'monthly'}

    def url_encode_filename(self, filename):
        """ترميز أسماء الملفات للحروف الخاصة والعربية"""
        return urllib.parse.quote(filename, safe='/-_')

    def generate_sitemap(self):
        """توليد ملف sitemap.xml"""
        print("🔍 بدء فحص ملفات HTML...")
        
        # إنشاء عنصر جذر XML
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

        # إضافة الصفحة الرئيسية (/)
        url_element = ET.SubElement(urlset, 'url')
        ET.SubElement(url_element, 'loc').text = f"{self.base_url}/"
        ET.SubElement(url_element, 'lastmod').text = self.current_date
        ET.SubElement(url_element, 'changefreq').text = 'daily'
        ET.SubElement(url_element, 'priority').text = '1.0'

        # الحصول على جميع ملفات HTML
        html_files = self.get_html_files()
        print(f"📄 تم العثور على {len(html_files)} ملف HTML")

        # إضافة كل ملف HTML إلى sitemap
        for filename in html_files:
            page_info = self.get_page_info(filename)
            encoded_filename = self.url_encode_filename(filename)
            
            url_element = ET.SubElement(urlset, 'url')
            ET.SubElement(url_element, 'loc').text = f"{self.base_url}/{encoded_filename}"
            # استخدم وقت آخر تعديل فعلي للملف
            try:
                lastmod_date = datetime.fromtimestamp(os.path.getmtime(filename)).strftime('%Y-%m-%d')
            except FileNotFoundError:
                lastmod_date = self.current_date
            ET.SubElement(url_element, 'lastmod').text = lastmod_date
            ET.SubElement(url_element, 'changefreq').text = page_info['changefreq']
            ET.SubElement(url_element, 'priority').text = page_info['priority']
            
            print(f"✅ تمت إضافة: {filename} (أولوية: {page_info['priority']})")

        # كتابة XML إلى ملف
        tree = ET.ElementTree(urlset)
        
        # إضافة تنسيق جميل للـ XML
        self.indent(urlset)
        
        # كتابة الملف مع التصريح XML
        with open(self.output_file, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding='utf-8', xml_declaration=False)

        print(f"🎉 تم إنشاء {self.output_file} بنجاح!")
        print(f"📊 إجمالي الروابط: {len(html_files) + 1}")  # +1 للصفحة الرئيسية

    def indent(self, elem, level=0):
        """إضافة مسافات لتنسيق XML"""
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

    def validate_sitemap(self):
        """التحقق من صحة sitemap المولد"""
        if not os.path.exists(self.output_file):
            print("❌ خطأ: لم يتم إنشاء ملف sitemap")
            return False
            
        try:
            tree = ET.parse(self.output_file)
            root = tree.getroot()
            urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
            print(f"✅ تم التحقق من sitemap: {len(urls)} رابط")
            return True
        except ET.ParseError as e:
            print(f"❌ خطأ في تحليل XML: {e}")
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