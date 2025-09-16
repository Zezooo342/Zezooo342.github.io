/**
 * Site Navigation and Related Articles System
 * Fetches site index and injects navigation and related content
 */

(function() {
    'use strict';
    
    let siteData = null;
    
    // Configuration
    const config = {
        siteIndexUrl: '/assets/site-index.json',
        maxRelatedArticles: 5,
        enableActiveHighlight: true
    };
    
    /**
     * Fetch site index data
     */
    async function fetchSiteIndex() {
        try {
            const response = await fetch(config.siteIndexUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            siteData = await response.json();
            return siteData;
        } catch (error) {
            console.warn('Could not load site index:', error);
            return null;
        }
    }
    
    /**
     * Get current page URL path
     */
    function getCurrentPagePath() {
        return window.location.pathname;
    }
    
    /**
     * Find current page data
     */
    function getCurrentPageData() {
        if (!siteData) return null;
        const currentPath = getCurrentPagePath();
        return siteData.pages.find(page => 
            page.url === currentPath || 
            page.url === currentPath.replace(/\/$/, '') ||
            page.url === currentPath + '.html' ||
            page.url === '/' + currentPath.split('/').pop()
        );
    }
    
    /**
     * Create navigation HTML
     */
    function createNavigation() {
        if (!siteData) return '';
        
        const navPages = siteData.pages.filter(page => page.nav === true);
        const currentPath = getCurrentPagePath();
        
        let navHTML = '<nav id="main-nav" class="site-nav">';
        navHTML += '<ul class="nav-list">';
        
        navPages.forEach(page => {
            const isActive = page.url === currentPath || 
                           page.url === currentPath.replace(/\/$/, '') ||
                           page.url === '/' + currentPath.split('/').pop();
            const activeClass = isActive && config.enableActiveHighlight ? ' class="active"' : '';
            const encodedUrl = encodeURI(page.url);
            
            navHTML += `<li><a href="${encodedUrl}"${activeClass}>${page.displayTitle}</a></li>`;
        });
        
        navHTML += '</ul>';
        navHTML += '</nav>';
        
        return navHTML;
    }
    
    /**
     * Create footer HTML
     */
    function createFooter() {
        if (!siteData) return '';
        
        const footerPages = siteData.navigation.footer.map(url => 
            siteData.pages.find(page => page.url === url)
        ).filter(Boolean);
        
        let footerHTML = '<div class="site-footer-content">';
        footerHTML += '<ul class="footer-links">';
        
        footerPages.forEach(page => {
            const encodedUrl = encodeURI(page.url);
            footerHTML += `<li><a href="${encodedUrl}">${page.displayTitle}</a></li>`;
        });
        
        footerHTML += '</ul>';
        footerHTML += '<div class="footer-copyright">';
        footerHTML += 'جميع الحقوق محفوظة &copy; دليل المال العربي 2025';
        footerHTML += '</div>';
        footerHTML += '</div>';
        
        return footerHTML;
    }
    
    /**
     * Get related articles for current page
     */
    function getRelatedArticles() {
        if (!siteData) return [];
        
        const currentPage = getCurrentPageData();
        if (!currentPage) return [];
        
        let relatedPages = [];
        
        // Use predefined related pages if available
        if (currentPage.relatedPages && currentPage.relatedPages.length > 0) {
            relatedPages = currentPage.relatedPages.map(url => 
                siteData.pages.find(page => page.url === url)
            ).filter(Boolean);
        }
        
        // If not enough related pages, add pages from same category
        if (relatedPages.length < config.maxRelatedArticles) {
            const sameCategoryPages = siteData.pages.filter(page => 
                page.category === currentPage.category && 
                page.url !== currentPage.url &&
                !relatedPages.some(related => related.url === page.url)
            );
            relatedPages = relatedPages.concat(sameCategoryPages);
        }
        
        // If still not enough, add high priority pages
        if (relatedPages.length < config.maxRelatedArticles) {
            const highPriorityPages = siteData.pages.filter(page => 
                page.priority >= 0.8 && 
                page.url !== currentPage.url &&
                !relatedPages.some(related => related.url === page.url)
            );
            relatedPages = relatedPages.concat(highPriorityPages);
        }
        
        return relatedPages.slice(0, config.maxRelatedArticles);
    }
    
    /**
     * Create related articles HTML
     */
    function createRelatedArticles() {
        const relatedPages = getRelatedArticles();
        if (relatedPages.length === 0) return '';
        
        let relatedHTML = '<section class="related-articles" id="related-articles">';
        relatedHTML += '<h3>مقالات ذات صلة</h3>';
        relatedHTML += '<div class="related-grid">';
        
        relatedPages.forEach(page => {
            const encodedUrl = encodeURI(page.url);
            relatedHTML += `
                <div class="related-item">
                    <h4><a href="${encodedUrl}">${page.displayTitle}</a></h4>
                    <p class="related-description">${page.description || ''}</p>
                    <a href="${encodedUrl}" class="related-link">اقرأ المزيد &larr;</a>
                </div>
            `;
        });
        
        relatedHTML += '</div>';
        relatedHTML += '</section>';
        
        return relatedHTML;
    }
    
    /**
     * Inject navigation into header placeholder
     */
    function injectNavigation() {
        const headerElement = document.getElementById('site-header');
        if (headerElement) {
            headerElement.innerHTML = createNavigation();
        }
    }
    
    /**
     * Inject footer into footer placeholder
     */
    function injectFooter() {
        const footerElement = document.getElementById('site-footer');
        if (footerElement) {
            footerElement.innerHTML = createFooter();
        }
    }
    
    /**
     * Inject related articles before footer or at end of main content
     */
    function injectRelatedArticles() {
        // Skip if page has data-no-related attribute
        if (document.body.dataset.noRelated !== undefined) {
            return;
        }
        
        const relatedHTML = createRelatedArticles();
        if (!relatedHTML) return;
        
        // Try to insert before footer
        const footerElement = document.getElementById('site-footer') || 
                             document.querySelector('footer') ||
                             document.querySelector('.footer');
        
        if (footerElement) {
            footerElement.insertAdjacentHTML('beforebegin', relatedHTML);
        } else {
            // Fallback: append to body or main content area
            const mainContent = document.querySelector('main') || 
                              document.querySelector('.main') || 
                              document.querySelector('.container') ||
                              document.body;
            
            if (mainContent) {
                mainContent.insertAdjacentHTML('beforeend', relatedHTML);
            }
        }
    }
    
    /**
     * Add basic navigation styles if not present
     */
    function addBasicStyles() {
        // Check if navigation styles already exist
        if (document.querySelector('style[data-site-nav]') || 
            document.querySelector('link[href*="nav.css"]')) {
            return;
        }
        
        const style = document.createElement('style');
        style.setAttribute('data-site-nav', 'true');
        style.textContent = `
            /* Site Navigation Styles */
            .site-nav {
                background: #334756;
                padding: 12px 0;
                text-align: center;
                margin: 0;
            }
            
            .nav-list {
                list-style: none;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 1em;
            }
            
            .nav-list li {
                margin: 0;
            }
            
            .nav-list a {
                color: #fff;
                text-decoration: none;
                font-weight: 500;
                padding: 8px 12px;
                border-radius: 4px;
                transition: background-color 0.3s ease;
                font-size: 16px;
            }
            
            .nav-list a:hover,
            .nav-list a.active {
                background-color: rgba(255, 255, 255, 0.1);
                text-decoration: none;
            }
            
            .nav-list a.active {
                background-color: rgba(59, 178, 115, 0.8);
            }
            
            /* Footer Styles */
            .site-footer-content {
                background: #076e4d;
                color: #fff;
                padding: 1.5em 0;
                text-align: center;
            }
            
            .footer-links {
                list-style: none;
                display: flex;
                justify-content: center;
                gap: 1.5em;
                margin: 0 0 1em 0;
                padding: 0;
                flex-wrap: wrap;
            }
            
            .footer-links a {
                color: #fff;
                text-decoration: none;
                font-weight: 500;
            }
            
            .footer-links a:hover {
                text-decoration: underline;
            }
            
            .footer-copyright {
                margin-top: 1em;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            /* Related Articles Styles */
            .related-articles {
                margin: 2em 0;
                padding: 1.5em;
                background: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e9ecef;
            }
            
            .related-articles h3 {
                color: #076e4d;
                margin: 0 0 1em 0;
                font-size: 1.3em;
                text-align: center;
            }
            
            .related-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1em;
            }
            
            .related-item {
                background: #fff;
                padding: 1em;
                border-radius: 6px;
                border: 1px solid #e1e5e9;
                transition: box-shadow 0.3s ease;
            }
            
            .related-item:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .related-item h4 {
                margin: 0 0 0.5em 0;
                font-size: 1.1em;
            }
            
            .related-item h4 a {
                color: #076e4d;
                text-decoration: none;
            }
            
            .related-item h4 a:hover {
                text-decoration: underline;
            }
            
            .related-description {
                font-size: 0.9em;
                color: #666;
                margin: 0 0 0.5em 0;
                line-height: 1.4;
            }
            
            .related-link {
                color: #3bb273;
                text-decoration: none;
                font-weight: 500;
                font-size: 0.9em;
            }
            
            .related-link:hover {
                text-decoration: underline;
            }
            
            /* RTL Support */
            [dir="rtl"] .nav-list,
            [dir="rtl"] .footer-links {
                direction: rtl;
            }
            
            [dir="rtl"] .related-link {
                direction: rtl;
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .nav-list {
                    gap: 0.5em;
                }
                
                .nav-list a {
                    padding: 6px 10px;
                    font-size: 14px;
                }
                
                .footer-links {
                    gap: 1em;
                    font-size: 14px;
                }
                
                .related-grid {
                    grid-template-columns: 1fr;
                }
                
                .related-articles {
                    padding: 1em;
                    margin: 1em 0;
                }
            }
        `;
        
        document.head.appendChild(style);
    }
    
    /**
     * Initialize the navigation system
     */
    async function init() {
        try {
            await fetchSiteIndex();
            
            if (!siteData) {
                console.warn('Site navigation: Could not load site data');
                return;
            }
            
            // Add basic styles
            addBasicStyles();
            
            // Inject navigation and footer
            injectNavigation();
            injectFooter();
            
            // Inject related articles for content pages
            injectRelatedArticles();
            
        } catch (error) {
            console.error('Site navigation initialization failed:', error);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for debugging/manual use
    window.SiteNav = {
        init,
        fetchSiteIndex,
        getCurrentPageData,
        getRelatedArticles,
        siteData: () => siteData
    };
    
})();