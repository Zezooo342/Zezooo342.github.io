/**
 * Centralized JSON-LD Article Schema Generator
 * Usage: Add data-* attributes to a container element to generate structured data
 * 
 * Example:
 * <div data-ld-article data-headline="Article Title" data-description="Description" 
 *      data-date-published="2025-01-15" data-image="image.jpg" data-author="Author Name">
 * </div>
 */

(function() {
    'use strict';
    
    // Default configuration
    const defaults = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        publisher: {
            '@type': 'Organization',
            name: 'دليل المال العربي',
            url: 'https://zezooo342.github.io'
        },
        mainEntityOfPage: {
            '@type': 'WebPage',
            '@id': window.location.href
        }
    };
    
    function generateArticleSchema(element) {
        const data = element.dataset;
        
        if (!data.ldArticle) return null;
        
        const schema = Object.assign({}, defaults);
        
        // Required fields
        if (data.headline) schema.headline = data.headline;
        if (data.description) schema.description = data.description;
        if (data.datePublished) schema.datePublished = data.datePublished;
        
        // Image handling
        if (data.image) {
            const imageUrl = data.image.startsWith('http') ? data.image : 
                           `https://zezooo342.github.io/${data.image}`;
            schema.image = imageUrl;
        } else {
            schema.image = 'https://zezooo342.github.io/assets/images/og-default.png';
        }
        
        // Author handling
        if (data.author) {
            schema.author = {
                '@type': 'Person',
                name: data.author
            };
        } else {
            schema.author = {
                '@type': 'Person',
                name: 'فريق دليل المال العربي'
            };
        }
        
        // Optional fields
        if (data.dateModified) schema.dateModified = data.dateModified;
        if (data.keywords) schema.keywords = data.keywords.split(',').map(k => k.trim());
        if (data.articleSection) schema.articleSection = data.articleSection;
        if (data.wordCount) schema.wordCount = parseInt(data.wordCount);
        
        return schema;
    }
    
    function injectSchema(schema) {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(schema, null, 2);
        document.head.appendChild(script);
    }
    
    // Initialize when DOM is ready
    function init() {
        const articleElements = document.querySelectorAll('[data-ld-article]');
        
        articleElements.forEach(element => {
            const schema = generateArticleSchema(element);
            if (schema) {
                injectSchema(schema);
            }
        });
    }
    
    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose for manual use
    window.LDArticle = {
        generate: generateArticleSchema,
        inject: injectSchema,
        init: init
    };
})();