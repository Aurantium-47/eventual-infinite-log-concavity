#!/usr/bin/env python3
"""Build a review PDF from the accompanying mathematical source chapters.
Requirements: Python 3, Pandoc, XeLaTeX. No network access is used.
"""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, os, re

ROOT=Path(__file__).resolve().parent
SOURCES=['INTRODUCTION.md','FINITE_AND_ALGEBRAIC_PROOF_TYPESET.md','ANALYTIC_PROOF.md','VERIFICATION_APPENDIX.md','REFERENCES.md']

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,default=ROOT/'output'/'pdf')
    args=parser.parse_args()
    for binary in ('pandoc','xelatex'):
        if shutil.which(binary) is None:
            raise SystemExit('Required executable not found: '+binary)
    out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    pieces=[];manifest=[]
    for name in SOURCES:
        path=ROOT/name;data=path.read_bytes()
        manifest.append({'file':name,'sha256':hashlib.sha256(data).hexdigest()})
        pieces.append(data.decode('utf-8').rstrip())
    manuscript=pieces[0]+'\n\n'+pieces[1]+'\n\n\\clearpage\n\n'+'\n\n\\clearpage\n\n'.join(pieces[2:])+'\n'
    manuscript=manuscript.replace('[finite and algebraic chapter](FINITE_AND_ALGEBRAIC_PROOF.md)','finite and algebraic chapter above')
    # Display one long exact constant to prevent an overfull inline-math box.
    manuscript=manuscript.replace(r'\(7405704307825/1693651716<67^2\).',r'\[7405704307825/1693651716<67^2.\]')
    # amsmath tags belong outside aligned; this changes typography only.
    manuscript=re.sub(r'(\\tag\{5\.6\})\s*(\\end\{aligned\})',r'\2 \1',manuscript)
    # Line breaks in the long bulk-error display preserve its exact expression.
    bulk=re.search(r'\\\[\s*(\\frac\{\|f_\{n,4\}.*?\\tag\{7\.1\})\s*\\\]',manuscript,re.S)
    if bulk:
        block=bulk.group(1).replace(' <\\frac{36821}', ' &<\\frac{36821}')
        block=block.replace('    +\\frac12', r' \\ &\quad+\frac12')
        block=block.replace(' =\\frac{18717720003}', r' \\ &=\frac{18717720003}')
        block=block.replace(r'\tag{7.1}', '')
        manuscript=manuscript[:bulk.start()]+r'\['+'\n'+r'\begin{aligned}'+'\n'+block+'\n'+r'\end{aligned}\tag{7.1}'+'\n'+r'\]'+manuscript[bulk.end():]
    md=out/'trinomial_research_draft.md';md.write_text(manuscript)
    tex=out/'trinomial_research_draft.tex'
    header=out/'typesetting_header.tex'
    header.write_text(r'\setlength{\emergencystretch}{3em}'+'\n')
    subprocess.run(['pandoc',str(md),'--from=markdown+tex_math_single_backslash+tex_math_dollars','--standalone',
                    '--to=latex','--toc','--toc-depth=2','--include-in-header',str(header),
                    '-V','geometry:margin=25mm','-V','fontsize=11pt','-V','colorlinks=true',
                    '-V','linkcolor=blue','-V','urlcolor=blue','-o',str(tex)],check=True)
    env=os.environ.copy()
    env['TEXMFVAR']=str(out/'.texlive'/'var')
    env['TEXMFCONFIG']=str(out/'.texlive'/'config')
    # Some minimal containers ship TeX sources but an incomplete filename database.
    if not subprocess.run(['kpsewhich','article.cls'],env=env,capture_output=True,text=True).stdout.strip():
        dist=Path('/usr/share/texlive/texmf-dist')
        if (dist/'tex/latex/base/article.cls').exists():
            env['TEXMF']='{'+str(dist)+',/usr/share/texmf}'
    if (out/'xelatex.fmt').exists():
        env['TEXFORMATS']=str(out)+os.pathsep
    if not subprocess.run(['kpsewhich','xelatex.fmt'],env=env,capture_output=True,text=True).stdout.strip():
        with (out/'format-build.log').open('w') as log:
            subprocess.run(['xetex','-ini','-etex','-jobname=xelatex','-progname=xelatex',
                            '-interaction=nonstopmode','-halt-on-error','xelatex.ini'],
                           cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
        env['TEXFORMATS']=str(out)+os.pathsep
    text=tex.read_text().replace('\\tableofcontents\n}', '\\tableofcontents\n}\n\\clearpage')
    tex.write_text(text)
    for run in (1,2,3):
        with (out/f'xelatex-pass-{run}.log').open('w') as log:
            subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',tex.name],cwd=out,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
    pdf=out/'trinomial_research_draft.pdf'
    report={'source_files':manifest,'manuscript_sha256':hashlib.sha256(md.read_bytes()).hexdigest(),
            'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
            'scope':'Typeset research draft; mathematical source and certificate verification are separate.'}
    (out/'build_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
    print(pdf)

if __name__=='__main__':main()
