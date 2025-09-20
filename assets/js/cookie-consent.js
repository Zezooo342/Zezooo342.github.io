// Cookie Consent Bar - Arabic RTL Version
(function() {
    'use strict';
    
    // Check if consent already given
    if (localStorage.getItem('cookieConsent') === 'accepted') {
        return;
    }
    
    // Create cookie consent bar
    function createCookieBar() {
        const cookieBar = document.createElement('div');
        cookieBar.id = 'cookie-consent-bar';
        cookieBar.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #2e4057;
            color: #fff;
            padding: 15px 20px;
            font-family: 'Tajawal', 'Cairo', Arial, sans-serif;
            font-size: 14px;
            line-height: 1.4;
            z-index: 9999;
            direction: rtl;
            text-align: right;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.2);
            border-top: 3px solid #076e4d;
        `;
        
        const content = document.createElement('div');
        content.style.cssText = `
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
        `;
        
        const message = document.createElement('div');
        message.style.cssText = `
            flex: 1;
            min-width: 200px;
        `;
        message.innerHTML = `
            <span style="font-weight: 600; color: #f0f8f4;">🍪 نحن نستخدم ملفات تعريف الارتباط</span>
            <br>
            نستخدم الكوكيز لتحسين تجربتك وعرض إعلانات مخصصة. بالمتابعة، توافق على استخدامها.
            <a href="/privacy.html" style="color: #76c7a3; text-decoration: underline; margin-right: 5px;">سياسة الخصوصية</a>
        `;
        
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: flex;
            gap: 10px;
            align-items: center;
        `;
        
        const acceptBtn = document.createElement('button');
        acceptBtn.textContent = '✓ موافق';
        acceptBtn.style.cssText = `
            background: #076e4d;
            color: #fff;
            border: none;
            padding: 8px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Tajawal', 'Cairo', Arial, sans-serif;
            font-size: 14px;
            font-weight: 600;
            transition: background 0.3s ease;
        `;
        
        const declineBtn = document.createElement('button');
        declineBtn.textContent = '✕ رفض';
        declineBtn.style.cssText = `
            background: transparent;
            color: #ccc;
            border: 1px solid #555;
            padding: 8px 16px;
            border-radius: 5px;
            cursor: pointer;
            font-family: 'Tajawal', 'Cairo', Arial, sans-serif;
            font-size: 14px;
            transition: all 0.3s ease;
        `;
        
        // Hover effects
        acceptBtn.onmouseover = () => acceptBtn.style.background = '#0a8f63';
        acceptBtn.onmouseout = () => acceptBtn.style.background = '#076e4d';
        
        declineBtn.onmouseover = () => {
            declineBtn.style.background = '#444';
            declineBtn.style.color = '#fff';
        };
        declineBtn.onmouseout = () => {
            declineBtn.style.background = 'transparent';
            declineBtn.style.color = '#ccc';
        };
        
        // Event handlers
        acceptBtn.onclick = function() {
            localStorage.setItem('cookieConsent', 'accepted');
            localStorage.setItem('cookieConsentDate', new Date().toISOString());
            removeCookieBar();
        };
        
        declineBtn.onclick = function() {
            localStorage.setItem('cookieConsent', 'declined');
            localStorage.setItem('cookieConsentDate', new Date().toISOString());
            removeCookieBar();
        };
        
        // Mobile responsive adjustments
        if (window.innerWidth <= 768) {
            content.style.flexDirection = 'column';
            content.style.textAlign = 'center';
            message.style.marginBottom = '10px';
        }
        
        buttonContainer.appendChild(acceptBtn);
        buttonContainer.appendChild(declineBtn);
        content.appendChild(message);
        content.appendChild(buttonContainer);
        cookieBar.appendChild(content);
        
        return cookieBar;
    }
    
    function removeCookieBar() {
        const bar = document.getElementById('cookie-consent-bar');
        if (bar) {
            bar.style.transition = 'transform 0.5s ease-out, opacity 0.5s ease-out';
            bar.style.transform = 'translateY(100%)';
            bar.style.opacity = '0';
            setTimeout(() => bar.remove(), 500);
        }
    }
    
    // Show cookie bar when DOM is ready
    function initCookieConsent() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', showCookieBar);
        } else {
            showCookieBar();
        }
    }
    
    function showCookieBar() {
        // Wait a bit for page to load completely
        setTimeout(() => {
            const cookieBar = createCookieBar();
            document.body.appendChild(cookieBar);
            
            // Animate in
            setTimeout(() => {
                cookieBar.style.transition = 'transform 0.5s ease-out';
                cookieBar.style.transform = 'translateY(0)';
            }, 100);
        }, 1000);
    }
    
    // Initialize
    initCookieConsent();
    
    // Handle window resize for mobile responsive
    window.addEventListener('resize', function() {
        const cookieBar = document.getElementById('cookie-consent-bar');
        if (cookieBar) {
            const content = cookieBar.querySelector('div');
            if (window.innerWidth <= 768) {
                content.style.flexDirection = 'column';
                content.style.textAlign = 'center';
            } else {
                content.style.flexDirection = 'row';
                content.style.textAlign = 'right';
            }
        }
    });
    
})();