#!/bin/bash

# Download PDF.js viewer files from official source

echo "╔════════════════════════════════════════╗"
echo "║   Downloading PDF.js Viewer            ║"
echo "╚════════════════════════════════════════╝"
echo ""

BASE_DIR="/Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy"
cd "$BASE_DIR"

# Download the latest stable release (v4.0.379)
echo "📥 Downloading PDF.js v4.0.379..."

# Create temp directory
mkdir -p pdfjs-temp
cd pdfjs-temp

# Download from GitHub releases
curl -L "https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip" -o pdfjs.zip

if [ ! -f pdfjs.zip ]; then
    echo "❌ Download failed. Trying alternative method..."
    wget "https://github.com/mozilla/pdf.js/releases/download/v4.0.379/pdfjs-4.0.379-dist.zip" -O pdfjs.zip
fi

echo "📦 Extracting..."
unzip -q pdfjs.zip

echo "📁 Copying viewer files..."
cd ..

# Copy web directory contents (viewer files)
cp -r pdfjs-temp/web/* .

# Copy build directory (PDF.js library)
cp -r pdfjs-temp/build .

echo "🧹 Cleaning up..."
rm -rf pdfjs-temp

echo ""
echo "✅ Setup complete!"
echo ""
echo "Files added to your repository:"
echo "  ├── viewer.html"
echo "  ├── viewer.css"
echo "  ├── viewer.mjs"
echo "  ├── build/"
echo "  │   ├── pdf.mjs"
echo "  │   └── pdf.worker.mjs"
echo "  ├── locale/"
echo "  └── images/"
echo ""
echo "🚀 You can now:"
echo "   1. Open index.html in a browser to test locally"
echo "   2. Commit and push to GitHub"
echo "   3. Enable GitHub Pages in repo settings"
echo ""
echo "⚠️  Note: The build/ folder is large (~3MB)."
echo "   Consider using Git LFS if you haven't already."
echo ""
