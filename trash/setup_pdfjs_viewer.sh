#!/bin/bash

# Setup PDF.js Viewer for SelfStudy Library
# This script downloads the necessary PDF.js viewer files

echo "╔════════════════════════════════════════╗"
echo "║   Setting up PDF.js Viewer             ║"
echo "╚════════════════════════════════════════╝"
echo ""

BASE_DIR="/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy"
cd "$BASE_DIR"

# Download PDF.js prebuilt version
echo "📥 Downloading PDF.js viewer files..."
echo ""

# Create temporary directory
mkdir -p temp_pdfjs
cd temp_pdfjs

# Download the latest stable release
echo "Downloading from GitHub releases..."
curl -L "https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip" -o pdfjs.zip

echo "📦 Extracting files..."
unzip -q pdfjs.zip

echo "📁 Moving viewer files to repository..."
cd ..

# Copy the web viewer files
cp -r temp_pdfjs/web/* .

# Clean up
echo "🧹 Cleaning up..."
rm -rf temp_pdfjs

echo ""
echo "✅ PDF.js viewer setup complete!"
echo ""
echo "Files added:"
echo "  • viewer.html - Main PDF viewer"
echo "  • viewer.css - Viewer styles"
echo "  • viewer.mjs - Viewer JavaScript"
echo "  • build/ - PDF.js library files"
echo "  • locale/ - Translation files"
echo "  • images/ - Viewer icons"
echo ""
echo "🚀 Your library is ready!"
echo "   Open index.html in a browser to view your library"
echo ""
echo "📝 Note: Add these to .gitignore if files are too large:"
echo "   echo 'build/' >> .gitignore"
echo "   echo 'web/' >> .gitignore"
echo ""
