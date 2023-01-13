import re

import dtypes
from tokenizer import BaseTokenizer


class PunctRegex(BaseTokenizer):
    """
    Stores regular expressions for string tokenization with respect to
    punctuation
    """

    def __repr__(self) -> str:
        return "{}(string_tokenizer_regex={})".format(
            __class__.__name__,
            self._RE_STRING_TOKENIZER
        )

    __slots__ = ["_RE_STRING_TOKENIZER"]

    # Format of a regular expression to split punctuation from words 
    _STRING_TOKENIZER_FMT = r"""(
        %(MultiChar)s
        |
        (?=%(WordStart)s)\S+?                   # Accept word characters until end is found
        (?=                                     # Sequences marking a word's end
            \s|                                 # White-space
            $|                                  # End-of-string
            %(NonWord)s|%(MultiChar)s|          # Punctuation
            ,(?=$|\s|%(NonWord)s|%(MultiChar)s) # Comma if at end of word
        )
        |
        \S
    )"""

    # Ending context chars
    cend = ('.', '!', '?', ';', ':')

    """
    Characters that cannot appear without words
    """
    @property
    def _re_non_word_chars(self):
        return r"(?:[)\";}\]\*:@\'\({\[%s])" % re.escape(
            "".join(set(self.cend) - {'.'})
        )

    """
    Multi-char punctuation symbols
    """
    _re_multi_char_punct = r"(?:\-{2,}|\.{2,}|(?:\.\s){2,}\.)"

    """
    Excludes some characters from starting word tokens
    """
    _re_word_start = r"[^\(\"\`{\[:;&\#\*@\)}\]\-,]"

    """
    Compiles word search regular experession
    """
    @property
    def gstring_re(self) -> str:
        self._RE_STRING_TOKENIZER = re.compile(
            self._STRING_TOKENIZER_FMT
            % {
                "NonWord":   self._re_non_word_chars,
                "WordStart": self._re_word_start,
                "MultiChar": self._re_multi_char_punct
            }, re.UNICODE | re.VERBOSE
        )

        return self._RE_STRING_TOKENIZER

    def tokenize(self, string: str) -> dtypes.List[str]:
        """
        Tokenizes a string to a list of tokens using pre-compiled regular
        expression. Splits of punctuation from words.

        Args:
            string (str) : String to be tokenized

        Returns:
            List of tokens, i.e "string to tokenize" -> ["string", "to", "tokenize"]
        """
        return self.gstring_re.findall(string)


class PunctToken:
    """
    String (sentence/context) token class. Stores token value, its type
    and if its final string token flag.
    """
        
    # Numeric token (contains only number(-s))
    _NUMERIC = re.compile(r"^-?[\.,]?\d[\d,\.-]*\.?$")
    # Alpha token (contains only alphabetical characters)
    _ALPHA = re.compile(r"[^\W\d]+$", re.UNICODE)

    def __init__(self, tk: str) -> None:
        self.tk = tk
        self.type = self.__stype(tk)
        self.tfinal = tk.endswith('.') | \
                      tk.endswith('?') | \
                      tk.endswith('!') | \
                      tk.endswith(';')

    def __stype(self, tk) -> None:
        return self._NUMERIC.sub("NUMERIC", tk.lower())

    @property
    def tk_no_endchar(self):
        return self.type[:-1] \
               if len(self.type) > 1 and self.type[-1] in ['.', '?', '!', "..."] \
               else self.type

    @property
    def fupper(self) -> bool:
        return self.tk[0].isupper()

    @property
    def flower(self) -> bool:
        return self.tk[0].islower()

    @property
    def is_num(self) -> bool:
        return self.type.startwith("NUMERIC")

    @property
    def is_alpha(self) -> bool:
        return self._ALPHA.match(self.tk)
    