import unittest
from enum import Enum
from typing import Callable, List

from src.tokenizers import WhitespaceTokenizer, NaivePunctTokenizer, PunctTokenizer

from nltk.tokenize import WhitespaceTokenizer as nltk_whitespace_tokenizer


class Tokenizers(Enum):
    WHITESPACE = WhitespaceTokenizer
    NAIVEPUNCT = NaivePunctTokenizer
    PUNCT = PunctTokenizer


class TestWhitespace(unittest.TestCase):
    @property
    def tokenizer(self) -> Callable:
        return Tokenizers.WHITESPACE.value()

    def __assert_message(self, expected_output: List[str], input: str) -> str:
        return f"Expected output '{expected_output}' with input '{input}'"

    def __check_equal(self, expected_output: List[str], input: str) -> None:
        self.assertEqual(
            self.tokenizer.tokenize(input),
            expected_output,
            self.__assert_message(expected_output=expected_output, input=input),
        )

    def __run_test(self, input) -> None:
        expected_output: List[str] = nltk_whitespace_tokenizer().tokenize(input)
        self.__check_equal(expected_output=expected_output, input=input)

    def test_empty_string(self):
        self.__run_test("")

    def test_single_space(self):
        self.__run_test(" ")

    def test_simple_phrase(self):
        self.__run_test("Lorem ipsum dolor sit amet")

    def test_with_punct(self):
        self.__run_test("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")

    def test_empty_head(self):
        self.__run_test("       Lorem ipsum")

    def test_empty_tail(self):
        self.__run_test("Lorem ipsum        ")

    def test_single_letters(self):
        self.__run_test("L O R E M")

    def test_long_empty(self):
        self.__run_test("                  ")


class TestNaivePunct(unittest.TestCase):
    @property
    def tokenizer(self) -> Callable:
        return Tokenizers.NAIVEPUNCT.value()

    def __assert_message(self, expected_output: List[str], input: str) -> str:
        return f"Expected output '{expected_output}' with input '{input}'"

    def __check_equal(self, expected_output: List[str], input: str) -> None:
        self.assertEqual(
            self.tokenizer.tokenize(input),
            expected_output,
            self.__assert_message(expected_output=expected_output, input=input),
        )

    def __run_test(self, input) -> None:
        expected_output: List[str] = nltk_whitespace_tokenizer().tokenize(input)
        self.__check_equal(expected_output=expected_output, input=input)

    def test_empty_string(self):
        self.__run_test("")

    def test_single_space(self):
        self.__run_test(" ")


if __name__ == "__main__":
    unittest.main()
