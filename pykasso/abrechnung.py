
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List


@dataclass(eq=True, frozen=True)
class Mitglied:
    name: str
    vorname: str


@dataclass
class AbrechnungsPosition:
    datum: date
    text: str
    wert: Decimal


@dataclass
class Abrechnung:
    mitglied: Mitglied
    positionen: List[AbrechnungsPosition]

    @property
    def betrag(self):
        return sum([pos.wert for pos in self.positionen])


def abrechnungen_aus_transaktionen(transaktionen: List[Dict[str, str]]) -> List[Abrechnung]:
    positionen = defaultdict(list)
    for transaktion in transaktionen:
        vorname, name = transaktion['Account Name'].split(':')[-1].split(' ')
        positionen[Mitglied(name, vorname)].append(
            AbrechnungsPosition(
                datum=datetime.strptime(transaktion['Date'], '%d.%m.%Y').date(),
                text=transaktion['Description'],
                wert=Decimal(transaktion['Amount Num.'].replace(',', '.')),
                )
            )

    result = []
    for mitglied, a_positionen in positionen.items():
        result.append(
            Abrechnung(mitglied, positionen=sorted(a_positionen, key=lambda x: x.datum))
            )

    return result
