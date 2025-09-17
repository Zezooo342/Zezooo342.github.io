# دليل استخدام الصور - موقع دليل المال العربي

## وصف الصور المطلوبة

### 1. banner-finance.jpg - لافتة المالية
**الوصف:** صورة مكتب مالي احترافي مع أجواء عربية أو شرق أوسطية
**الاستخدام:** الصفحة الرئيسية، أقسام الخدمات المالية
**الأبعاد المقترحة:** 1920x1080px أو 1200x630px للمشاركة الاجتماعية
**رابط التحميل:** https://unsplash.com/photos/person-using-laptop-computer-holding-card-5QgIuuBxKwM
**رابط بديل:** https://unsplash.com/photos/person-holding-pencil-near-laptop-computer-nP1L2f3oNE0

### 2. invest-business.jpg - الاستثمار والأعمال
**الوصف:** صورة تُظهر استثمار وأعمال، مثل رسوم بيانية، عملات، أو محفظة استثمارية
**الاستخدام:** صفحة دليل الاستثمار، المقالات المالية
**الأبعاد المقترحة:** 1200x800px
**رابط التحميل:** https://unsplash.com/photos/silver-and-gold-coins-OHOU-5UVIYQ
**رابط بديل:** https://unsplash.com/photos/person-holding-fan-of-u-s-dollars-banknote-ZihPQeQR2wM

### 3. learn-arabic-finance.jpg - تعليم مالي عربي
**الوصف:** صورة تعليمية تُظهر التعلم المالي، مثل كتب، حاسوب، أو دورة تدريبية
**الاستخدام:** صفحات المقالات التعليمية، أقسام التعلم
**الأبعاد المقترحة:** 1200x800px
**رابط التحميل:** https://unsplash.com/photos/person-reading-a-book-beside-white-ceramic-teacup-on-white-table-SgRNgAeLQ7I
**رابط بديل:** https://unsplash.com/photos/black-framed-eyeglasses-on-white-book-page-fb7yNPbT0l8

### 4. crypto-money.jpg - العملات الرقمية
**الوصف:** صورة متعلقة بالعملات الرقمية، البيتكوين، أو التداول الرقمي
**الاستخدام:** صفحة دليل العملات الرقمية، مقالات الكريبتو
**الأبعاد المقترحة:** 1200x800px
**رابط التحميل:** https://unsplash.com/photos/gold-bitcoin-coin-on-white-background-n-Jnmi1Y0I
**رابط بديل:** https://unsplash.com/photos/gold-bitcoin-RJdp1pXAK2o

### 5. team-arabic.jpg - فريق عربي
**الوصف:** صورة فريق عمل عربي أو شرق أوسطي احترافي في بيئة عمل
**الاستخدام:** صفحة "من نحن"، قسم الفريق
**الأبعاد المقترحة:** 1200x800px
**رابط التحميل:** https://unsplash.com/photos/people-sitting-on-chair-in-front-of-computer-3184360
**رابط بديل:** https://unsplash.com/photos/group-of-people-sitting-indoors-Q7ReFXpHNHE

## أمثلة أكواد HTML لاستخدام الصور

### استخدام كصورة عادية:
```html
<img src="/assets/images/banner-finance.jpg" alt="مكتب مالي احترافي" 
     style="width: 100%; max-width: 1200px; height: auto;">
```

### استخدام كخلفية قسم:
```html
<section style="background-image: url('/assets/images/invest-business.jpg'); 
                background-size: cover; background-position: center;">
  <div class="content">
    <!-- محتوى القسم -->
  </div>
</section>
```

### استخدام في البيانات المهيكلة:
```html
<div data-ld-article 
     data-headline="عنوان المقال" 
     data-description="وصف المقال"
     data-image="assets/images/learn-arabic-finance.jpg">
</div>
```

### استخدام في Meta Tags للمشاركة الاجتماعية:
```html
<meta property="og:image" content="https://zezooo342.github.io/assets/images/banner-finance.jpg"/>
<meta name="twitter:image" content="https://zezooo342.github.io/assets/images/banner-finance.jpg">
```

### استخدام مع CSS لخلفية متجاوبة:
```css
.hero-banner {
  background-image: url('/assets/images/banner-finance.jpg');
  background-size: cover;
  background-position: center;
  height: 400px;
}

@media (max-width: 768px) {
  .hero-banner {
    height: 250px;
  }
}
```

## ملاحظات مهمة

1. **الأبعاد:** تأكد من أن الصور محسنة للويب (أقل من 500KB لكل صورة)
2. **التنسيق:** استخدم JPEG للصور الفوتوغرافية، PNG للشعارات والرسوم
3. **النص البديل:** أضف دائماً وصف مناسب في خاصية alt للصور
4. **التحسين:** استخدم أدوات ضغط الصور قبل الرفع
5. **الحقوق:** جميع الروابط المقترحة من Unsplash تحت رخصة مجانية للاستخدام التجاري

## رخصة الاستخدام

الصور المقترحة من Unsplash متاحة تحت رخصة Unsplash License التي تسمح بالاستخدام المجاني للأغراض التجارية وغير التجارية.
رابط الرخصة: https://unsplash.com/license