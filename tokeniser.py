import string
from enum import Enum

class ControlTokens(Enum):
    NULL      = 0
    START     = 1
    NEWLINE   = 2
    PERIOD    = 3
    QUOTE     = 4
    COMMA     = 5
    QMARK     = 6
    EXCMARK   = 7
    COLON     = 8
    SEMICOLON = 9

# Simple buffered tokeniser
class Tokeniser:
    BUF_SZ = 512
    TERM_TOKENS = [ControlTokens.PERIOD, ControlTokens.QMARK, ControlTokens.EXCMARK, ControlTokens.NULL]
    TERM_TOKEN_LUT = {'.' : ControlTokens.PERIOD,
                      '?' : ControlTokens.QMARK,
                      '!' : ControlTokens.EXCMARK}

    def __init__(self, stream, ignore_newline=True):
        self._stream = stream
        self._ignore_newline = ignore_newline
    
    # TODO: Consider if a token for starting each sentence is neccesary.
    # TODO: Cleanup logic and cleanly support colon/semicolon
    def __iter__(self):
        term = True
        tok_buf = ""
        # Prefill the buffer
        self._fill_buf()
        while not self._is_eof:
            next_char = self._get_next_char()
            if not self._ignore_newline and next_char in ('\n', '\r'):
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                yield ControlTokens.NEWLINE
            elif next_char in self.TERM_TOKEN_LUT.keys():
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                yield self.TERM_TOKEN_LUT[next_char]
                term = True
            elif next_char in ('\'', '"', '`'):
                if len(tok_buf):
                    yield tok_buf
                    tok_buf = ''
                if term:
                    term = False
                    yield ControlTokens.START
                yield ControlTokens.QUOTE
            elif next_char in (' ', '\t', ',', '\n', '\r'):
                if len(tok_buf):
                    # Did this token start a new clause?
                    if term:
                        term = False
                        yield ControlTokens.START
                    yield tok_buf
                    tok_buf = ''
            else:
                tok_buf += next_char.upper()

    @property
    def _is_eof(self):
        return len(self._text_buf) == 0
    
    def _fill_buf(self):
        self._text_buf = self._stream.read(self.BUF_SZ)
        self._text_buf_offs = 0

    def _get_next_char(self):
        # We assume we can always get a char so deal with buffer filling after getting result
        assert len(self._text_buf) and self._text_buf_offs < len(self._text_buf), "Tried to read empty buffer"
        result = self._text_buf[self._text_buf_offs]
        self._text_buf_offs += 1
        #  Refill buffer if this was the last char
        if not self._text_buf_offs < len(self._text_buf):
            self._fill_buf()
        return result
