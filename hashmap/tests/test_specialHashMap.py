import pytest
from specialHashMap import SpecialHashMap

@pytest.fixture(scope="function")
def specialHashMap():
    return SpecialHashMap()

class TestSpecialHashMap:
    def test_iloc(self, specialHashMap):
        specialHashMap["val"] = 3
        specialHashMap["1"] = 10
        assert specialHashMap.iloc[0] == 10
        with pytest.raises(ValueError):
            specialHashMap.iloc[2]

    def test_ploc(self, specialHashMap):
        specialHashMap["value1"] = 1
        specialHashMap["value2"] = 2
        specialHashMap["value3"] = 3
        specialHashMap["1"] = 10
        specialHashMap["2"] = 20
        specialHashMap["3"] = 30
        specialHashMap["(1, 5)"] = 100
        specialHashMap["(5, 5)"] = 200
        specialHashMap["(10, 5)"] = 300
        specialHashMap["(1, 5, 3)"] = 400
        specialHashMap["(5, 5, 4)"] = 500
        specialHashMap["(10, 5, 5)"] = 600
        assert specialHashMap.ploc[">=1"] == {1: 10, 2: 20, 3: 30}
        assert specialHashMap.ploc["<3"] == {1: 10, 2: 20}
        assert specialHashMap.ploc[">0, >0"] == {(1, 5): 100, (5, 5): 200, (10, 5): 300}
        assert specialHashMap.ploc[">=10, >0"] == {(10, 5): 300}
        assert specialHashMap.ploc["<5, >=5, >=3"] == {(1, 5, 3): 400}
        assert specialHashMap.ploc["<>1"] == {2: 20, 3: 30}
        assert specialHashMap.ploc["=1"] == {1: 10}
        assert specialHashMap.ploc["<=2"] == {1: 10, 2: 20}
        with pytest.raises(SyntaxError):
            specialHashMap.ploc["f>1"]
        with pytest.raises(SyntaxError):
            specialHashMap.ploc["1, >1"]
        with pytest.raises(SyntaxError):
            specialHashMap.ploc["1>"]