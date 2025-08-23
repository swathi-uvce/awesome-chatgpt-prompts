#!/usr/bin/env python3
"""
Quick Start Script for Awesome ChatGPT Prompts - Python Edition
Helps users get up and running quickly with the new Python-based system
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print the project banner"""
    print("🚀 Awesome ChatGPT Prompts - Python Edition")
    print("=" * 50)
    print("Successfully migrated from Jekyll (Ruby) to Python Flask!")
    print("All features preserved with improved development experience.")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n🔍 Checking dependencies...")
    
    try:
        import flask
        print("✅ Flask installed")
    except ImportError:
        print("❌ Flask not installed")
        return False
    
    try:
        import flask_frozen
        print("✅ Frozen-Flask installed")
    except ImportError:
        print("❌ Frozen-Flask not installed")
        return False
    
    try:
        import markdown
        print("✅ Markdown installed")
    except ImportError:
        print("❌ Markdown not installed")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_files():
    """Check if required files exist"""
    print("\n📁 Checking project files...")
    
    required_files = [
        "app.py",
        "build.py", 
        "requirements.txt",
        "prompts.csv",
        "templates/base.html",
        "templates/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def show_commands():
    """Show available commands"""
    print("\n🎯 Available Commands:")
    print("=" * 30)
    print("Development:")
    print("  python app.py          # Start development server")
    print("  make dev               # Start development server (if make available)")
    print()
    print("Production:")
    print("  python build.py build  # Build static site")
    print("  python build.py serve  # Serve built site")
    print("  make build             # Build static site (if make available)")
    print("  make serve             # Serve built site (if make available)")
    print()
    print("Utility:")
    print("  make help              # Show all available commands")
    print("  make clean             # Clean build directory")
    print("  make full              # Full workflow: clean, install, build, serve")

def start_development():
    """Start the development server"""
    print("\n🚀 Starting development server...")
    print("📱 Open http://localhost:4000 in your browser")
    print("🔄 Hot reload enabled - changes will auto-refresh")
    print("⏹️  Press Ctrl+C to stop")
    print()
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")

def main():
    """Main quick start function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        print("\n💡 Please install Python 3.8+ and try again")
        return
    
    # Check if dependencies are installed
    if not check_dependencies():
        print("\n📦 Installing dependencies...")
        if not install_dependencies():
            print("\n❌ Failed to install dependencies. Please run:")
            print("   pip install -r requirements.txt")
            return
    
    # Check project files
    if not check_files():
        print("\n❌ Some required files are missing.")
        print("Please ensure you're in the correct project directory.")
        return
    
    # Show available commands
    show_commands()
    
    # Ask if user wants to start development server
    print("\n" + "=" * 50)
    response = input("🚀 Would you like to start the development server now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes', '']:
        start_development()
    else:
        print("\n💡 To start development later, run:")
        print("   python app.py")
        print("   or")
        print("   make dev")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Run 'python quickstart.py' again when you're ready.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your setup and try again.")
