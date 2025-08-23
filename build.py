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
    
    # Files to copy
    static_files = [
        'style.css',
        'script.js',
        'embed-style.css',
        'embed-script.js',
        'embed-preview-style.css',
        'embed-preview-script.js',
        'favicon.ico'
    ]
    
    for file_path in static_files:
        if Path(file_path).exists():
            shutil.copy2(file_path, build_dir)
            print(f"✓ Copied {file_path}")

def copy_csv_files():
    """Copy CSV data files to build directory"""
    build_dir = Path('_site')
    
    csv_files = ['prompts.csv', 'vibeprompts.csv']
    for csv_file in csv_files:
        if Path(csv_file).exists():
            shutil.copy2(csv_file, build_dir)
            print(f"✓ Copied {csv_file}")

def copy_templates_to_static():
    """Copy and process templates to static HTML files"""
    build_dir = Path('_site')
    
    # Create main index.html
    from flask import render_template_string
    from app import load_prompts, load_vibe_prompts
    
    # Load data
    prompts = load_prompts()
    vibe_prompts = load_vibe_prompts()
    
    # Read base template
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base_template = f.read()
    
    # Read index template
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_template = f.read()
    
    # Create main page
    main_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Awesome ChatGPT Prompts — awesome AI prompts</title>
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
                                <select id="audienceSelect" class="audience-select">
                                    <option value="everyone">Everyone</option>
                                    <option value="developers">Developers</option>
                                </select>
                            </div>
                            <div class="prompt-count" id="promptCount">
                                <span class="count-label">All Prompts</span>
                                <span class="count-number">{len(prompts)}</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="prompts-grid">
                        <div class="prompt-card contribute-card">
                            <a href="https://github.com/f/awesome-chatgpt-prompts/pulls" target="_blank" style="text-decoration: none; color: inherit; height: 100%; display: flex; flex-direction: column;">
                                <div class="prompt-title" style="display: flex; align-items: center; gap: 8px;">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <circle cx="12" cy="12" r="10"></circle>
                                        <line x1="12" y1="8" x2="12" y2="16"></line>
                                        <line x1="8" y1="12" x2="16" y2="12"></line>
                                    </svg>
                                    Add Your Prompt
                                </div>
                                <p class="prompt-content" style="flex-grow: 1;">
                                    Share your creative prompts with the community! Submit a pull request to add your prompts to the collection.
                                </p>
                                <span class="contributor-badge">Contribute Now</span>
                            </a>
                        </div>
                        
                        {''.join([f'''
                        <div class="prompt-card" {'data-dev="true"' if prompt.get('for_devs') else ''}>
                            <div class="prompt-title">
                                {prompt['act']}
                                <div class="action-buttons">
                                    <button class="copy-button" title="Copy prompt" onclick="copyPrompt(this, '{prompt['prompt'].replace("'", "\\'").replace("\n", "\\n")}')">
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                            <p class="prompt-content">{prompt['prompt'][:200]}{'...' if len(prompt['prompt']) > 200 else ''}</p>
                            <a href="https://github.com/f" class="contributor-badge" target="_blank" rel="noopener">@f</a>
                        </div>
                        ''' for prompt in prompts])}
                    </div>
                </div>
            </div>
        </div>
        <script src="script.js"></script>
    </body>
    </html>
    """
    
    with open(build_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print("✓ Generated index.html")

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
