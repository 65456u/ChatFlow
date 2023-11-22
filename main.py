# 1. 包的引入
from ply import lex

# 2. Token类型列表的声明
tokens = (
    'TOKEN_1', 'TOKEN_2', 'TOKEN_3'
)

# 3. Token匹配规则的声明（字符串，函数）
t_TOKEN_1 = r"""reg_expr_1"""
t_TOKEN_2 = r"""reg_expr_2"""


def t_TOKEN_3(t):
    r"""reg_expr_3"""
    return t


if __name__ == '__main__':
    data = 'reg_expr_3reg_expr_2reg_expr_1'

    lexer = lex.lex()
    lexer.input(data)

    while True:
        token = lexer.token()
        print(token)
        if not token:
            break
