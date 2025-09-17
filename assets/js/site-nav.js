/**
 * Site Navigation JavaScript
 * Handles global navigation and footer injection for non-AMP pages
 * RTL-friendly design for Arabic content
 */

(function() {
    'use strict';
    
    // Skip if this is an AMP page
    if (document.documentElement.hasAttribute('⚡') || 
        document.documentElement.hasAttribute('amp')) {
        return;
    }
    
    let siteIndex = null;
    
    // Fetch site index
    async function fetchSiteIndex() {
        try {
            const response = await fetch('/assets/site-index.json');
            if (!response.ok) throw new Error('Failed to fetch site index');
            siteIndex = await response.json();
            return siteIndex;
        } catch (error) {
            console.warn('Could not load site index:', error);
            return null;
        }
    }
    
    // Get current page path for active link highlighting
    function getCurrentPath() {
        let path = window.location.pathname;
        if (path === '/') path = '/index.html';
        if (!path.endsWith('.html')) path += '.html';
        return path;
    }
    
    // Create navigation HTML
    function createNavigation(pages) {
        if (!pages) return '';
        
        const currentPath = getCurrentPath();
        const mainPages = pages.filter(page => 
            ['main', 'financial', 'info'].includes(page.category)
        ).slice(0, 8); // Limit to 8 main navigation items
        
        return mainPages.map(page => {
            const isActive = page.path === currentPath ? ' class="active"' : '';
            const href = page.path.replace(/^\//, '');
            return `<a href="${href}"${isActive}>${page.title}</a>`;
        }).join('');
    }
    
    // Create footer navigation HTML
    function createFooterNavigation(pages) {
        if (!pages) return '';
        
        const footerPages = pages.filter(page => 
            !['social'].includes(page.category)
        );
        
        return footerPages.map(page => {
            const href = page.path.replace(/^\//, '');
            return `<li><a href="${href}">${page.title}</a></li>`;
        }).join('');
    }
    
    // Inject header navigation
    function injectHeader() {
        const headerElement = document.getElementById('site-header');
        if (!headerElement) return;
        
        const navHTML = siteIndex ? 
            createNavigation(siteIndex.pages) : 
            `<a href="index.html">الرئيسية</a>
             <a href="articles.html">المقالات</a>
             <a href="about.html">من نحن</a>
             <a href="contact.html">تواصل معنا</a>`;
        
        headerElement.innerHTML = `<nav>${navHTML}</nav>`;
    }
    
    // Inject footer
    function injectFooter() {
        const footerElement = document.getElementById('site-footer');
        if (!footerElement) return;
        
        const footerNavHTML = siteIndex ? 
            createFooterNavigation(siteIndex.pages) : 
            `<li><a href="index.html">الرئيسية</a></li>
             <li><a href="articles.html">المقالات</a></li>
             <li><a href="about.html">من نحن</a></li>
             <li><a href="contact.html">تواصل معنا</a></li>
             <li><a href="privacy.html">سياسة الخصوصية</a></li>`;
        
        footerElement.innerHTML = `
            <div class="footer-content">
                <nav>
                    <ul>${footerNavHTML}</ul>
                </nav>
                <div class="copyright">
                    جميع الحقوق محفوظة &copy; دليل المال العربي ${new Date().getFullYear()}
                </div>
            </div>
        `;
    }
    
    // Create related articles section
    function createRelatedArticles() {
        if (!siteIndex) return;
        
        const currentPath = getCurrentPath();
        const currentPage = siteIndex.pages.find(page => page.path === currentPath);
        if (!currentPage) return;
        
        // Get related articles from same category or popular pages
        let relatedPages = siteIndex.pages.filter(page => 
            page.path !== currentPath && 
            (page.category === currentPage.category || page.priority >= 0.8)
        ).slice(0, 5);
        
        // If not enough related, add some high-priority pages
        if (relatedPages.length < 3) {
            const additionalPages = siteIndex.pages
                .filter(page => page.path !== currentPath && !relatedPages.includes(page))
                .sort((a, b) => b.priority - a.priority)
                .slice(0, 5 - relatedPages.length);
            relatedPages = [...relatedPages, ...additionalPages];
        }
        
        if (relatedPages.length === 0) return;
        
        const relatedHTML = `
            <div class="related-articles">
                <h3>مقالات ذات صلة</h3>
                <ul>
                    ${relatedPages.map(page => {
                        const href = page.path.replace(/^\//, '');
                        return `<li><a href="${href}">${page.title}</a></li>`;
                    }).join('')}
                </ul>
            </div>
        `;
        
        // Find main content area and append related articles
        const mainContent = document.querySelector('main, .container, .main, article') ||
                           document.querySelector('body > div:last-of-type');
        
        if (mainContent) {
            mainContent.insertAdjacentHTML('beforeend', relatedHTML);
        }
    }
    
    // Check if page seems to be article-like
    function isArticlePage() {
        const currentPath = getCurrentPath();
        return currentPath.includes('article') || 
               currentPath.includes('crypto') || 
               currentPath.includes('invest') || 
               currentPath.includes('money') || 
               currentPath.includes('business') ||
               currentPath.includes('management') ||
               document.querySelector('article, [data-ld-article]') !== null;
    }
    
    // Initialize navigation
    async function init() {
        try {
            await fetchSiteIndex();
            injectHeader();
            injectFooter();
            
            // Add related articles for article-like pages
            if (isArticlePage()) {
                createRelatedArticles();
            }
        } catch (error) {
            console.warn('Navigation initialization failed:', error);
            // Fallback: still inject basic navigation
            injectHeader();
            injectFooter();
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for manual use
    window.SiteNav = {
        init: init,
        injectHeader: injectHeader,
        injectFooter: injectFooter,
        createRelatedArticles: createRelatedArticles
    };
    
})();