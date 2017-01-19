
import pytest
from wavefront_reader import parse_mixed_delim_str


@pytest.mark.parametrize("fstr, farray", [('1/3/5 2/4/6 3/5/7', [(1, 2, 3), (3, 4, 5), (5, 6, 7)]),
                                          ('1//10 2//20 3//30', [(1, 2, 3), (), (10, 20, 30)]),
                                          ('1 2 3', [(1, 2, 3), (), ()]),
                                          ('1/10 2/20 3/30', [(1, 2, 3), (10, 20, 30), ()]),
                                          ('1 2 3 4', [(1, 2, 3, 4), (), ()])])
def test_all_coords_present(fstr, farray):
    out = parse_mixed_delim_str(fstr)
    assert out == farray


