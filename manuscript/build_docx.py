#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build manuscript.docx and cover_letter.docx/.md from the project markdown.

Times New Roman 12pt throughout, journal-style headings, embedded figures,
rendered tables, and a GigaScience cover letter.
"""
import os
import re
from datetime import date

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANU = os.path.join(ROOT, "manuscript", "manuscript.md")
REPO = "https://github.com/yyx-4113/matrix-stiffness-neuropathic-pain"
TAG = "v1.0.0"


def set_base_style(doc):
    st = doc.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st.element.rPr.rFonts.set(__import__("docx.oxml.ns", fromlist=["qn"]).qn("w:eastAsia"), "Times New Roman")


def add_formatted(par, text):
    """Apply **bold**, *italic*, `code` inline formatting to a paragraph."""
    pat = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`")
    last = 0
    for m in pat.finditer(text):
        if m.start() > last:
            par.add_run(text[last:m.start()])
        g = m.groups()
        if g[0] is not None:
            r = par.add_run(g[0]); r.bold = True
        elif g[1] is not None:
            r = par.add_run(g[1]); r.italic = True
        elif g[2] is not None:
            r = par.add_run(g[2]); r.font.name = "Courier New"
        last = m.end()
    if last < len(text):
        par.add_run(text[last:])


def build_manuscript():
    doc = Document()
    set_base_style(doc)
    lines = open(MANU, encoding="utf-8").read().splitlines()

    seen_heading = False
    seen_hr = False
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        # title
        if line.startswith("# ") and not seen_heading:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(line[2:]); r.bold = True; r.font.size = Pt(16)
            i += 1
            continue
        # horizontal rule
        if stripped == "---":
            seen_hr = True
            i += 1
            continue
        # headings
        if line.startswith("### "):
            seen_heading = True
            p = doc.add_paragraph(); r = p.add_run(line[4:]); r.bold = True; r.font.size = Pt(12)
            i += 1
            continue
        if line.startswith("## "):
            seen_heading = True
            p = doc.add_paragraph(); p.space_before = Pt(6)
            r = p.add_run(line[3:]); r.bold = True; r.font.size = Pt(13)
            i += 1
            continue
        # image
        if line.startswith("!["):
            m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
            if m:
                caption, rel = m.group(1), m.group(2)
                img = os.path.normpath(os.path.join(ROOT, "manuscript", rel))
                if os.path.isfile(img):
                    try:
                        doc.add_picture(img, width=Inches(6.0))
                        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
                    except Exception as e:
                        doc.add_paragraph(f"[figure missing: {rel} ({e})]")
                else:
                    doc.add_paragraph(f"[figure missing: {rel}]")
                cap = doc.add_paragraph()
                cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cr = cap.add_run(caption); cr.italic = True; cr.font.size = Pt(10)
            i += 1
            continue
        # table
        if stripped.startswith("|") and i + 1 < n and lines[i + 1].strip().startswith("|"):
            rows = [stripped]
            j = i + 1
            while j < n and lines[j].strip().startswith("|"):
                rows.append(lines[j].strip()); j += 1
            # header = rows[0], separator = rows[1], data = rest
            def cells(rw):
                return [c.strip() for c in rw.strip("|").split("|")]
            header = cells(rows[0])
            data = [cells(r) for r in rows[2:]]
            tbl = doc.add_table(rows=1, cols=len(header))
            tbl.style = "Table Grid"
            for k, h in enumerate(header):
                c = tbl.rows[0].cells[k]
                c.text = ""
                add_formatted(c.paragraphs[0], h)
                for rn in c.paragraphs[0].runs: rn.bold = True
            for drow in data:
                cells_row = tbl.add_row().cells
                for k, val in enumerate(drow):
                    cells_row[k].text = ""
                    add_formatted(cells_row[k].paragraphs[0], val)
            # footnote line(s) after table (italic note starting with *)
            i = j
            continue
        # blank
        if stripped == "":
            i += 1
            continue
        # author / affiliation lines (before first heading/hr)
        if not seen_heading and not seen_hr:
            p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_formatted(p, stripped)
            i += 1
            continue
        # normal paragraph (incl. italic footnote lines starting with *)
        p = doc.add_paragraph()
        add_formatted(p, stripped)
        if stripped.startswith("*") and stripped.endswith("*"):
            for rn in p.runs: rn.italic = True; rn.font.size = Pt(10)
        i += 1

    out = os.path.join(ROOT, "manuscript", "manuscript.docx")
    doc.save(out)
    print("wrote", out)
    return out


def build_cover():
    doc = Document()
    set_base_style(doc)
    today = date(2026, 10, 21).strftime("%B %d, %Y")

    def P(text="", align=None, bold=False, italic=False, size=12):
        p = doc.add_paragraph()
        if align is not None: p.alignment = align
        r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        return p

    P(today)
    P()
    P("The Editor-in-Chief")
    P("GigaScience")
    P("Oxford Academic / GigaScience Press")
    P()
    P("Dear Editor,")
    P()
    add_formatted(doc.add_paragraph(),
        "Please consider our Research Article entitled \u201cA controlled stiffness signature does "
        "not transfer to neuropathic-pain transcriptomes, while established ECM gene sets retain "
        "tissue specificity\u201d for publication in GigaScience.")
    P()
    add_formatted(doc.add_paragraph(),
        "We report a prospectively specified, two-stage reanalysis testing whether a "
        "mechanically controlled (substrate-stiffness) transcriptional programme, derived from "
        "HEK293A (GSE98547), engages pain-relevant tissues (dorsal root ganglion, spinal cord) after "
        "nerve injury. The signature was biologically anchored (CTGF \u0394 = +1.64, P = 9.5 \u00d7 10\u207b\u2076) "
        "and the pipeline\u2019s sensitivity was confirmed by a literature-derived nerve-injury gene set "
        "(Hedges g = 3.85, P = 0.0286). The pre-registered conclusion is that the HEK293A-derived "
        "stiffness programme does not transfer to injured DRG (bounded, sensitivity-validated null), "
        "whereas, once baseline-expression confounding is controlled, established ECM / "
        "mechanotransduction gene sets retain tissue specificity in pain transcriptomes (4/5 sets show "
        "stronger DRG-than-blood shift). The work is thus both a negative result (the projected "
        "signature fails) and a positive, methodology-driven correction to prior \u201cECM enrichment in "
        "pain\u201d interpretations \u2014 a fit for GigaScience\u2019s readership, which values rigour, open "
        "data, and reusable analytical workflows.")
    P()
    add_formatted(doc.add_paragraph(),
        "We confirm this work is original, has not been published, and is not under consideration "
        "elsewhere. We used only de-identified public data (GSE98547, GSE111216, GSE261676); no new "
        "human or animal subjects were enrolled, so no IRB/ethics approval was required. All analysis "
        "code, configuration, and result artifacts are deposited at " + REPO + " (tag " + TAG + ") with a "
        "checksummed MANIFEST, satisfying the journal\u2019s open-data mandate. There are no competing "
        "interests and no funding to declare.")
    P()
    P("Thank you for your consideration.")
    P()
    P("Sincerely,")
    P()
    P("Yongxin Yang, B.M.")
    P("The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China")
    P("ORCID: 0009-0004-9698-6552")

    out = os.path.join(ROOT, "manuscript", "cover_letter.docx")
    doc.save(out)
    print("wrote", out)

    # also emit a markdown cover letter for the record
    md = f"""# Cover letter \u2014 GigaScience

{today}

The Editor-in-Chief
GigaScience
Oxford Academic / GigaScience Press

Dear Editor,

Please consider our Research Article entitled "A controlled stiffness signature does not transfer to
neuropathic-pain transcriptomes, while established ECM gene sets retain tissue specificity" for
publication in GigaScience.

[body: prospectively specified reanalysis; HEK293A-derived stiffness signature does not transfer to
injured DRG (bounded, sensitivity-validated null); established ECM/mechanotransduction sets retain
tissue specificity once baseline-expression confounding is controlled (4/5 DRG > blood). Methodology-
driven correction to prior "ECM enrichment in pain" interpretations; fit for GigaScience's open-data,
reusable-workflow readership.]

We confirm the work is original, not published, and not under consideration elsewhere. Only de-identified
public data were used (GSE98547, GSE111216, GSE261676); no IRB/ethics approval required. All code,
configuration, and result artifacts are deposited at {REPO} (tag {TAG}) with a checksummed MANIFEST. No
competing interests; no funding.

Sincerely,
Yongxin Yang, B.M.
The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China
ORCID: 0009-0004-9698-6552
"""
    mdout = os.path.join(ROOT, "manuscript", "cover_letter.md")
    open(mdout, "w", encoding="utf-8").write(md)
    print("wrote", mdout)


if __name__ == "__main__":
    build_manuscript()
    build_cover()
