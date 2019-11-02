# pylint: disable=no-self-use

from decimal import Decimal

from pykasso.abrechnung import Abrechnung, AbrechnungsPosition


class TestAbrechnungsSaldo:
    def test_betrag_wenn_keine_positionen_vorhanden(self):
        abrechnung = Abrechnung('name', 'vorname', positionen=[])

        assert abrechnung.betrag == 0

    def test_betrag_ueber_alle_positionen(self):
        abrechnung = Abrechnung('name', 'vorname', positionen=[
            AbrechnungsPosition(None, '', Decimal('13.72')),
            AbrechnungsPosition(None, '', Decimal('-113.01')),
            AbrechnungsPosition(None, '', Decimal('99')),
            AbrechnungsPosition(None, '', Decimal('0.10')),
        ])
        assert abrechnung.betrag == sum([pos.wert for pos in abrechnung.positionen])
