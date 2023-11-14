from .token import Token, TokenType
from .lexer import Lexer
from .ast import BinOp, Number, UnOp, Variable, Assignment, Semicolon

class Parser:
    def __init__(self):
        self._current_token = None
        self._lexer = Lexer()
    
    def check_token(self, type_: TokenType):
        if self._current_token:
            if self and self._current_token.type_ == type_:
                self._current_token = self._lexer.next()
        else:
            raise SyntaxError("invalid token")

    def factor(self):
        token = self._current_token
        if token:
            if token.type_ == TokenType.NUMBER:
                self.check_token(TokenType.NUMBER)
                return Number(token)
            if token.type_ == TokenType.LPAREN:
                self.check_token(TokenType.LPAREN)
                result = self.expr()
                self.check_token(TokenType.RPAREN)
                return result
            if token.type_ == TokenType.OPERATOR:
                self.check_token(TokenType.OPERATOR)
                return UnOp(token,self.factor())
            if token.type_ == TokenType.VARIABLE:
                self.check_token(TokenType.VARIABLE)
                return Variable(token)
        raise SyntaxError("invalid factor")

    def term(self):
        result = self.factor()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["*", "/"]:
                break
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            return BinOp(result, token, self.term())            
        return result

    def expr(self):
        result = self.term()
        while self._current_token and (self._current_token.type_ == TokenType.OPERATOR):
            if self._current_token.value not in ["+", "-"]:
                break
            token = self._current_token
            self.check_token(TokenType.OPERATOR)
            result = BinOp(result, token, self.term())            
        return result

    def token_list(self):
        if self._current_token:
            if self._current_token.type_ == TokenType.BEGIN:
                result = self.token_scope()
            elif self._current_token.type_ == TokenType.VARIABLE:
                variable = self._current_token
                self.check_token(TokenType.VARIABLE)
                self.check_token(TokenType.ASSIGNMENT)
                result = Assignment(variable, self.expr())
            elif self._current_token.type_ == TokenType.END:
                result = None
            else:
                raise SyntaxError("invalid token syntax")
            if self._current_token.type_ == TokenType.SEMICOLON:
                self._current_token = self._lexer.next()
                result = Semicolon(result, self.token_list())
        return result
    
    def token_scope(self):
        self.check_token(TokenType.BEGIN)
        result = self.token_list()
        self.check_token(TokenType.END)
        return result

    def parse(self, code):
        self._lexer.init(code)
        self._current_token = self._lexer.next()
        result = self.token_scope()
        self.check_token(TokenType.DOT)
        return result
