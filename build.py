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
    
    # Create main index.html using our actual templates
    from app import load_prompts, load_vibe_prompts
    
    # Load data
    prompts = load_prompts()
    vibe_prompts = load_vibe_prompts()
    
    # Read our actual templates
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        base_template = f.read()
    
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        index_template = f.read()
    
    # Simple template processing - replace placeholders
    def process_template(template_content, **replacements):
        """Simple template processor that replaces {{ variable }} with values"""
        result = template_content
        for key, value in replacements.items():
            placeholder = f"{{{{ {key} }}}}"
            result = result.replace(placeholder, str(value))
        return result
    
    # Process the index template first
    index_content = process_template(
        index_template,
        title="Awesome ChatGPT Prompts",
        subtitle="World's First & Most Famous Prompts Directory",
        body_class=""
    )
    
    # Process the base template with the index content
    main_content = process_template(
        base_template,
        title="Awesome ChatGPT Prompts",
        subtitle="World's First & Most Famous Prompts Directory", 
        body_class="",
        content=index_content
    )
    
    with open(build_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(main_content)
    
    print("✓ Generated index.html from templates")
    
    # Also create admin.html
    with open('templates/admin.html', 'r', encoding='utf-8') as f:
        admin_template = f.read()
    
    admin_content = process_template(
        admin_template,
        title="Admin - Add Prompts",
        subtitle="Add new prompts to the collection",
        body_class=""
    )
    
    with open(build_dir / 'admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_content)
    
    print("✓ Generated admin.html from templates")

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
