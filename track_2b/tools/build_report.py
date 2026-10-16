#!/usr/bin/env python3
"""Build the five-page report from its maintained Markdown; development tool only."""
import re
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
root=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyReport',fontName='Helvetica',fontSize=10.8,leading=16,spaceAfter=12,textColor=colors.HexColor('#26364a')))
styles['Heading1'].textColor=colors.HexColor('#26364a');styles['Heading1'].fontSize=23;styles['Heading1'].spaceAfter=16
styles['Heading2'].textColor=colors.HexColor('#355f76');styles['Heading2'].fontSize=16;styles['Heading2'].leading=21;styles['Heading2'].spaceAfter=16
story=[]
for page_index,page in enumerate((root/'technical_report.md').read_text().split('<!-- page -->')):
    if page_index:story.append(PageBreak())
    for block in re.split(r'\n\s*\n',page.strip()):
        text=escape(block.replace('\n',' '))
        text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
        if block.startswith('# '):story.append(Paragraph(text[2:],styles['Heading1']))
        elif block.startswith('## '):story.append(Paragraph(text[3:],styles['Heading2']))
        else:story.append(Paragraph(text,styles['BodyReport']))
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#dce0de'));canvas.line(45,43,A4[0]-45,43)
    canvas.setFont('Helvetica',9);canvas.setFillColor(colors.HexColor('#687789'))
    canvas.drawString(45,29,'StimmFolgen | Track 2B | reviewed AHV prototype');canvas.drawRightString(A4[0]-45,29,str(doc.page))
SimpleDocTemplate(str(root/'StimmFolgen_Report.pdf'),pagesize=A4,leftMargin=45,rightMargin=45,topMargin=47,bottomMargin=57,title='StimmFolgen technical report',author='StimmFolgen').build(story,onFirstPage=footer,onLaterPages=footer)
