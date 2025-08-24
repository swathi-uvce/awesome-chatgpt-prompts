# GitHub Pages Deployment Guide

## Overview

This repository is configured to automatically deploy the ChatGPT Prompts site to GitHub Pages whenever changes are pushed to the `main` branch.

## How it Works

1. **Automated Build**: When you push to `main`, GitHub Actions automatically:
   - Sets up Python 3.11
   - Installs dependencies from `requirements.txt`
   - Runs `python build.py build` to generate static files
   - Deploys the `_site/` directory to GitHub Pages

2. **Static Site Generation**: The `build.py` script:
   - Uses Flask's template engine to render Jinja2 templates
   - Processes all prompt data from CSV files
   - Generates optimized static HTML files
   - Creates proper relative file paths for GitHub Pages
   - Adds `.nojekyll` file for compatibility

## Deployment Process

### Automatic Deployment
- **Trigger**: Push to `main` branch
- **Workflow**: `.github/workflows/publish.yml`
- **Build Time**: ~2-3 minutes
- **Live Site**: Available at your GitHub Pages URL

### Manual Deployment (if needed)
```bash
# Build the site locally
python build.py build

# The generated files in _site/ directory can be deployed to any static hosting
```

## Local Development

### Development Server
```bash
# Install dependencies
pip install -r requirements.txt

# Start development server (hot reload)
python app.py
# Visit http://localhost:4000

# Or use make commands
make dev
```

### Test Production Build
```bash
# Build static site
python build.py build

# Serve built site locally
python build.py serve
# Visit http://localhost:8000

# Or use make commands
make build
make serve
```

## File Structure

```
_site/                 # Generated static files (auto-created)
├── .nojekyll         # GitHub Pages compatibility file
├── index.html        # Main page (878KB with all prompts)
├── admin.html        # Admin interface
├── style.css         # Stylesheets
├── script.js         # JavaScript functionality
├── prompts.csv       # Prompt data
└── vibeprompts.csv   # Vibe prompt data

templates/            # Source templates
├── base.html         # Base template
├── index.html        # Main page template
└── admin.html        # Admin page template

static/               # Static assets (copied to _site/)
├── style.css
└── script.js
```

## Troubleshooting

### Build Failures
If the GitHub Pages deployment fails:

1. **Check the Actions tab** in your repository for error details
2. **Test locally** using `python build.py build`
3. **Common issues**:
   - Missing dependencies in `requirements.txt`
   - Template syntax errors
   - CSV file format issues

### Site Not Loading
If the deployed site doesn't load properly:

1. **Check GitHub Pages settings** in repository settings
2. **Verify custom domain** configuration (if using one)
3. **Clear browser cache** and check browser console for errors

### Development Issues
If local development isn't working:

```bash
# Clean and reinstall
rm -rf _site/
pip install -r requirements.txt
python app.py
```

## Performance

- **Build Time**: ~30 seconds
- **Site Size**: ~1.1MB total
- **Main Page**: 878KB (includes all prompts)
- **Load Time**: <2 seconds on average connection

## Custom Domain

To use a custom domain (like `prompts.chat`):

1. Add `CNAME` file to repository root with your domain
2. Update DNS settings to point to GitHub Pages
3. The workflow automatically handles CNAME file deployment

## Security

- No server-side code execution required
- Static files only - secure by default
- All processing happens during build time
- No database or dynamic content vulnerabilities