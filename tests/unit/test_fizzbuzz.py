# coding=utf-8
#
# Created by junn, on 2019-09-20
#

from unittest import TestCase
from kata.fizzbuzz import FizzBuzzer, print_fizzbuzz_list


def test_should_print_number():
    fb = FizzBuzzer(1)
    assert fb.to_str() == 1


def test_should_divisible_by_3():
    fb = FizzBuzzer(12)
    assert fb.to_str() == "Fizz"


def test_should_divisible_by_5():
    fb = FizzBuzzer(10)
    assert fb.to_str() == "Buzz"


def test_should_divisible_by_3_and_5():
    fb = FizzBuzzer(15)
    assert fb.to_str() == "FizzBuzz"


class FizzBuzzerTest(TestCase):

    def test_invalid_number(self):
        # fb = FizzBuzzer(0)
        self.assertRaisesRegex(Exception, "Invalid number zero", FizzBuzzer, 0)

    def test_print_fizzbuzz_list(self):
        results = print_fizzbuzz_list(1, 5)
        self.assertListEqual(results, [1, 2, "Fizz", 4, "Buzz"])

        results = print_fizzbuzz_list(14, 20)
        self.assertListEqual(results, [14, "FizzBuzz", 16, 17, "Fizz", 19, "Buzz"])

        results = print_fizzbuzz_list(90, 100)
        self.assertListEqual(results, ["FizzBuzz", 91, 92, "Fizz", 94, "Buzz", "Fizz", 97, 98, "Fizz", "Buzz"])

    def test_exception_sequence_index(self):
        self.assertRaisesRegex(Exception, "The start > end", print_fizzbuzz_list, 5, 1)

    def test_contains_specified_number(self):
         fb = FizzBuzzer(13)
         assert fb.to_str() == "Fizz"

         fb = FizzBuzzer(59)
         assert fb.to_str() == "Buzz"

         fb = FizzBuzzer(51)
         assert fb.to_str() == "FizzBuzz"

         fb = FizzBuzzer(35)
         assert fb.to_str() == "FizzBuzz"

         fb = FizzBuzzer(53)
         assert fb.to_str() == "FizzBuzz"

         fb = FizzBuzzer(533)
         assert fb.to_str() == "FizzBuzz"

