// دليل المال العربي - Main JavaScript
// تحديث السنة الحالية في الفوتر

document.addEventListener('DOMContentLoaded', function() {
    // تحديث السنة الحالية
    updateCurrentYear();
    
    // إضافة تفاعل للقائمة (إذا لزم الأمر في المستقبل)
    initializeMenuToggle();
});

/**
 * تحديث السنة الحالية في الفوتر
 */
function updateCurrentYear() {
    const currentYear = new Date().getFullYear();
    const yearElements = document.querySelectorAll('.current-year');
    
    yearElements.forEach(element => {
        element.textContent = currentYear;
    });
    
    // تحديث النص الثابت إذا وُجد
    const copyrightElements = document.querySelectorAll('footer div, .copyright');
    copyrightElements.forEach(element => {
        if (element.textContent && element.textContent.includes('2025')) {
            element.textContent = element.textContent.replace('2025', currentYear);
        }
    });
}

/**
 * إعداد قائمة متجاوبة للأجهزة المحمولة
 */
function initializeMenuToggle() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    
    // إضافة زر القائمة للأجهزة المحمولة (إذا لزم الأمر)
    const navUl = nav.querySelector('ul');
    if (navUl && window.innerWidth <= 768) {
        // يمكن إضافة المزيد من التفاعل هنا حسب الحاجة
    }
}

/**
 * تحسين أداء التحميل للإعلانات
 */
function optimizeAdLoading() {
    // تأخير تحميل الإعلانات قليلاً لتحسين الأداء
    if (typeof adsbygoogle !== 'undefined') {
        setTimeout(() => {
            try {
                (adsbygoogle = window.adsbygoogle || []).push({});
            } catch (e) {
                console.log('AdSense not ready yet');
            }
        }, 1000);
    }
}

// تصدير الوظائف للاستخدام في صفحات أخرى إذا لزم الأمر
window.ArabMoneyGuide = {
    updateCurrentYear: updateCurrentYear,
    initializeMenuToggle: initializeMenuToggle
};