// Override PDF.js default URL
// This prevents the viewer from loading compressed.tracemonkey-pldi-09.pdf by default

const defaultOptions = {
  defaultUrl: {
    value: "",  // Empty string - no default PDF
    kind: 0  // OptionKind.VIEWER
  }
};

// Export for PDF.js to use
if (typeof PDFViewerApplicationOptions !== 'undefined') {
  for (const key in defaultOptions) {
    PDFViewerApplicationOptions.set(key, defaultOptions[key].value);
  }
}
