# Standard library
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import sys
import csv

# 3rd Party Library

# Local Imports

"""Symbol Reasoning

    One option is the Greek uppercase Ϙ (qoppa) to repersent Huquq, which decends from the Phoenician Qoph (𐤒), which in turn is 
    ancestor to the Arabic qāf (the twenty-first letter of the Arabic alphabet) and one of the letters in huququ'llah. Qoph is the 
    nineteenth letter of the Semitic abjads, including Phoenician qōp 𐤒, Hebrew qūp̄ ק ‎, Aramaic qop _, Syriac qōp̄ ܩ, 
    and Arabic qāf ق (Wikipedia).

    Another option would be the first letter of "huquq", which is ح (ḥā), a variant of (Ḫāʾ), "the sixth letter of the Arabic alphabet" 
    which is a variation of "Heth, sometimes written Chet, but more accurately Ḥet" and ancestor to the Greek lowercase Ͱ (Wikipedia).

    1 ḥuqúq or huquq (1 "rights") could be defined as the unit amount equal to 19 mithqáls of gold in currency 
    (e.g., $1 huquq = $1/mithqál * 19 mithqáls = $1/g * 69.192g)

"""

@dataclass
class HuququLabels:
    choice: str = "name"

    name: str = "huququ'llah"
    diacritic_lower: str = "ḥuqúqu'lláh"
    diacritic_upper: str = "Ḥuqúqu'lláh"
    unit: str = "hq"
    unit_symbol: str = "Ͱ"
    mithqal: str = "mithqal"
    mithqal_diacritic: str = "mit͟hqál"
    mithqal_unit: str = "mq"
    nakhud: str = "nakhud"
    nakhud_diacritic: str = "nak͟hud"
    nakhud_unit: str = "nh"


    def dict(self):
        return { k: v for k, v in asdict(self).items() }

    def __str__(self):
        return (self.dict())[self.choice]

@dataclass
class Huququllah:
    _PERCENT = 0.19
    _GRAMS = 69.192
    _MITHQAL = 19
    _TROYOZ = 2.22457446

    basic, remainder, payable = None, None, None
    wealth: float = None
    price: float = None
    weight: str = "toz"

    def __init__(self, wealth=None, price=None, weight: str='toz'):
        self.wealth = wealth
        self.price = price
        self.weight = weight

        # Calculate Huququllah
        self._basicSum()
        self._remainder()    # Gives the remainder of wealth that has not reached a full unit (if any)
        self._payable()


    def _basicSum(self) -> float:
        """'...basic sum on which Ḥuqúqu'lláh is payable is nineteen mit͟hqáls of gold.' 
                - BH, #35, Ḥuqúqu'lláh: The Right of God (2007)
        
            Multiplying the cost of gold/gram to 69.192g will calculate 19 mit͟hqáls of 
                gold in dollars, i.e., the basic sum (one unit).

                nh - nak͟hud
                mq - mit͟hqál
                 g - grams
                oz - troy ounce
        
            Conversion:
                 19Nk =  1Mq =  3.642g
                361Nk = 19Mq = 69.192g

            Calculation:
                19 mq = $gold/g * 69.192g
                           or
                19 mq = $gold/g * (3.642g * 19mq)

        Raises:
            ValueError: Not able to determine weight conversion from given unit

        Returns:
            float: basic sum that is equivalent to 19 mit͟hqáls of gold
        """

        if not self.price:
            raise ValueError("Provide gold price to calculate basic sum (equal to 19 mit͟hqáls of gold).")
            sys.exit(1)

        if self.weight in ("troy oz", "t oz", "toz", "oz"):
            factor = self._TROYOZ
        elif self.weight in ("gram", "grams", "g"):
            factor = self._GRAMS
        elif self.weight in ("mithqal", "mithqals", "mq"):
            factor = self._MITHQAL
        else:
            raise ValueError(f"Unrecognized weight provided: {self.weight}")
            sys.exit(1)
        
        self.basic = self.price * factor
        return self.basic

    def _remainder(self) -> float:
        try:
            self.remainder = self.wealth % self.basic
        except ZeroDivisionError:
            print("Basic sum cannot be equal to zero.")
            sys.exit(-1)

    def _payable(self) -> float:
        """Provide the payable amount of Ḥuqúqu'lláh.
            
            (wealth - remainder) * 0.19

        Args:
            wealth (float):  Wealth after expenses have been deducted and that has not had Huququ'llah paid

        Raises:
            ValueError: Missing basic sum (equivalent to 19 mit͟hqáls of gold)

        Returns:
            float: payable amount of Huququ'llah
        """

        if self.basic is None:
            raise ValueError(f"Provide gold price first to find basic sum amount.")

        if self.wealth < self.basic:
            self.payable = 0.00
        else: 
            self.payable = (self.wealth - self.remainder) * self._PERCENT
        
        return self.payable

    def __str__(self):
        """ String representation of this object """
        return f"Payable: ${round(self.payable, 2):.2f}\n"

    def report(self, selected="diacritic_lower"):
        print(f"Accrued wealth is {self.wealth // self.basic}x over the 19{HuququLabels.mithqal_unit} of gold.")
        print(f"Amount of wealth that {HuququLabels(choice=selected)} will be payable on: ${round((self.wealth - self.remainder), 2):.2f}.")
        print(" ~ ~ ~ ")
        print(f"Basic: ${round(self.basic, 2):.2f} (equivalent to 19{HuququLabels.mithqal_unit} of gold)")
        print(f"Remainder of wealth: ${round(self.remainder, 2):.2f} ({HuququLabels.diacritic_lower} not paid)")
        print(f"Payable: ${round(self.payable, 2):.2f}\n")


def record(pkg, file=Path("huququllah_record.csv")):
    with open(file, 'a+', newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(pkg)