
from datetime import date
from decimal import Decimal

from pykasso.abrechnung import abrechnungen_aus_transaktionen


def erstelle_transaktionen_aus_erwartung(erwartung):
    result = []
    for (name, vorname), positionen in erwartung.items():
        for datum, text, wert in positionen:
            result.append(
                {
                    'Date': datum.strftime('%d.%m.%Y'),
                    'Account Name': f'Passiva:Mitglieder:{vorname} {name}',
                    'Description': text,
                    'Full Category Path': 'Aktiva:Bank',
                    'Amount Num': f'{wert:.2f}'.replace('.', ',')
                }
            )

    return result

def pruefe_abrechnungen_gegen_erwartung(abrechnungen, erwartung):
    assert len(abrechnungen) == len(erwartung.keys())

    for abrechnung in abrechnungen:
        erwartete_transaktionen = erwartung[(abrechnung.name, abrechnung.vorname)]

        assert len(abrechnung.positionen) == len(erwartete_transaktionen)

        for ((datum, text, wert), position) in zip(erwartete_transaktionen, abrechnung.positionen):
            assert position.datum == datum
            assert position.text == text
            assert position.wert == wert

#-----------------------------------------------------------------

def test_mehrere_transaktionen_zum_selben_kto():
    erwartung = {
        ('name', 'vorname'): [
            (date(2019, 7, 13), 'Buchungstext 1', Decimal('113.27')),
            (date(2019, 7, 13), 'Buchungstext 2', Decimal('-59.07')),
        ],
    }

    transaktionen = erstelle_transaktionen_aus_erwartung(erwartung)
    abrechnungen = abrechnungen_aus_transaktionen(transaktionen)

    pruefe_abrechnungen_gegen_erwartung(abrechnungen, erwartung)


def test_mehrere_transaktionen_zu_verschiedenen_konten():
    erwartung = {
        ('Name1', 'Vorname1'): [
            (date(2019, 7, 13), 'Buchungstext 1', Decimal('3.27')),
            (date(2019, 7, 14), 'Buchungstext 2', Decimal('13.59')),
            (date(2019, 11, 13), 'Buchungstext 4', Decimal('256.01'))
            ],
        ('Name2', 'Vorname2'): [
            (date(2019, 10, 15), 'Buchungstext 3', Decimal('-59.27'))
        ]
    }

    transaktionen = erstelle_transaktionen_aus_erwartung(erwartung)
    abrechnungen = abrechnungen_aus_transaktionen(transaktionen)

    pruefe_abrechnungen_gegen_erwartung(abrechnungen, erwartung)

def test_ungeordnete_transaktionen_werden_geordnet():
    erwartung = {
        ('Name1', 'Vorname1'): [
            (date(2019, 7, 13), 'Buchungstext 1', Decimal('3.27')),
            (date(2019, 7, 14), 'Buchungstext 2', Decimal('13.59')),
            (date(2019, 11, 13), 'Buchungstext 4', Decimal('256.01'))
            ],
        ('Name2', 'Vorname2'): [
            (date(2019, 10, 15), 'Buchungstext 3', Decimal('-59.27'))
        ]
    }

    _trans = erstelle_transaktionen_aus_erwartung(erwartung)
    _trans_even = [t for i, t in enumerate(_trans) if i % 2 == 0]
    _trans_odd = [t for i, t in enumerate(_trans) if i % 2 == 1]
    abrechnungen = abrechnungen_aus_transaktionen(_trans_even + _trans_odd)

    pruefe_abrechnungen_gegen_erwartung(abrechnungen, erwartung)
