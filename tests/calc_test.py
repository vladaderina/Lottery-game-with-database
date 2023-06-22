from unittest import TestCase, main
from calc import calc

class CalcTest(TestCase):
    def test_plus(self):
        self.assertEqual(calc('2+2'), 4)
    def test_minus(self):
        self.assertEqual(calc('3-1'), 2)
    def test_mult(self): 
        self.assertEqual(calc('3*9'), 27)
    def test_dev(self):
        self.assertEqual(calc('3/1'), 3)
    def test_no_signs(self):
        with self.assertRaises(ValueError)as e:
            calc('qwerty')
        self.assertEqual('Выражение должно содержать оператор', e.exception.args[0])
    def test_many_signs(self):
        with self.assertRaises(ValueError)as e:
            calc('1+2-3/4*5')
        self.assertEqual('Выражение должно содержать только 2 целых числа и 1 знак', e.exception.args[0])
    def test_float(self):
        with self.assertRaises(ValueError)as e:
            calc('2.2+4.3')
        self.assertEqual('Выражение должно содержать только 2 целых числа и 1 знак', e.exception.args[0])
    def test_string(self):
        with self.assertRaises(ValueError) as e:
            calc('a+b')
        self.assertEqual('Выражение должно содержать только 2 целых числа и 1 знак', e.exception.args[0])
if __name__ == '__main__':
    calc()