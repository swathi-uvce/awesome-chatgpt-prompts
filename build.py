#!/usr/bin/env python3
"""
Build script for generating static site from Flask application
Replaces Jekyll build functionality
"""

import os
import shutil
from pathlib import Path
from app import app, freezer

def clean_build_directory():
    """Clean the build directory"""
    build_dir = Path('_site')
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(exist_ok=True)

def copy_static_files():
    """Copy static files to build directory"""
    build_dir = Path('_site')
    
    # Files to copy from root directory
    root_files = [
        'style.css',
        'script.js',
        'favicon.ico'
    ]
    
    for file_path in root_files:
        if Path(file_path).exists():
            shutil.copy2(file_path, build_dir)
            print(f"✓ Copied {file_path}")
    
    # Copy static directory if it exists
    static_dir = Path('static')
    if static_dir.exists():
        for static_file in static_dir.rglob('*'):
            if static_file.is_file():
                # Copy to build directory with same filename (not nested)
                dest_path = build_dir / static_file.name
                shutil.copy2(static_file, dest_path)
                print(f"✓ Copied static/{static_file.name}")
    
    # Ensure critical files exist or create minimal versions
    critical_files = {
        'style.css': '/* Awesome ChatGPT Prompts Styles */\nbody { font-family: system-ui; }',
        'script.js': '// Awesome ChatGPT Prompts JavaScript\nconsole.log("Prompts loaded");'
    }
    
    for filename, content in critical_files.items():
        file_path = build_dir / filename
        if not file_path.exists():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created minimal {filename}")

def copy_csv_files():
    """Copy CSV data files to build directory"""
    build_dir = Path('_site')
    
    csv_files = ['prompts.csv', 'vibeprompts.csv']
    for csv_file in csv_files:
        if Path(csv_file).exists():
            shutil.copy2(csv_file, build_dir)
            print(f"✓ Copied {csv_file}")

def copy_templates_to_static():
    """Copy and process templates to static HTML files using Flask's template engine"""
    build_dir = Path('_site')
    
    # Import Flask app components
    from app import app, load_prompts, load_vibe_prompts
    
    # Load data
    prompts = load_prompts()
    vibe_prompts = load_vibe_prompts()
    
    # Use Flask's template engine to render templates properly
    with app.app_context():
        try:
            # Create a mock request context for url_for to work
            with app.test_request_context():
                # Import render_template_string after setting up context
                from flask import render_template
                
                # Render index.html with data
                index_html = render_template('index.html', 
                                           title="Awesome ChatGPT Prompts",
                                           subtitle="World's First & Most Famous Prompts Directory",
                                           prompts=prompts,
                                           total_prompts=len(prompts))
                
                # Post-process to fix static file URLs for GitHub Pages
                import re
                # Replace Flask url_for static calls with relative paths
                index_html = re.sub(r'/static/([^"\']+)', r'\1', index_html)
                
                with open(build_dir / 'index.html', 'w', encoding='utf-8') as f:
                    f.write(index_html)
                
                print("✓ Generated index.html from templates")
                
                # Generate admin.html if it exists
                try:
                    admin_html = render_template('admin.html',
                                               title="Admin - Add Prompts",
                                               subtitle="Add new prompts to the collection")
                    # Post-process to fix static file URLs
                    admin_html = re.sub(r'/static/([^"\']+)', r'\1', admin_html)
                    
                    with open(build_dir / 'admin.html', 'w', encoding='utf-8') as f:
                        f.write(admin_html)
                    
                    print("✓ Generated admin.html from templates")
                except Exception as e:
                    print(f"⚠️ Could not generate admin.html: {e}")
                    
        except Exception as e:
            print(f"❌ Template rendering failed: {e}")
            # Fallback to simple template processing
            print("🔄 Falling back to simple template processing...")
            _simple_template_fallback(build_dir, prompts)

def _simple_template_fallback(build_dir, prompts):
    """Simple fallback template processing when Flask rendering fails"""
    # Create a basic HTML page with the prompts data
    html_content = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Awesome ChatGPT Prompts — awesome AI prompts</title>
    <meta name="description" content="World's First & Most Famous Prompts Directory">
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="layout-wrapper">
        <header class="site-header">
            <div class="header-left">
                <h1 class="site-title">Awesome ChatGPT Prompts</h1>
                <p class="site-slogan">World's First & Most Famous Prompts Directory</p>
            </div>
        </header>
        <div class="content-wrapper">
            <div class="container-lg markdown-body">
                <div class="search-section">
                    <div class="search-header">
                        <div class="search-controls">
                            <div class="search-input-wrapper">
                                <input type="text" id="searchInput" placeholder="Search prompts..." class="search-input">
                                <div id="searchResults" class="search-results"></div>
                            </div>
                        </div>
                        <div class="prompt-count" id="promptCount">
                            <span class="count-label">All Prompts</span>
                            <span class="count-number">{len(prompts)}</span>
                        </div>
                    </div>
                </div>
                <div class="prompts-grid">
                    <!-- Contribute Card -->
                    <div class="prompt-card contribute-card">
                        <a href="https://github.com/swathi-uvce/awesome-chatgpt-prompts/pulls" target="_blank" style="text-decoration: none; color: inherit; height: 100%; display: flex; flex-direction: column;">
                            <div class="prompt-title" style="display: flex; align-items: center; gap: 8px;">Add Your Prompt</div>
                            <p class="prompt-content" style="flex-grow: 1;">Share your creative prompts with the community! Submit a pull request to add your prompts to the collection.</p>
                            <span class="contributor-badge">Contribute Now</span>
                        </a>
                    </div>"""
    
    # Add prompt cards
    for prompt in prompts[:50]:  # Limit to first 50 prompts for simplicity
        escaped_prompt = prompt.get('prompt', '').replace('"', '&quot;').replace("'", "\\'").replace('\n', '\\n')[:200]
        html_content += f"""
                    <div class="prompt-card">
                        <div class="prompt-title">{prompt.get('act', 'Prompt')}</div>
                        <p class="prompt-content">{escaped_prompt}...</p>
                        <button class="copy-button" onclick="navigator.clipboard.writeText('{escaped_prompt}')">Copy</button>
                    </div>"""
    
    html_content += """
                </div>
            </div>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>"""
    
    with open(build_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✓ Generated index.html with fallback method")

def add_nojekyll_file():
    """Add .nojekyll file for GitHub Pages compatibility"""
    build_dir = Path('_site')
    with open(build_dir / '.nojekyll', 'w') as f:
        f.write('')
    print("✓ Added .nojekyll file for GitHub Pages")

def add_cname_file():
    """Add CNAME file if custom domain is configured"""
    build_dir = Path('_site')
    
    # Check if CNAME file exists in root
    root_cname = Path('CNAME')
    if root_cname.exists():
        shutil.copy2(root_cname, build_dir)
        print("✓ Copied CNAME file for custom domain")
    else:
        # Create CNAME for prompts.chat domain
        with open(build_dir / 'CNAME', 'w') as f:
            f.write('prompts.chat\n')
        print("✓ Created CNAME file for prompts.chat domain")

def add_seo_files():
    """Add SEO and meta files"""
    build_dir = Path('_site')
    
    # Add robots.txt
    robots_content = """User-agent: *
Allow: /

Sitemap: https://prompts.chat/sitemap.xml
"""
    with open(build_dir / 'robots.txt', 'w') as f:
        f.write(robots_content)
    print("✓ Added robots.txt for SEO")
    
    # Add basic sitemap.xml
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://prompts.chat/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    with open(build_dir / 'sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    print("✓ Added sitemap.xml for SEO")
    
    # Add manifest.json for PWA
    manifest_content = """{
  "name": "Awesome ChatGPT Prompts",
  "short_name": "ChatGPT Prompts",
  "description": "World's First & Most Famous Prompts Directory",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/favicon.ico",
      "sizes": "any",
      "type": "image/x-icon"
    }
  ]
}"""
    with open(build_dir / 'manifest.json', 'w') as f:
        f.write(manifest_content)
    print("✓ Added manifest.json for PWA support")

def build_site():
    """Build the static site"""
    print("🚀 Building static site...")
    
    # Clean build directory
    clean_build_directory()
    
    try:
        # Try to use Frozen-Flask
        print("🔄 Attempting to freeze Flask app...")
        freezer.freeze()
        print("✅ Frozen-Flask build successful!")
    except Exception as e:
        print(f"⚠️  Frozen-Flask failed: {e}")
        print("🔄 Falling back to manual static generation...")
        copy_templates_to_static()
    
    # Copy additional static files
    copy_static_files()
    copy_csv_files()
    
    # Add .nojekyll file for GitHub Pages compatibility
    add_nojekyll_file()
    
    # Add CNAME file for custom domain support
    add_cname_file()
    
    # Add SEO files
    add_seo_files()
    
    print("✅ Static site built successfully!")
    print(f"📁 Output directory: {Path('_site').absolute()}")

def serve_site():
    """Serve the built site locally"""
    import http.server
    import socketserver
    
    build_dir = Path('_site')
    if not build_dir.exists():
        print("❌ Build directory not found. Run 'python build.py' first.")
        return
    
    # Don't change working directory, serve from current location
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Create a custom handler that serves from the _site directory
    class SiteHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(build_dir.absolute()), **kwargs)
    
    with socketserver.TCPServer(("", PORT), SiteHandler) as httpd:
        print(f"🌐 Serving site at http://localhost:{PORT}")
        print("📁 Serving from:", build_dir.absolute())
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'build':
            build_site()
        elif command == 'serve':
            serve_site()
        elif command == 'dev':
            print("🚀 Starting development server...")
            print("Run 'python app.py' for development mode")
        else:
            print("Usage: python build.py [build|serve|dev]")
            print("  build  - Generate static site")
            print("  serve  - Serve built site locally")
            print("  dev    - Show development instructions")
    else:
        build_site()
