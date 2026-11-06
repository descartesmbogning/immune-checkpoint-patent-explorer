"""Build the medRxiv files (Word and PDF) from paper/manuscript/*.md.

Needs pandoc, LibreOffice (soffice) and python-docx. Run from the repository root:
    python scripts/build_manuscript.py
Output: paper/manuscript/build/{manuscript,supplementary}.{docx,pdf}
"""
import subprocess
from pathlib import Path

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "manuscript"
OUT = SRC / "build"
OUT.mkdir(exist_ok=True)


def border(el, edges, sz=8, color="000000"):
    b = OxmlElement("w:tblBorders" if el.tag.endswith("tblPr") else "w:tcBorders")
    for e in edges:
        x = OxmlElement(f"w:{e}")
        x.set(qn("w:val"), "single"); x.set(qn("w:sz"), str(sz)); x.set(qn("w:color"), color)
        b.append(x)
    el.append(b)


def field(par, instr):
    for kind, text in (("begin", None), (None, instr), ("end", None)):
        r = par.add_run()
        if kind:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), kind); r._r.append(f)
        else:
            t = OxmlElement("w:instrText"); t.set(qn("xml:space"), "preserve"); t.text = text; r._r.append(t)


def polish(path: Path, footer_text: str) -> None:
    d = docx.Document(path)
    for t in d.tables:
        tblPr = t._tbl.tblPr
        for old in tblPr.findall(qn("w:tblBorders")):
            tblPr.remove(old)
        border(tblPr, ["top", "bottom"], sz=10)
        for i, row in enumerate(t.rows):
            # keep rows together and repeat header row
            trPr = row._tr.get_or_add_trPr()
            cant = OxmlElement("w:cantSplit"); trPr.append(cant)
            if i == 0:
                h = OxmlElement("w:tblHeader"); trPr.append(h)
            for cell in row.cells:
                if i == 0:
                    border(cell._tc.get_or_add_tcPr(), ["bottom"], sz=6)
                for p in cell.paragraphs:
                    p.paragraph_format.space_after = Pt(1); p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.line_spacing = 1.0
                    if i < len(t.rows) - 1:
                        p.paragraph_format.keep_with_next = True
                    for r in p.runs:
                        r.font.size = Pt(8.5)
                        if i == 0:
                            r.font.bold = True
    # table captions stay with their table; figures stay with their caption
    for p in d.paragraphs:
        if p.style.name in ("Table Caption", "Captioned Figure") or p._p.xpath(".//w:drawing"):
            p.paragraph_format.keep_with_next = True
        if p.style.name in ("Table Caption", "Image Caption"):
            p.paragraph_format.keep_together = True
            for r in p.runs:
                r.font.italic = False
    # a table's heading and caption stay on the same page as the table
    for t in d.tables:
        prev = t._tbl.getprevious()
        for _ in range(3):
            if prev is None or prev.tag != qn("w:p"):
                break
            docx.text.paragraph.Paragraph(prev, t._parent).paragraph_format.keep_with_next = True
            prev = prev.getprevious()
    # breathing room after each table
    for t in d.tables:
        nxt = t._tbl.getnext()
        if nxt is not None and nxt.tag == qn("w:p"):
            docx.text.paragraph.Paragraph(nxt, t._parent).paragraph_format.space_before = Pt(10)
    sec = d.sections[0]
    fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run(footer_text + "  ·  page "); r.font.size = Pt(8)
    field(fp, "PAGE")
    for r in fp.runs:
        r.font.size = Pt(8)
    d.save(path)


def build(name: str, footer: str) -> None:
    docx_path = OUT / f"{name}.docx"
    subprocess.run(["pandoc", str(SRC / f"{name}.md"), "-o", str(docx_path), "--reference-doc", str(SRC / "reference.docx"),
                    "--resource-path", str(SRC)], check=True)
    polish(docx_path, footer)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(docx_path)],
                   check=True, capture_output=True)


if __name__ == "__main__":
    build("manuscript", "Mbogning Fonkou · China's rise in immune checkpoint patents · preprint")
    build("supplementary", "Supplementary material · China's rise in immune checkpoint patents")
    for f in sorted(OUT.iterdir()):
        print(f.name, f.stat().st_size)
