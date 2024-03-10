# Standard library
import sys
from typing import List, Tuple

# 3rd Party Library

# Local Imports

class HuquqError(Exception):
    """ Base exception class for errors from this module. """

class HuquqMissingValueError(HuquqError, Exception):
    """ Exception class for calculation errors from this module. """

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

class Huququllah():
    _PERCENT = 0.19
    name_full = "huquq'u'llah"
    name_full_diacritic = "ḥuqúqu'lláh"
    name_full_diacritic_capital = "Ḥuqúqu'lláh"
    name_short = "Hq"
    symbol = "Ͱ"
    labels = { "name": name_full, "symbol": symbol, "short": short, "diacritic": name_full_diacritic }
     
    def __init__(self, metalPrice: float, weight: str="oz", unit: str="short"):
        self._mPrice = metalPrice
        self._weight = weight.lower()
        self._unit = self.labels[unit.lower()]
        self._calculate_basic_sum()
    
    @property
    def basic(self) -> float:
        return self._amount
    
    @huh.setter
    def basic(self, val: float):
        self._amount = val 

    @property
    def remainder(self) -> float:
        return self._remainder
    
    @huh.setter
    def remainder(self, val: float):
        self._remainder = val

    @property
    def unit(self) -> str:
        return self._unit

    def _calculate_basic_sum(self) -> None:
        """ '...basic sum on which Huqúqu'lláh is payable is nineteen mithqáls of gold.' 
                - BH, #35, Huqúqu'lláh: The Right of God (2007)
        
            Multipling the cost of gold/gram to 69.192g will calculate 19 mithqāls of gold in dollars, i.e., the basic sum (one Ḥuqúqu'lláh unit).
        
            Conversion:
                19Nk =  1Mq =  3.642g
                361Nk = 19Mq = 69.192g

            Calculation:
                X = gold $ per g * 69.192g
                        or
                X = gold $ per g * 3.642g * 19

            :return None: montary equivalant to 19 mithqāls of gold (basic sum)
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

        self.basic(self._mPrice * factor)


    def payable(self, wealth: float = None):
        """ Compute payable amount of Ḥuqúqu'lláh.
            
            (wealth - remainder) * 19%
        
        :param float: Monetary wealth after expenses have been deducted
        :return flaot: Payment owing for Ḥuqúqu'lláh
        """

        if not wealth:
            raise MissingHuquqWealthValue("Cannot calculate Ḥuqúqu'lláh without accured wealth.")
        
        if not self.basic:
            raise HuquqMissingValueError("Provide gold price first to find basic sum amount.")
        
        if wealth < self.basic:
            pay = 0.00
        else:
            pay = (wealth - self.remainder) * self._PERCENT

        # Gives the remainder of wealth that has not reached a full unit (if any)
        self.remainder(wealth % self.basic)

        print(f"Wealth contains {wealth // self.basic} basic units of Ḥuqúqu'lláh.")
        print(f"       Amount of wealth that will have {self.unit} paid: ${round((pay / self._PERCENT), 2)}.")
        print(f"Remainder of wealth that will not have {self.unit} paid: ${round(self.remainder, 2)}.\n\n")
        
        return pay

    def __str__(self):
        """ String representation of this object """
        return f"${round(self.basic, 2)}{self.unit}"

