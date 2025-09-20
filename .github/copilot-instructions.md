# GitHub Copilot Instructions

## Project Overview
This is an Arabic financial guidance website (`دليل المال العربي`) hosted on GitHub Pages. The site provides financial advice, investment guides, and money-making strategies for Arabic-speaking audiences.

## Code Structure
- **HTML Files**: Article pages with Arabic content about financial topics
- **Python Scripts**: Content generation and automation tools
  - `ai_growth_system.py`: RSS feed processing and article planning
  - `content_generator_pro.py`: Article generation with SEO optimization
  - `self_optimization.py`: Performance analysis and optimization engine
- **Assets**: CSS, JavaScript, and image files for the website

## Coding Standards

### Python Code
- Use Arabic comments for user-facing strings and business logic
- Follow PEP 8 style guidelines
- Include proper error handling with try-catch blocks
- Use type hints where appropriate
- Maintain consistent indentation (4 spaces)

### HTML/CSS
- Ensure RTL (Right-to-Left) support for Arabic content
- Include proper meta tags for SEO
- Use semantic HTML structure
- Maintain responsive design principles

### Error Handling
- Always wrap external API calls in try-catch blocks
- Provide meaningful error messages in Arabic when appropriate
- Log errors for debugging purposes
- Gracefully handle missing data or failed requests

## Common Issues to Avoid
1. **Translation Logic**: When checking conditions for translation, ensure the condition matches the data being processed
2. **Encoding**: Always use UTF-8 encoding for Arabic text
3. **Empty Content**: Validate data before processing to avoid empty or null values
4. **Network Calls**: Handle network timeouts and connection errors
5. **File Operations**: Use proper file handling with context managers

## Testing Guidelines
- Test all Python scripts for syntax errors using `python -m py_compile`
- Validate HTML structure and accessibility
- Test Arabic text rendering and RTL layout
- Verify all external links and dependencies

## Performance Considerations
- Optimize images for web delivery
- Minimize HTTP requests
- Use efficient data structures for large datasets
- Cache frequently accessed data when possible

## Security Best Practices
- Never commit API keys or sensitive data
- Validate all user inputs
- Use HTTPS for all external requests
- Sanitize content before rendering

## Content Guidelines
- Maintain professional tone in Arabic content
- Provide accurate financial information
- Include proper disclaimers for investment advice
- Use clear, accessible language for general audience