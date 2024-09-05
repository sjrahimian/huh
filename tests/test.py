from huh.huquq import Huququllah
from math import floor

def test_class_huquq():
    h = Huququllah(metalPrice=1)
    assert h.basic >= 0.0
    assert h.unit == "Hq"
    assert h.remainder == None
    assert h.payable(0.00) == 0.00

def test_class_huquqlabel():
    assert HuququLabels() == "huquq"
    assert HuququLabels(default="nakhud_diacritic") == "nak͟hud"

def test_huquqllah_calc():
    huq = Huququllah("1000", "500", "toz", "USD")
    assert floor(huq.basic) == 1112
    assert floor(huq.remainder) == 1000
    assert floor(huq.payable) == 0

    huq = Huququllah("1200", "500", "toz", "USD")
    assert floor(huq.remainder) == 87
    assert floor(huq.payable) == 0

    huq = Huququllah("2000", "500", "toz", "USD")
    assert floor(huq.remainder) == 887
    assert floor(huq.payable) == 211

def test_huquqllah_calc_weights():
    huq_troyoz = Huququllah("1500", "500", "toz", "USD")
    huq_gram = Huququllah("1500", "16.08", "toz", "USD")

    assert floor(huq_troyoz.basic) == floor(huq_gram.basic)
    assert floor(huq_troyoz.remainder) == floor(huq_gram.remainder)
    assert floor(huq_troyoz.payable) == floor(huq_gram.payable)
