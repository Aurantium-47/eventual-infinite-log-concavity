# Building the research draft

Requirements: Python 3, Pandoc, and a working XeLaTeX installation with standard LaTeX/AMS packages and Latin Modern fonts.

```sh
python build_manuscript.py
```

The default outputs are in `output/pdf/`: a combined Markdown snapshot, LaTeX source, PDF, source/output hash manifest, and compiler logs. Use `--output-dir PATH` to choose another writable destination.

The build preserves the source chapters. It applies only documented typesetting transformations: equation-tag placement, line wrapping, display of one long exact constant, an in-document companion-chapter reference, and page-break placement. The finite typeset chapter is a separate transcription of the algebraic source; no original proof source is overwritten.

In minimal containers with incomplete TeX filename databases, the script can use an existing `/usr/share/texlive/texmf-dist` source tree and build the XeLaTeX format locally in the output directory. It does not install packages, access the network, or write system directories. On a normal TeX installation this fallback is unused.

This build command typesets the paper. It does not run the mathematical certificate verification commands in `certificate_package/`.
