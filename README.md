# SelfStudy / catCafe

This repository is a curated collection of course materials and books to build a strong foundation in Complex Systems, Network Science, and related fields. The `index.html` app provides a collapsible library of PDFs, loads them with the bundled PDF.js viewer, and adds bookmarks, light/dark theme, and tts.rocks-powered narration for selections or whole pages.

## Run locally
1. From the repo root, start a static server (needed for the PDF.js module worker):  
   `python3 -m http.server 8000`
2. Visit `http://localhost:8000/index.html`.
3. Internet access is required for the hosted PDFs (GitHub `media` URLs) and the tts.rocks voice engine.

## Reader features
- Library sidebar for quick browsing; mobile drawers and bottom shortcuts.
- Bookmarks saved in `localStorage`, with auto-save on page changes and quick resume.
- TTS: read current selection or entire page via tts.rocks, with speed control (0.6–3×), mini overlay player, and queue/auto-continue controls.
- TTS queue: enqueue current/next pages, auto-advance until stopped, skip ahead, and toggle auto-continue; overlay and tools show queue status.
- EPUB viewer: inline rendering via epub.js with simple prev/next controls; MOBI opens via an embedded external viewer (may be blocked by some hosts—download if it fails).
- Theme sync between parent and PDF iframe (light/dark).

## What’s here
- `index.html` – primary UI, library tree, bookmark + narration controls, theme toggle.
- `viewer/` – PDF.js viewer assets with a messaging shim (`viewer.html`) that reports page changes, selection text, and page text to the parent.
- `tts.js` – bundled copy of the tts.rocks helper (page currently pulls the CDN version; keep this if you want to self-host).
- `01-Foundations` … `05-General-Reading` – subject folders with PDFs, notes, and supporting materials.
- `instructions.md` – working notes on the TTS integration idea.
- External links section in the sidebar: PDFs open in the viewer; EPUBs open in the inline ebook reader; MOBIs try an embedded external viewer; non-PDF sites load in an embedded iframe (some sites may block embedding via X-Frame-Options).

## 📚 Library structure
### 01-Foundations
#### Mathematics
- **Calculus**
  - [Crash Course in Vector Calculus](./01-Foundations/Mathematics/Calculus/Crash-Course-in-Vector-Calculus.pdf)
  - [Single and Multivariable Calculus: Early Transcendentals](./01-Foundations/Mathematics/Calculus/Single-and-Multivariable-Calculus-Early-Transcendentals.pdf)
- **Linear Algebra**
  - [Linear Algebra and Multivariable Calculus - MIT 18.02 (Evan Chen)](./01-Foundations/Mathematics/Linear-Algebra/Linear-Algebra-and-Multivariable-Calculus-Chen-MIT-18.02.pdf)
  - [Linear Algebra (Cherney, Denton, Thomas, Waldron)](./01-Foundations/Mathematics/Linear-Algebra/Linear-Algebra-Cherney-Denton-Thomas-Waldron.pdf)
  - [Topics in Random Matrix Theory (Terence Tao)](./01-Foundations/Mathematics/Linear-Algebra/Topics-in-Random-Matrix-Theory-Tao.pdf)
- **Probability & Statistics**
  - [All of Statistics (Wasserman, 2004)](./01-Foundations/Mathematics/Probability-Statistics/All-of-Statistics-Wasserman-2004.pdf)
  - [Introduction to Probability Models (Ross)](./01-Foundations/Mathematics/Probability-Statistics/Introduction-to-Probability-Models-Ross.pdf)
  - [Introduction to Mathematical Statistics, 8th Ed (Hogg)](./01-Foundations/Mathematics/Probability-Statistics/Introduction-to-Mathematical-Statistics-8th-Ed-Hogg.pdf)
  - [Introduction to Probability and Statistics (Mendenhall, Beaver)](./01-Foundations/Mathematics/Probability-Statistics/Introduction-to-Probability-and-Statistics-Mendenhall-Beaver.pdf)
  - [Introduction to Econometrics (Stock & Watson, 2020)](./01-Foundations/Mathematics/Probability-Statistics/Introduction-to-Econometrics-Stock-Watson-2020.pdf)
  - [Probability Cheatsheet - CME106 Stanford (Amidi)](./01-Foundations/Mathematics/Probability-Statistics/Probability-Cheatsheet-CME106-Amidi.pdf)
  - [Statistics Cheatsheet - CME106 Stanford (Amidi)](./01-Foundations/Mathematics/Probability-Statistics/Statistics-Cheatsheet-CME106-Amidi.pdf)
- **Numerical Methods**
  - [Numerical Recipes: The Art of Scientific Computing (Press et al., 2007)](./01-Foundations/Mathematics/Numerical-Methods/Numerical-Recipes-Press-et-al-2007.pdf)

#### Computer Science
- **Algorithms**
  - [Introduction to Algorithms, 4th Edition (CLRS)](./01-Foundations/Computer-Science/Algorithms/Introduction-to-Algorithms-4th-Ed-CLRS.pdf)
  - [Algorithm Design (Kleinberg & Tardos)](./01-Foundations/Computer-Science/Algorithms/%28KT%29%20Algorithm%20Design%20by%20Jon%20Kleinberg,%20Eva%20Tardos.pdf)
  - [Algorithms (Jeff Erickson)](./01-Foundations/Computer-Science/Algorithms/Algorithms-JeffE.pdf)
- **System Design**
  - [System Design Interview: An Insider's Guide (Alex Xu)](./01-Foundations/Computer-Science/System-Design/System-Design-Interview-Xu.pdf)

### 02-Network-Science
- **Graph Theory**
  - [Graph Theory (Narsingh Deo)](./02-Network-Science/Graph-Theory/Graph-Theory-Deo.pdf)
- **Complex Networks**
  - [Networks (Mark Newman, 2018)](./02-Network-Science/Complex-Networks/Networks-Newman-2018.pdf)
  - [Networks, Crowds, and Markets (Easley & Kleinberg)](./02-Network-Science/Complex-Networks/Networks-Crowds-and-Markets-Easley-Kleinberg.pdf)
  - [Network Science (Barabási)](./02-Network-Science/Complex-Networks/Network-Science-Barabasi.pdf)
  - [Handbook of Graph Drawing and Visualization (Tamassia, 2013 draft)](./02-Network-Science/Complex-Networks/Handbook%20of%20Graph%20Drawing%20and%20Visualization_%20Draft%20of%202013%20--%20Tamassia%20R_%20%28Ed_%29%20--%202013%20--%20d6e78ba7a942e1219d1be5b603984547%20--%20Anna%E2%80%99s%20Archive.pdf)
- **Network Science 2**
  - [NETS2 - Complex Networks: Principles, Methods and Applications (Latora, Nicosia, Russo)](./02-Network-Science/NETS2%20-%20Complex%20Networks%3A%20Principles%2C%20Methods%20and%20Applications%20%28Latora%2C%20Nicosia%2C%20Russo%29.pdf)
  - [NETS2 - Random Graphs and Complex Networks (van der Hofstad) [Vol 1]](./02-Network-Science/NETS2%20-%20Random%20Graphs%20and%20Complex%20Networks%20%28van%20der%20Hofstad%29%20%5BVol%201%5D.pdf)
  - [NETS2 - Random Graphs and Complex Networks (van der Hofstad) [Vol 2]](./02-Network-Science/NETS2%20-%20Random%20Graphs%20and%20Complex%20Networks%20%28van%20der%20Hofstad%29%20%5BVol%202%5D.pdf)
- **Machine Learning on Graphs**
  - [CS224W: Machine Learning with Graphs (Stanford)](./02-Network-Science/Machine-Learning-on-Graphs/CS224W-Machine-Learning-with-Graphs-Stanford.pdf)
  - [Course README](./02-Network-Science/Machine-Learning-on-Graphs/README.md)
  - [Geometric Deep Learning](https://geometricdeeplearning.com/lectures/)
- **Network Dynamics**
  - [Dynamical Processes on Complex Networks (Barrat et al., 2008)](./02-Network-Science/Network-Dynamics/Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008.pdf)

### 03-Complex-Systems
- **Nonlinear Dynamics & Chaos**
  - [Nonlinear Dynamics and Chaos (Strogatz, 2024)](./03-Complex-Systems/Nonlinear-Dynamics-Chaos/Nonlinear-Dynamics-and-Chaos-Strogatz-2024.pdf)
  - [Nonlinear Dynamics and Chaos - Solutions Manual (Strogatz, 2024)](./03-Complex-Systems/Nonlinear-Dynamics-Chaos/Nonlinear-Dynamics-and-Chaos-Solutions-Manual-Strogatz-2024.pdf)
  - [Study Notes](./03-Complex-Systems/Nonlinear-Dynamics-Chaos/notes/)
- **Urban Science**
  - [Introduction to Urban Science: Evidence and Theory of Cities as Complex Systems (Bettencourt, 2021)](./03-Complex-Systems/Urban-Science/Introduction-to-Urban-Science-Bettencourt-2021.pdf)
- **General Complexity**
  - [Modeling and Analysis of Complex Systems (Sayama)](./03-Complex-Systems/General-Complexity/Modeling-and-Analysis-of-Complex-Systems-Sayama.pdf)
  - More books to add here.

### 04-Applied-Methods
- **Epidemiology**
  - [Mathematics of Epidemics on Networks (Kiss, Miller, Simon)](./04-Applied-Methods/Epidemiology/Mathematics-of-Epidemics-on-Networks-Kiss-Miller-Simon.pdf)
  - [Code Experiments (TSIR Simulation)](./04-Applied-Methods/Epidemiology/code-experiments/)
- **Research Design**
  - [Research Design and Methods: A Process Approach (Bordens & Abbott, 2022)](./04-Applied-Methods/Research-Design/Research-Design-and-Methods-Bordens-Abbott-2022.pdf)

### 05-General-Reading
- [Complexity: A Guided Tour (Melanie Mitchell)](./05-General-Reading/Complexity-A-Guided-Tour-Mitchell.pdf)
- [Scale (Geoffrey West)](./05-General-Reading/Scale-West.pdf)
- [The Nature of Computation (Moore & Mertens)](./05-General-Reading/The-Nature-of-Computation-Moore-Mertens.pdf)
- [The Feeling of Life Itself (Christof Koch)](./05-General-Reading/The-Feeling-of-Life-Itself-Christof-Koch.pdf)

## 🔗 External resources & online courses
### Deep Learning
- [Alice's Experiments in a Differentiable World](https://arxiv.org/pdf/2404.17625) – differentiable programming research
- [Dive Into Deep Learning](https://d2l.ai)

### Complex Systems
- [COSMO: Complex Systems Modeling](https://cosmo-notes.github.io/)

## 🛠️ Tools & aids
1. [jupyter-book](https://jupyterbook.org/en/stable/intro.html) – build books from notebooks
2. [Quarto](https://quarto.org/docs/books/) – scientific and technical publishing
3. [JuliaDynamics](https://juliadynamics.github.io/JuliaDynamics/) – nonlinear dynamics and chaos in Julia
4. [NumPy Cheatsheet](https://gist.github.com/pourmand1376/aa6a8bc4fddda31fecbdf73b2535af21) – quick reference

## Organization and notes
- Books are organized by domain (Foundations → General Reading). Each category mixes PDFs, study notes, and code experiments.
- The viewer/parent messaging enables: page queries for bookmarks, selection/page text extraction for TTS, and theme syncing into the iframe.
- Updating the library: the sidebar is hard-coded in `index.html`; add a new `<div class="file" onclick="loadPDF('URL.pdf', this)">Title</div>` entry under the desired category. The `loadPDF` handler now detects file type: PDFs use the PDF viewer, EPUBs load in the ebook reader, MOBIs try an external inline viewer, and everything else falls back to the general iframe loader. Hosted URLs are supported; relative URLs work when served locally.
- External links that point directly to PDFs/EPUBs open in the viewer. Non-PDF web pages use the iframe loader; some sites block embedding via X-Frame-Options. MOBIs are best converted to EPUB/PDF if the inline external viewer is blocked.
- Track progress in your own study log (repo previously referenced an `AA-MasterLog/` folder). 
