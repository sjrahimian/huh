# Standard library
import json
from pathlib import Path
import sys

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

class JSONCommentDecoder(json.JSONDecoder):
    def __init__(self, **kw):
        super().__init__(**kw)

    def decode(self, s: str):
        s = '\n'.join( line if not line.lstrip().startswith('//') else '' for line in s.split('\n') )
        return super().decode(s)

class Huququllah():
    name = "huquq'u'llah"
    diacritic = "ḥuqúqu'lláh"
    diacritic_capital = "Ḥuqúqu'lláh"
    short = "Hq"
    symbol = "Ͱ"
     
    def __init__(self, metalPrice: float=0.00, metalType: str="", weight: str="oz", unit: str="short"):
        self._PERCENT = 0.19

        # load custom labels from json
        self._labels = { "name": self.name, "symbol": self.symbol, "short": self.short, "diacritic": self.diacritic }
        if (fn:= Path(f"{Path().cwd().parent}\labels.jsonc")).exists():
            with open(fn, 'r') as f:
                self._labels = self._labels | json.load(f, cls=JSONCommentDecoder)
        
        self._mPrice = metalPrice
        self._mType = metalType
        self._weight = weight.lower()
        print(self._labels)
        self._unit = self._labels[unit.lower()]
        self._basic, self._remainder = None, None
        self._calculate_basic_sum()
    
    @property
    def basic(self) -> float:
        return self._basic

    @property
    def remainder(self) -> float:
        return self._remainder
    
    @remainder.setter
    def remainder(self, val: float):
        self._remainder = val

    @property
    def unit(self) -> str:
        """ Selected label """
        return self._unit
    
    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, value: dict):
        self._labels = value | self._labels

    def _calculate_basic_sum(self) -> None:
        """ '...basic sum on which Huqúqu'lláh is payable is nineteen mithqáls of gold.' 
                - BH, #35, Huqúqu'lláh: The Right of God (2007)
        
            Multiplying the cost of gold/gram to 69.192g will calculate 19 mithqāls of 
                gold in dollars, i.e., the basic sum (one Ḥuqúqu'lláh unit).
        
            Conversion:
                19Nk =  1Mq =  3.642g
                361Nk = 19Mq = 69.192g

            Calculation:
                X = gold $ per g * 69.192g
                        or
                X = gold $ per g * 3.642g * 19

            :return None: monetary equivalent to 19 mithqāls of gold (basic sum)
        """
        GRAMS = 69.192
        MITHQAL = 19
        TROY_OZ = 2.22457446

        if self._weight in ("troy ounce", "troy ounces", "troy oz", "oz troy", "t oz", "toz", "oz"):
            factor = TROY_OZ
        elif self._weight in ("gram", "grams", "g"):
            factor = GRAMS
        elif self._weight in ("mithqal", "mithqals", "mq"):
            factor = MITHQAL

        self._basic = self._mPrice * factor


    def payable(self, wealth: float) -> float:
        """ Compute payable amount of Ḥuqúqu'lláh.
            
            (wealth - remainder) * 19%
        
        :param float: Monetary wealth after expenses have been deducted
        
        :return float: Payment owing for Ḥuqúqu'lláh
        """
        if self._basic is None:
            raise ValueError(f"Provide {self._mType} price first to find basic sum amount.")

        if wealth < self._basic:
            return 0.00
        
        # Gives the remainder of wealth that has not reached a full unit (if any)
        try:
            self._remainder = wealth % self._basic
            pay = (wealth - self._remainder) * self._PERCENT
        except ZeroDivisionError:
            raise ValueError(f"[ERROR] Failed to properly calculate {self._unit} basic amount based on {self._mType}.")
            sys.exit(-1)
            # return 0.00

        print(f"Your accrued wealth contains {wealth // self._basic} {self._unit}.")
        print(f"       Amount of wealth that {self._unit} will be payable on: ${format(round((wealth - self._remainder), 2), '.2f')}.")
        print(f"Remainder of wealth that will not have {self._unit} paid: ${round(self._remainder, 2)}.\n\n")
        print("You owe", pay)
        
        return pay

    def __str__(self):
        """ String representation of this object """
        return f"${round(self._basic, 2)}{self._unit}"

