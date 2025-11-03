# PDF.js Viewer Setup Instructions

## Option 1: Quick Setup Script

Run this script to automatically download and setup PDF.js:

```bash
cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy
chmod +x download_pdfjs.sh
./download_pdfjs.sh
```

## Option 2: Manual Download

If the script doesn't work:

1. **Download PDF.js prebuilt package:**
   - Go to: https://github.com/mozilla/pdf.js/releases
   - Download: `pdfjs-4.0.379-dist.zip` (or latest version)

2. **Extract the files:**
   ```bash
   unzip pdfjs-4.0.379-dist.zip
   ```

3. **Copy to your SelfStudy directory:**
   ```bash
   cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy
   
   # Copy all web viewer files
   cp -r path/to/extracted/pdfjs-4.0.379-dist/web/* .
   
   # Copy the build library
   cp -r path/to/extracted/pdfjs-4.0.379-dist/build .
   ```

## Required Files

After setup, you should have:

```
SelfStudy/
├── index.html (already created ✅)
├── viewer.html (from PDF.js)
├── viewer.css (from PDF.js)
├── viewer.mjs (from PDF.js)
├── build/
│   ├── pdf.mjs
│   └── pdf.worker.mjs
├── locale/ (translation files)
├── images/ (viewer icons)
└── [your book directories...]
```

## Checking if Setup Worked

Run this to verify:

```bash
cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy
ls -la viewer.html build/pdf.mjs
```

If both files exist, you're good to go!

## Testing Locally

Open `index.html` in your browser:
- Chrome/Edge: May need to run a local server due to CORS
- Firefox: Should work directly
- Safari: May need local server

### Simple local server:
```bash
cd /Users/natkite/Documents/2025/netsi25/PhD/phd-dev/SelfStudy
python3 -m http.server 8000
```

Then open: http://localhost:8000

## For GitHub Pages

Once the files are in place:

1. Commit everything:
   ```bash
   git add .
   git commit -m "Add PDF.js viewer and library interface"
   git push
   ```

2. Enable Pages:
   - Repo Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/ (root)`

3. Your library will be live at:
   `https://thechesirecat.github.io/SelfStudy/`

## Note on Git LFS

The `build/` directory contains large files. Since you already have Git LFS set up (I see `.git/lfs/` in your directory), the large PDFs should already be tracked. The PDF.js library files are smaller and shouldn't need LFS.

## Troubleshooting

**Error: "Cannot find viewer.html"**
- Make sure you ran the download script or manually copied the files

**Error: "CORS policy"**
- Use a local server (python -m http.server) for testing
- Will work fine on GitHub Pages

**PDFs not loading**
- Check that file paths match exactly (case-sensitive)
- Verify PDFs are in the correct directories
