#!/usr/bin/env python3
"""
Awesome ChatGPT Prompts - Python Flask Application
Replaces Jekyll functionality with Python-based static site generation
"""

import os
import csv
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_frozen import Freezer
import markdown
import frontmatter
from pathlib import Path

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['FREEZER_RELATIVE_URLS'] = True
freezer = Freezer(app)

# Global data storage
prompts_data = []
vibe_prompts_data = []

def load_prompts():
    """Load prompts from CSV file"""
    global prompts_data
    csv_path = Path('prompts.csv')
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            prompts_data = list(reader)
            # Convert for_devs to boolean
            for prompt in prompts_data:
                prompt['for_devs'] = prompt['for_devs'].upper() == 'TRUE'
    return prompts_data

def load_vibe_prompts():
    """Load vibe prompts from CSV file"""
    global vibe_prompts_data
    csv_path = Path('vibeprompts.csv')
    if csv_path.exists():
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            vibe_prompts_data = list(reader)
    return vibe_prompts_data

def parse_markdown_content(content):
    """Convert markdown content to HTML"""
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    return md.convert(content)

@app.route('/')
def index():
    """Main page route"""
    prompts = load_prompts()
    return render_template('index.html', 
                         prompts=prompts, 
                         total_prompts=len(prompts),
                         title="Awesome ChatGPT Prompts",
                         subtitle="World's First & Most Famous Prompts Directory")

@app.route('/vibe')
def vibe():
    """Vibe coding mode route"""
    vibe_prompts = load_vibe_prompts()
    return render_template('vibe.html',
                         prompts=vibe_prompts,
                         total_prompts=len(vibe_prompts),
                         title="/vibe",
                         subtitle="awesome vibe coding prompts to help you build simple apps")

@app.route('/prompts.csv')
def prompts_csv():
    """Serve prompts CSV file"""
    return send_from_directory('.', 'prompts.csv')

@app.route('/vibeprompts.csv')
def vibeprompts_csv():
    """Serve vibe prompts CSV file"""
    return send_from_directory('.', 'vibeprompts.csv')

@app.route('/api/prompts')
def api_prompts():
    """API endpoint for prompts"""
    prompts = load_prompts()
    audience = request.args.get('audience', 'everyone')
    
    if audience == 'developers':
        filtered_prompts = [p for p in prompts if p.get('for_devs', False)]
    else:
        filtered_prompts = prompts
    
    return jsonify({
        'prompts': filtered_prompts,
        'total': len(filtered_prompts),
        'filtered': len(filtered_prompts)
    })

@app.route('/api/search')
def api_search():
    """Search API endpoint"""
    query = request.args.get('q', '').lower()
    audience = request.args.get('audience', 'everyone')
    
    prompts = load_prompts()
    
    if audience == 'developers':
        prompts = [p for p in prompts if p.get('for_devs', False)]
    
    if query:
        filtered_prompts = [
            p for p in prompts 
            if query in p.get('act', '').lower() or query in p.get('prompt', '').lower()
        ]
    else:
        filtered_prompts = prompts
    
    return jsonify({
        'prompts': filtered_prompts,
        'total': len(filtered_prompts),
        'filtered': len(filtered_prompts)
    })

@app.route('/api/github-stars')
def api_github_stars():
    """GitHub stars API endpoint (mock for now)"""
    return jsonify({
        'stargazers_count': 129000
    })

# Static file routes for non-static folder files
@app.route('/<path:filename>')
def static_files(filename):
    """Serve static files that aren't in the static folder"""
    # List of files that should be served from root
    root_files = ['style.css', 'script.js', 'embed-style.css', 'embed-script.js', 
                  'embed-preview-style.css', 'embed-preview-script.js', 'favicon.ico']
    
    if filename in root_files:
        return send_from_directory('.', filename)
    
    # Try to serve from static folder
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Load data on startup
    load_prompts()
    load_vibe_prompts()
    
    # Development server
    app.run(debug=True, host='0.0.0.0', port=4001)
