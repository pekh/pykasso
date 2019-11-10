
import csv
import os.path
from typing import List

import click

from .abrechnung import abrechnungen_aus_transaktionen
from .pdf_abrechnung import PDFAbrechnung


DEFAULT_AUSGABEVERZEICHNIS = 'pdfs/'


def schreibe_in_ausgabeverzeichnis(ausgabeverzeichnis: str, pdf_abrechnungen: List[PDFAbrechnung]):
    for abrechnung in pdf_abrechnungen:
        with open(os.path.join(ausgabeverzeichnis, abrechnung.filename), 'wb') as datei:
            abrechnung.erzeuge_dokument()
            datei.write(abrechnung.buffer.getvalue())



@click.command()
@click.argument('transaktionsdatei', type=click.File('r'))
@click.option('-a', '--ausgabeverzeichnis',
              help='Ausgabeverzeichnis für die fertigen Abrechnungen',
              default=DEFAULT_AUSGABEVERZEICHNIS, type=click.Path(exists=True, writable=True))
@click.version_option()
def cli(transaktionsdatei, ausgabeverzeichnis):
    '''
    Werkzeuge zur Erleichterung der Kassenverwaltung

    (c) Jan-Peer Grunwald, pekh@eufrutki.net
    '''
    abrechnungen = abrechnungen_aus_transaktionen(csv.DictReader(transaktionsdatei, delimiter=';'))
    pdf_abrechnungen = map(lambda x: PDFAbrechnung(x.mitglied, x), abrechnungen)

    schreibe_in_ausgabeverzeichnis(ausgabeverzeichnis, pdf_abrechnungen)
