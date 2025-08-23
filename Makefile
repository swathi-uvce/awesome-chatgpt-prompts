# Awesome ChatGPT Prompts - Python Edition Makefile
# Provides easy commands for development and production

.PHONY: help install dev build serve clean test

help:  ## Show this help message
	@echo "Awesome ChatGPT Prompts - Python Edition"
	@echo "========================================"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install -r requirements.txt

dev:  ## Start development server
	@echo "🚀 Starting development server..."
	@echo "📱 Open http://localhost:4000 in your browser"
	@echo "🔄 Hot reload enabled - changes will auto-refresh"
	@echo "⏹️  Press Ctrl+C to stop"
	python app.py

build:  ## Build static site for production
	@echo "🏗️  Building static site..."
	python build.py build
	@echo "✅ Build complete! Site generated in _site/ directory"

serve:  ## Serve built static site locally
	@echo "🌐 Serving built site at http://localhost:8000"
	@echo "⏹️  Press Ctrl+C to stop"
	python build.py serve

clean:  ## Clean build artifacts
	@echo "🧹 Cleaning build directory..."
	rm -rf _site/
	@echo "✅ Clean complete!"

test:  ## Run tests (placeholder for future testing)
	@echo "🧪 Running tests..."
	@echo "⚠️  No tests configured yet. Add pytest to requirements.txt for testing."

deploy: build  ## Build and prepare for deployment
	@echo "🚀 Site ready for deployment!"
	@echo "📁 Deploy the contents of _site/ directory to your web server"
	@echo "🌐 Or use: make serve to test locally"

full: clean install build serve  ## Full workflow: clean, install, build, serve
	@echo "🎉 Full workflow complete!"

# Development shortcuts
run: dev  ## Alias for dev command
start: dev  ## Alias for dev command
live: dev  ## Alias for dev command

# Production shortcuts
prod: build  ## Alias for build command
static: build  ## Alias for build command
generate: build  ## Alias for build command
