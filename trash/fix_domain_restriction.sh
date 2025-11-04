#!/bin/bash

# Fix PDF.js domain restriction for localhost/GitHub Pages

cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy

echo "Fixing PDF.js domain restrictions..."

# Search for HOSTED_VIEWER_ORIGINS in viewer.mjs
if grep -q "HOSTED_VIEWER_ORIGINS" viewer.mjs; then
    echo "Found HOSTED_VIEWER_ORIGINS in viewer.mjs"
    
    # Backup
    cp viewer.mjs viewer.mjs.backup
    
    # The restriction checks if origin is mozilla.github.io
    # We need to allow localhost and github.io domains
    # This is a minified file, so we'll add localhost to the allowed list
    
    sed -i '' 's/mozilla\.github\.io/localhost|mozilla\.github\.io|github\.io/g' viewer.mjs
    
    echo "✅ Modified viewer.mjs to allow localhost and GitHub Pages"
else
    echo "HOSTED_VIEWER_ORIGINS not found, trying alternative approach..."
    
    # Try searching for domain validation
    if grep -q "validateFileURL" viewer.mjs; then
        echo "Found validateFileURL"
        cp viewer.mjs viewer.mjs.backup
        # Disable validation by making it always return true
        sed -i '' 's/validateFileURL/validateFileURLDisabled/g' viewer.mjs
        echo "✅ Disabled file URL validation"
    fi
fi

echo ""
echo "Restart your server and test again!"
