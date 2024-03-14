from huh.huquq import Huququllah

def test_huquq():
    h = Huququllah(metalPrice=1)
    assert h.basic >= 0.0
    assert h.unit == "Hq"
    assert h.remainder == None
    assert h.payable(0.00) == 0.00