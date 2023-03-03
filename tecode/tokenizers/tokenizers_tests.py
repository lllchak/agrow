import unittest
from enum import Enum
from typing import Callable, List

from src.tokenizers import WhitespaceTokenizer, NaivePunctTokenizer, PunctTokenizer

from nltk.tokenize import WhitespaceTokenizer as nltk_ws_tkn
from nltk.tokenize import wordpunct_tokenize, word_tokenize


class TestBase(unittest.TestCase):
    def _assert_message(self, expected_output: List[str], input: str) -> str:
        return f"Expected output '{expected_output}' with input '{input}'"

    def _run_test(self, tokenizer: Callable, tkn_func: Callable, input: str) -> None:
        expected_output: List[str] = tkn_func(input)
        self.__check_equal(
            tokenizer=tokenizer, expected_output=expected_output, input=input
        )

    def __check_equal(
        self, tokenizer: Callable, expected_output: List[str], input: str
    ) -> None:
        self.assertEqual(
            tokenizer(input),
            expected_output,
            self._assert_message(expected_output=expected_output, input=input),
        )


class Tokenizers(Enum):
    WHITESPACE = WhitespaceTokenizer
    NAIVEPUNCT = NaivePunctTokenizer
    PUNCT = PunctTokenizer


class TestWhitespace(TestBase):
    @property
    def tokenizer(self) -> Callable:
        return Tokenizers.WHITESPACE.value()

    def test_empty_string(self) -> None:
        self._run_test(self.tokenizer.tokenize, nltk_ws_tkn().tokenize, "")

    def test_single_space(self) -> None:
        self._run_test(self.tokenizer.tokenize, nltk_ws_tkn().tokenize, " ")

    def test_simple_phrase(self) -> None:
        self._run_test(
            self.tokenizer.tokenize,
            nltk_ws_tkn().tokenize,
            "Lorem ipsum dolor sit amet",
        )

    def test_with_punct(self) -> None:
        self._run_test(
            self.tokenizer.tokenize,
            nltk_ws_tkn().tokenize,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )

    def test_empty_head(self) -> None:
        self._run_test(
            self.tokenizer.tokenize, nltk_ws_tkn().tokenize, "       Lorem ipsum"
        )

    def test_empty_tail(self) -> None:
        self._run_test(
            self.tokenizer.tokenize, nltk_ws_tkn().tokenize, "Lorem ipsum        "
        )

    def test_single_letters(self) -> None:
        self._run_test(self.tokenizer.tokenize, nltk_ws_tkn().tokenize, "L O R E M")

    def test_long_empty(self) -> None:
        self._run_test(
            self.tokenizer.tokenize, nltk_ws_tkn().tokenize, "                  "
        )

    def test_only_punct(self) -> None:
        self._run_test(self.tokenizer.tokenize, nltk_ws_tkn().tokenize, ",,,?.!")


class TestNaivePunct(TestBase):
    @property
    def tokenizer(self) -> Callable:
        return Tokenizers.NAIVEPUNCT.value()

    def test_empty_string(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, "")

    def test_single_space(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, " ")

    def test_simple_phrase(self) -> None:
        self._run_test(
            self.tokenizer.tokenize, wordpunct_tokenize, "Burger costs $5.4 dollars"
        )

    def test_with_punct(self) -> None:
        self._run_test(
            self.tokenizer.tokenize,
            wordpunct_tokenize,
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        )

    def test_only_punct(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, ",?.,;")

    def test_empty_tail(self) -> None:
        self._run_test(
            self.tokenizer.tokenize, wordpunct_tokenize, "Lorem ipsum,      "
        )

    def test_long_empty(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, "                ")

    def test_single_letters(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, "L, O, R, E, M,")

    def test_one_letter(self) -> None:
        self._run_test(self.tokenizer.tokenize, wordpunct_tokenize, "L")


# class TestPunct(unittest.TestCase):
#     @property
#     def tokenizer(self) -> Callable:
#         return Tokenizers.PUNCT.value()

#     def __check_equal(self, expected_output: List[str], input: str) -> None:
#         self.assertEqual(
#             self.tokenizer.tokenize.tokenize(input),
#             expected_output,
#             self.__assert_message(expected_output=expected_output, input=input),
#         )

#     def test_empty_string(self):
#         _self._run_test()


if __name__ == "__main__":
    unittest.main()
