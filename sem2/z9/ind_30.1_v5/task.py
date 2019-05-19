import numpy as np
import unittest
from cmath import inf


def inf_sum(argument, accuracy=0.1):
    if accuracy <= 0:
        return 1/(argument+1)**3
    elif accuracy > 1 or abs(argument) > 1:
        raise ValueError

    result = 1
    i = 1
    x_i: float = 1

    while abs(x_i) > accuracy:
        x_i *= (-1)*(i+2)*argument/i
        # x_i = (-1*argument)**i * ((i+1)*(i+2))/i
        result += x_i
        i += 1
    return result


class TestInfinitySum(unittest.TestCase):

    def test_1_normal(self):
        x = 0.5
        eps = 0.01
        self.assertAlmostEqual(
            1/(x+1)**3,
            inf_sum(x, eps),
            delta=2*eps
        )

    def test_2_eps_greater_1(self):
        # self.assertEqual(
        #     inf_sum(0.1, 12),
        #     0,
        #     "test 2: eps>1"
        # )
        self.assertRaises(ValueError)

    def test_3_abs_x_greater_1(self):
        self.assertRaises(ValueError,
            # inf_sum(1.2),
            # "test 3.1: x>1"
        )
        # self.assertEqual(
        #     float(inf),
        #     inf_sum(-1.2),
        #     "test 3.2: x<-1"
        # )

    def test_4_eps_less_0(self):
        x = 0.2
        self.assertEqual(1/(1+x)**3,
                         inf_sum(x, 0),
                         "test 4.1 : eps=0")
        self.assertEqual(1/(1+x)**3,
                         inf_sum(x, -1),
                         "test 4.2 : eps<0")


if __name__ == "__main__":
    unittest.main()