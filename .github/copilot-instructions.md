# دليل المال العربي (Arabic Money Guide)
Arabic financial education website powered by static HTML/CSS/JavaScript with automated Python content generation system.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively
- Repository setup and validation:
  - `cd /path/to/Zezooo342.github.io` 
  - `python3 --version` -- verify Python 3.12+ is available
  - `ls -la *.html | wc -l` -- should show 47+ HTML files
  - `python3 content_generator_pro.py` -- generates content successfully in <1 second. NEVER CANCEL.
  - `python3 automation_master.py` -- runs automation system in <1 second. NEVER CANCEL.
- Content generation scripts work WITHOUT external dependencies for basic functionality
- Python dependency installation with `pip install -r requirements.txt` requires network access:
  - **CRITICAL**: May fail in sandboxed environments due to network restrictions
  - **WORKAROUND**: Core content generation scripts work without external dependencies
  - **DEPENDENCIES**: requests, feedparser, textblob, beautifulsoup4, lxml, googletrans (for advanced features only)

## Validation Scenarios
- **ALWAYS** test the website by examining generated HTML files after running content scripts
- **ALWAYS** verify Arabic RTL layout is preserved in generated content
- **MANUAL VALIDATION**: Check generated Arabic content in files like `التسويق_بالعمول.html`, `العملات_الرقمية.html`
- **CONTENT VERIFICATION**: Ensure generated articles have proper Arabic financial education topics
- **SEO VALIDATION**: Verify structured data (JSON-LD) and Open Graph tags in generated HTML
- **NAVIGATION TEST**: Check that site navigation works with `assets/js/site-nav.js`

## Build Process and Timing
- **NO TRADITIONAL BUILD**: This is a static website - HTML files are served directly
- **Content Generation**: 
  - `python3 content_generator_pro.py` -- takes <1 second, generates 3 Arabic articles. NEVER CANCEL.
  - `python3 automation_master.py` -- takes <1 second, creates optimized content. NEVER CANCEL.
  - Scripts create HTML files with Arabic names like `العملات_الرقمية.html`
- **GitHub Actions Workflows**:
  - `.github/workflows/daily.yml` -- runs daily at 5:00 UTC for content generation
  - `.github/workflows/intelligent_automation.yml` -- runs every 6 hours for smart automation
  - **TIMING**: Workflows run in GitHub environment with network access for dependencies

## Repository Structure
```
/
├── *.html                    # 47+ static HTML pages (articles & main pages)
├── index.html               # Main homepage in Arabic
├── assets/
│   ├── js/                  # JavaScript files
│   │   ├── site-nav.js      # Navigation system
│   │   ├── ld-article.js    # Structured data generator
│   │   └── cookie-consent.js
│   ├── css/                 # Stylesheets
│   │   ├── common.min.css   # Main styles
│   │   └── nav.css          # Navigation styles
│   └── images/              # Image assets
├── Python Scripts:
│   ├── content_generator_pro.py  # Main content generator
│   ├── ai_growth_system.py      # AI content planning (requires deps)
│   ├── automation_master.py     # Automation system
│   └── self_optimization.py     # Performance optimization engine
├── .github/workflows/       # GitHub Actions automation
└── requirements.txt         # Python dependencies (external access required)
```

## Common Development Tasks

### Adding New Content
- **Generate Articles**: `python3 content_generator_pro.py` -- creates 3 new Arabic financial articles
- **Auto-optimization**: `python3 automation_master.py` -- creates optimized content based on analytics
- **Manual Creation**: Follow existing HTML template structure with Arabic RTL layout

### Testing Changes
- **Content Validation**: Check generated `.html` files for proper Arabic encoding and RTL layout
- **Navigation Test**: Verify `assets/js/site-nav.js` loads correctly
- **SEO Check**: Ensure structured data and meta tags are present in generated content
- **Local Testing**: Use `python3 -m http.server 8000` to serve files locally (if network allows)

### GitHub Actions Integration
- **Daily Content**: Workflows automatically generate content and commit changes
- **Manual Trigger**: Use GitHub UI to manually run `intelligent_automation.yml`
- **Dependencies**: GitHub Actions environment has network access for `pip install -r requirements.txt`

## Technical Specifications

### Content Generation System
- **Topics**: Arabic financial education (investment, cryptocurrency, online income, small business)
- **Output**: SEO-optimized HTML with Arabic RTL layout, structured data, and social media tags
- **Performance**: Core scripts run in <1 second without external dependencies
- **Advanced Features**: Require external dependencies (Google Trends, RSS feeds, translation)

### Website Features
- **Language**: Arabic (RTL layout)
- **SEO**: JSON-LD structured data, Open Graph tags, optimized meta descriptions
- **Monetization**: Google AdSense integration (ca-pub-9892132994837464)
- **Analytics**: Built-in performance tracking and optimization recommendations

### Known Limitations
- **Dependency Installation**: Requires network access for `pip install -r requirements.txt`
- **AI Features**: Advanced AI features (trends, RSS feeds) require external API access
- **GitHub Pages**: Deployment happens automatically via GitHub Pages from main branch

## File Inventory Reference
```bash
# Repository structure
ls -la *.html | wc -l          # 47+ HTML files (validated: shows 48 files)
ls -la *.py                    # 4 Python automation scripts (ai_growth_system.py, automation_master.py, content_generator_pro.py, self_optimization.py)
ls -la assets/js/              # 4 JavaScript files (cookie-consent.js, ld-article.js, site-nav.js, site-nav.min.js)
ls -la assets/css/             # 3 CSS files (common.min.css, nav.css, nav.min.css)

# Key files
head -10 index.html            # Main Arabic homepage
head -10 README.md             # Arabic documentation
cat requirements.txt           # Python dependencies list (6 packages)
ls -la .github/workflows/      # 2 automation workflows (daily.yml, intelligent_automation.yml)
```

## Troubleshooting
- **Pip Install Fails**: Core scripts work without external dependencies. Example error: "ERROR: Could not find a version that satisfies the requirement requests==2.32.5"
- **Content Generation Issues**: Check Python 3.12+ is available, core scripts work without network dependencies
- **Advanced AI Features Fail**: ai_growth_system.py requires external dependencies. Error: "ModuleNotFoundError: No module named 'feedparser'"
- **Arabic Encoding Problems**: Ensure UTF-8 encoding is preserved. Check files contain `lang="ar" dir="rtl"`
- **GitHub Actions Failures**: Check workflow logs for dependency installation issues
- **HTML Validation**: Use browser developer tools to check for RTL layout and Arabic text rendering

## Critical Notes
- **NEVER CANCEL** content generation scripts - they complete in <1 second
- **ALWAYS** preserve Arabic text encoding and RTL layout in any modifications
- **MANUAL VALIDATION REQUIRED**: Test generated Arabic content for accuracy and proper formatting
- Core functionality works without external dependencies - use this for basic development and testing