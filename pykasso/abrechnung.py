
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Dict, List


@dataclass
class AbrechnungsPosition:
    datum: date
    text: str
    wert: Decimal


@dataclass
class Abrechnung:
    name: str
    vorname: str
    positionen: List[AbrechnungsPosition]


def abrechnungen_aus_transaktionen(transaktionen: List[Dict[str, str]]) -> List[Abrechnung]:
    positionen = defaultdict(list)
    for transaktion in transaktionen:
        vorname, name = transaktion['Account Name'].split(':')[-1].split(' ')
        positionen[(name, vorname)].append(
            AbrechnungsPosition(
                datum=datetime.strptime(transaktion['Date'], '%d.%m.%Y').date(),
                text=transaktion['Description'],
                wert=Decimal(transaktion['Amount Num'].replace(',', '.')),
                )
            )

    result = []
    for (name, vorname), a_positionen in positionen.items():
        result.append(Abrechnung(vorname=vorname, name=name, positionen=a_positionen))

    return result
