
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, NextPageTemplate, PageTemplate, Paragraph

from .abrechnung import Abrechnung, Mitglied

DEBUG = True
PAGE_WIDTH, PAGE_HEIGHT = A4
DOC_FONT = ('Helvetica', 10)

STD_PAR_STYLE = ParagraphStyle(
    'STD_PAR_STYLE',
    spaceAfter=5*mm,
    )



PDF_AUTHOR = f'Vereinsname - Kassenwart'
ABSENDER = [
    'Vereinsname Zeile 1',
    'Vereinsname Zeile 2',
    'Strasse Hnr',
    'PLZ Ort'
]



class PDFAbrechnung:

    def __init__(self, empfaenger: Mitglied, abrechnung: Abrechnung, buffer=BytesIO()):
        self._abrechnung = abrechnung
        self._empfaenger = empfaenger
        self._buffer = buffer

        first_page_tpl = PageTemplate(
            id='first_page_tpl',
            onPage=self._first_page_static,
            frames=[
                Frame(
                    x1=10*mm, y1=15*mm, width=PAGE_WIDTH - 20*mm, height=PAGE_HEIGHT - 105*mm,
                    showBoundary=DEBUG, id='mainFrame',
                ),
            ]
        )
        next_page_tpl = PageTemplate(
            id='next_page_tpl',
            onPage=self._next_page_static,
            frames=[
                Frame(
                    x1=10*mm, y1=15*mm, width=PAGE_WIDTH - 20*mm, height=PAGE_HEIGHT - 25*mm,
                    showBoundary=DEBUG, id='mainFrame'
                ),
            ]
        )

        self.doc = BaseDocTemplate(
            self._buffer,
            pagesize=A4,
            pageTemplates=[first_page_tpl, next_page_tpl],
            showBoundary=DEBUG,
            title=f'Abrechnung für {self.filename}',
            author=PDF_AUTHOR,
            # Die folgenden sind nur für nicht-flowables interessant:
            # (falls überhaupt)
            leftMargin=10*mm,
            rightMargin=10*mm,
            topMargin=10*mm,
            bottomMargin=10*mm,
            #
        )

        self._elements = [NextPageTemplate('next_page_tpl')]

    def _first_page_static(self, canvas, doc):
        canvas.saveState()
        self._draw_multiline_text(canvas, 10*mm, PAGE_HEIGHT-10*mm, 5*mm, ABSENDER)

        empfaenger_daten = [
            f'{self._empfaenger.vorname} {self._empfaenger.name}',
            self._empfaenger.strasse,
            f'{self._empfaenger.plz} {self._empfaenger.ort}',
            self._empfaenger.land
        ]
        self._draw_multiline_text(canvas, 10*mm, PAGE_HEIGHT-50*mm, 5*mm, empfaenger_daten)

        canvas.restoreState()

    def _next_page_static(self, canvas, doc):
        canvas.saveState()
        # doc.page
        canvas.restoreState()

    def _draw_multiline_text(self, canvas, start_x, start_y, step, lines, font=DOC_FONT):
        canvas.setFont(*font)
        canvas.setFont(*DOC_FONT)

        pos_y = start_y

        for line in lines:
            canvas.drawString(start_x, pos_y, line)
            pos_y -= step

    def erzeuge_dokument(self):
        self._elements.append(Paragraph(self.filename, STD_PAR_STYLE))
        for pos in self._abrechnung.positionen:
            self._elements.append(Paragraph(f'{pos.text}', STD_PAR_STYLE))
        self.doc.build(self._elements)

    @property
    def buffer(self):
        return self._buffer

    @property
    def filename(self):
        return f'{self._empfaenger.vorname} {self._empfaenger.name}.pdf'
