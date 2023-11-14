import pytest
from interpreter import Interpreter, Number, BinOp, UnOp, Token, TokenType, Variable, Assignment, Semicolon

@pytest.fixture(scope="function")
def interpreter():
    return Interpreter()

class TestInterpreter:
    interpreter = Interpreter()

    def test_token(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.eval("1-=-1")
        with pytest.raises(SyntaxError):
            interpreter.eval("(2+2")
        with pytest.raises(SyntaxError):
            interpreter.eval("2+-")
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN x:2END.")
        with pytest.raises(SyntaxError):
            interpreter.eval("x")
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN x:= 2 $ 3; END.")
        with pytest.raises(SyntaxError):
            interpreter.eval("BEGIN   x:   2 END.")

    def test_binop(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.visit_binop(BinOp(Number(Token(TokenType.NUMBER, 2)), Token(TokenType.OPERATOR, "&"), Number(Token(TokenType.NUMBER, 2))))

    def test_unop(self, interpreter):
        assert interpreter.eval("BEGIN x:=1++++-++1 END.") == {"x":0}
        assert interpreter.eval("BEGIN x:=1---1 END.") == {"x":0}
        assert interpreter.eval("BEGIN x:=1----1 END.") == {"x":2}
        with pytest.raises(SyntaxError):
            interpreter.visit_unop(UnOp(Token(TokenType.OPERATOR, "$"), Number(Token(TokenType.NUMBER, 2))))

    def test_variables(self, interpreter):
        with pytest.raises(ValueError):
            interpreter.eval("BEGIN x:=y END.")

    def test_invalid_factor(self, interpreter):
        with pytest.raises(SyntaxError):
            interpreter.parser.factor()

    def test_expression_1(self, interpreter):
        assert interpreter.eval("BEGIN END.") == {}

    def test_expression_2(self, interpreter):
        assert interpreter.eval("BEGIN x:= 2 + 3 * (2 + 3); y:= 2 / 2 - 2 + 3 * ((1 + 1) + (1 + 1)); END.") == {'x': 17.0, 'y': 11.0}
    
    def test_expression_3(self, interpreter):
        assert interpreter.eval("BEGIN y:= 2; BEGIN a := 3; a := a; b := 10 + a + 10 * y / 4; c := a - b; END; x := 11; END.") == {'x': 11.0, 'y': 2.0, 'a': 3.0, 'b': 18.0, 'c': -15.0}

    def test_number_str(self):
        num = Number("2")
        assert num.__str__()=='Number (2)'

    def test_binop_str(self):
        binop = BinOp(Number(Token(TokenType.NUMBER, 2)), Token(TokenType.OPERATOR, "+"), Number (Token(TokenType.NUMBER, 2)))
        assert binop.__str__() == "BinOp+ (Number (Token(TokenType.NUMBER, 2)), Number (Token(TokenType.NUMBER, 2)))"

    def test_unop_str(self):
        unop = UnOp(Token(TokenType.OPERATOR, "-"), Number(Token(TokenType.NUMBER, 2)))
        assert unop.__str__() == "UnOp-Number (Token(TokenType.NUMBER, 2))"

    def test_variable_str(self):
        var = Variable("x")
        assert var.__str__() == "Variable(x)"

    def test_assignment_str(self):
        assignment = Assignment(Variable("x"), Number(Token(TokenType.NUMBER, 2)))
        assert assignment.__str__() == "AssignmentVariable(x):=Number (Token(TokenType.NUMBER, 2))"

    def test_semicolon_str(self):
        semicolon = Semicolon(Variable("x"), Variable("y"))
        assert semicolon.__str__() == "Semicolon (Variable(x), Variable(y))"
