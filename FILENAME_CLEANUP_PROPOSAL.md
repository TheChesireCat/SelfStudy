# Book Filename Cleanup Proposal

## Current vs. Proposed Filenames

### 01-Foundations/Mathematics/Calculus/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Vec_Cal2.pdf` | `Vector-Calculus-2.pdf` | Abbreviated, unclear |
| `multivariable.pdf` | `Multivariable-Calculus.pdf` | Too generic |

### 01-Foundations/Mathematics/Linear-Algebra/
| Current | Proposed | Issues |
|---------|----------|--------|
| `LinearAlgebraMultiVar-lamv.pdf` | `Linear-Algebra-and-Multivariable-Calculus.pdf` | Mixed case, unclear abbreviation |
| `linear-guest.pdf` | `Linear-Algebra-Guest.pdf` | Too generic, lowercase |
| `matrix-book.pdf` | `Matrix-Methods.pdf` | Too generic |

### 01-Foundations/Mathematics/Probability-Statistics/
| Current | Proposed | Issues |
|---------|----------|--------|
| `2004 - wasserman - all of statistics.pdf` | `All-of-Statistics-Wasserman-2004.pdf` | Inconsistent format, spaces |
| `Econometrics-James-H.-Stock-Mark-W.-Watson-Introduction-to-Econometrics-Global-Edition-Pearson-Education-Limited-2020.pdf` | `Introduction-to-Econometrics-Stock-Watson-2020.pdf` | Way too long, includes publisher |
| `cheatsheet-probability.pdf` | `Probability-Cheatsheet.pdf` | Lowercase, inconsistent |
| `cheatsheet-statistics.pdf` | `Statistics-Cheatsheet.pdf` | Lowercase, inconsistent |
| `introduction-to-probability-model-s.ross-math-cs.blog_.ir_.pdf` | `Introduction-to-Probability-Models-Ross.pdf` | Has website domain in name |
| `statbook2.pdf` | `Statistics-Book-2.pdf` | Too generic, no caps |
| `william_mendenhall_robert_j-_beaver_barbara_m-_bookfi-org.pdf` | `Introduction-to-Probability-and-Statistics-Mendenhall-Beaver.pdf` | Has website, underscores, no title |

### 01-Foundations/Mathematics/Numerical-Methods/
| Current | Proposed | Issues |
|---------|----------|--------|
| `William H. Press, Saul A. Teukolsky, William T. Vetterling, Bria - Numerical recipes_ the art of scientific computing (2007, Cambridge University Press) - libgen.li.pdf` | `Numerical-Recipes-Press-et-al-2007.pdf` | Extremely long, has website |

### 01-Foundations/Computer-Science/Algorithms/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Introduction.to.Algorithms.4th.Leiserson.Stein.Rivest.Cormen.MIT.Press.pdf` | `Introduction-to-Algorithms-4th-Ed-CLRS.pdf` | Dots instead of dashes, includes publisher |

### 01-Foundations/Computer-Science/System-Design/
| Current | Proposed | Issues |
|---------|----------|--------|
| `System Design Interview An Insider's Guide by Alex Xu (z-lib.org).pdf` | `System-Design-Interview-Alex-Xu.pdf` | Spaces, has website |

### 02-Network-Science/Graph-Theory/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Graph Theory Narsingh DEO.pdf` | `Graph-Theory-Narsingh-Deo.pdf` | Spaces, all caps last name |

### 02-Network-Science/Complex-Networks/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Introduction to the Modeling and Analysis of Complex Systems.pdf` | `Modeling-and-Analysis-of-Complex-Systems-Sayama.pdf` | Spaces, too long |
| `Mark Newman - Networks (2018, Oxford University Press).pdf` | `Networks-Newman-2018.pdf` | Author first, has publisher |
| `Networks, Crowds, and Markets (Easley and Kleinberg).pdf` | `Networks-Crowds-and-Markets-Easley-Kleinberg.pdf` | Commas, parentheses |
| `Newman_Networks.pdf` | `Networks-Newman-Alt.pdf` | Underscore, duplicate (different edition) |
| `vdoc.pub_network-science.pdf` | `Network-Science-Barabasi.pdf` | Has website domain |

### 02-Network-Science/Network-Dynamics/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Barrat_et_al_2008_Dynamical_Processes_on_Complex_Networks.pdf` | `Dynamical-Processes-on-Complex-Networks-Barrat-et-al-2008.pdf` | Underscores, mixed case |

### 03-Complex-Systems/Nonlinear-Dynamics-Chaos/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Book-Steven H Strogatz - Nonlinear Dynamics and Chaos_ With Applications to Physics, Biology, Chemistry, and Engineering-Chapman and Hall_CRC (2024).pdf` | `Nonlinear-Dynamics-and-Chaos-Strogatz-2024.pdf` | Way too long, has publisher, "Book-" prefix |
| `Sol-Mitchal Dichter,  Steven H. Strogatz - Student Solutions Manual for Non Linear Dynamics and Chaos_ With Applications to Physics, Biology, Chemistry, and Engineering-Routledge, CRC Press (2024).pdf` | `Nonlinear-Dynamics-and-Chaos-Solutions-Manual-Strogatz-2024.pdf` | Extremely long, "Sol-" prefix, has publisher |

### 03-Complex-Systems/Urban-Science/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Luís M. A. Bettencourt - Introduction to Urban Science Evidence and Theory of Cities as Complex Systems-The MIT Press (2021).pdf` | `Introduction-to-Urban-Science-Bettencourt-2021.pdf` | Long, has publisher, special characters |

### 04-Applied-Methods/Epidemiology/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Mathematics of Epidemics on Networks.pdf` | `Mathematics-of-Epidemics-on-Networks-Kiss-et-al.pdf` | Spaces, missing authors |

### 04-Applied-Methods/Research-Design/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Kenneth S. Bordens, Bruce B. Abbott - Research Design and Methods_ A Process Approach-McGraw Hill (2022).pdf` | `Research-Design-and-Methods-Bordens-Abbott-2022.pdf` | Long, has publisher |

### 05-General-Reading/
| Current | Proposed | Issues |
|---------|----------|--------|
| `Complexity_ A Guided Tour - Melanie Mitchell.pdf` | `Complexity-A-Guided-Tour-Mitchell.pdf` | Underscore after title |
| `Scale - Geoffrey West.pdf` | `Scale-West.pdf` | Spaces, dash |
| `The Nature of Computation -- Cristopher Mo - Unknown.pdf` | `The-Nature-of-Computation-Moore.pdf` | Double dash, "Unknown", truncated author |

---

## Naming Conventions Applied

1. **Format**: `Title-Author-Year.pdf` (when available)
2. **Separators**: Hyphens only (no spaces, underscores, or dots)
3. **Capitalization**: Title case for main words
4. **Remove**: Publishers, websites (z-lib.org, libgen.li, etc.), prefixes like "Book-" or "Sol-"
5. **Shorten**: Long subtitles removed
6. **Author format**: Last-name or Last-name-et-al for multiple authors
7. **Editions**: Include only when relevant (e.g., "4th-Ed")
8. **Duplicates**: Add "-Alt" suffix for alternative editions

---

## Benefits

- ✅ Consistent naming across all files
- ✅ No spaces (better for command line)
- ✅ No special characters or website domains
- ✅ Easier to identify books at a glance
- ✅ Sorted alphabetically within folders
- ✅ Professional appearance
- ✅ Year included for version tracking

---

## Statistics

- **Total files to rename**: 28 PDFs
- **Average length reduction**: ~40 characters
- **Files with website domains**: 4
- **Files with publisher info**: 8
- **Files with inconsistent formatting**: 20+

---

## Notes for Special Cases

1. **Newman Networks**: Two versions exist. Kept as `Networks-Newman-2018.pdf` and `Networks-Newman-Alt.pdf`
2. **Cheatsheets**: Kept as reference materials with "Cheatsheet" in name
3. **Solutions Manual**: Clearly marked to distinguish from main textbook
4. **Author names**: Used commonly recognized forms (e.g., "CLRS" for algorithms book)
5. **Special characters**: Removed accents from "Luís" → plain ASCII

