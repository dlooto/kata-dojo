# coding=utf-8
#
# Created by junn, on 2019-09-20
#


class FizzBuzzer:

    def __init__(self, number):
        self.number = number
        if self.number == 0:
            raise Exception("Invalid number zero")

    def to_str(self):
        if self.is_divisible_by_3_and_5():
            return "FizzBuzz"
        if self.is_divisible_by_3():
            return "Fizz"
        if self.is_divisible_by_5():
            return "Buzz"

        return self.number

    def is_divisible_by_3(self):
        return self.number % 3 == 0

    def is_divisible_by_5(self):
        return self.number % 5 == 0

    def is_divisible_by_3_and_5(self):
        return self.is_divisible_by_3() and self.is_divisible_by_5()


def print_fizzbuzz_list(s, e):
    if s > e:
        raise Exception("The start > end")

    results = []
    for i in range(s, e+1):
        fb = FizzBuzzer(i)
        results.append(fb.to_str())

    return results
