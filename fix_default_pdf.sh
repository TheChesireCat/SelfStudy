#!/bin/bash

# Fix PDF.js default URL issue
# Replace the hardcoded default PDF with empty file

cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy

echo "Searching for defaultUrl in viewer.mjs..."

# The defaultUrl is hardcoded in the minified viewer.mjs
# We need to find and replace it

# Method 1: Replace the default PDF filename in viewer.mjs
if [ -f "viewer.mjs" ]; then
    echo "Backing up viewer.mjs..."
    cp viewer.mjs viewer.mjs.backup
    
    echo "Replacing default URL..."
    # Replace compressed.tracemonkey-pldi-09.pdf with empty string
    sed -i '' 's/compressed\.tracemonkey-pldi-09\.pdf//g' viewer.mjs
    
    echo "✅ Modified viewer.mjs"
fi

echo ""
echo "Now test again with:"
echo "  http://localhost:3000/viewer.html?file=01-Foundations/Computer-Science/Algorithms/Introduction-to-Algorithms-4th-Ed-CLRS.pdf"
echo ""
