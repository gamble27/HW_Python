import unittest
from program import inf_sum
import numpy as np
from cmath import inf


class TestInfinitySum(unittest.TestCase):
    def test_1_normal(self):
        for eps in np.arange(0.1, 0.5, 0.1):
            for x in np.linspace(0, eps, 5)[1:-1]:
                with self.subTest(eps=eps, x=x):
                    self.assertAlmostEqual(
                        np.log(
                            (1+x)/(1-x)
                            ),
                        inf_sum(x, eps),
                        delta=2*eps
                        )

    def test_2_eps_greater_1(self):
        self.assertEqual(
            inf_sum(0.1, 12),
            0,
            "test 2: eps>1"
        )

    def test_3_abs_x_greater_1(self):
        self.assertEqual(
            float(inf),
            inf_sum(1.2),
            "test 3.1: x>1"
        )
        self.assertEqual(
            float(inf),
            inf_sum(-1.2),
            "test 3.2: x<-1"
        )

    def test_4_eps_less_0(self):
        x = 0.2
        self.assertEqual(np.log((1+x)/(1-x)),
                         inf_sum(x, 0),
                         "test 4.1 : eps=0")
        self.assertEqual(np.log((1+x)/(1-x)),
                         inf_sum(x, -1),
                         "test 4.2 : eps<0")


if __name__ == "__main__":
    unittest.main()
