import pytest
from interpreter import Interpreter, Number, BinOp, UnOp, Token, TokenType

@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()

class TestInterpreter:
    interpreter = Interpreter()

    def test_add(self, interpreter):
        assert interpreter.eval("2+2") == 4
    
    def test_sub(self, interpreter):
        assert interpreter.eval("2-2") == 0

    def test_mult(self, interpreter):
        assert interpreter.eval("2*2") == 4
    
    def test_div(self, interpreter):
        assert interpreter.eval("2/2") == 1

    def test_add_with_letter(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2+a")
    
    def test_add_wrong_operator(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("2$2")

    @pytest.mark.parametrize(
        "interpreter, code", [(interpreter, "2 + 2"),
                              (interpreter, "2+ 2"),
                              (interpreter, " 2 +2")]
    )
    def test_add_spaces(self, interpreter, code):
        assert interpreter.eval(code) == 4

    def test_priority(self, interpreter):
        assert interpreter.eval("(2+2)*2") == 8
        assert interpreter.eval("2+2*2") == 6
        assert interpreter.eval("2*2/2+2") == 4

    def test_token(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("1-=-1")
        with pytest.raises(SyntaxError):
            interpreter.eval("(2+2")
        with pytest.raises(SyntaxError):
            interpreter.eval("2+-")

    def test_binop(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, 2)), Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, 2))))

    def test_unop(self, interpreter):
        assert interpreter.eval("+++++++2") == 2
        assert interpreter.eval("-2") == -2
        assert interpreter.eval("--2") == 2
        with pytest.raises(SyntaxError):
            interpreter.eval("*2")

    def test_number_str(self):
        num = Number("2")
        assert num.__str__()=='Number (2)'

    def test_binop_str(self):
        binop = BinOp(Number(Token(TokenType.NUMBER, 2)), Token(TokenType.OPERATOR, "+"), Number (Token(TokenType.NUMBER, 2)))
        assert binop.__str__() == "BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 2)))"

    def test_unop_str(self):
        unop = UnOp(Token(TokenType.OPERATOR, "+"), Number(Token(TokenType.NUMBER, 2)))
        assert unop.__str__() == "UnOp+Number (Token(TokenType.NUMBER, 2))"
