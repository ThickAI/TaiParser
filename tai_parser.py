import sys

from lark import Lark, Transformer, v_args

rule_grammar=r"""
   ?start: rule

    rule: rule_name ":" logic_expr "->" logic_expr

    logic_expr: sub_clause
        | parenthesized_clause
        | logic_expr (connective logic_expr)*
    
    parenthesized_clause: "("logic_expr")"
    connective : "and" | "or" | "并且" | "或者"
    sub_clause: indicator comparison_operator SIGNED_NUMBER
        | indicator "=" bool
        
    rule_name: indicator
    indicator: /[\p{Han}a-zA-Z]+[\p{Han}a-zA-Z0-9\/]*/
    comparison_operator: ">" | ">=" | "<" | "<=" | "="
    bool: "true" | "false" | "真" | "假"

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

"""

logic_grammar=r"""
    ?start: logic_expr

    logic_expr: sub_clause
    | parenthesized_clause
    | logic_expr (connective logic_expr)*
    
    parenthesized_clause: "("logic_expr")"
    connective : "and" | "or" | "并且" | "或者"
    sub_clause: indicator comparison_operator SIGNED_NUMBER
    indicator: /[\p{Han}a-zA-Z]+[\p{Han}a-zA-Z0-9]*/
    comparison_operator: ">" | ">=" | "<" | "<=" | "="

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS

    %ignore WS

"""

tai_parser = Lark(logic_grammar, regex=True)
rules_tai_parser = Lark(rule_grammar, regex=True)

if __name__ == '__main__':
    filename=sys.argv[1]
    with open(filename, encoding="utf8") as f:
        s=f.readline()
        while s:
            if filename.endswith(".rules.txt"):
                print(rules_tai_parser.parse(s).pretty())
            elif filename.endswith(".logic.txt"):
                print(tai_parser.parse(s).pretty())
            else:
                print("Incorrect file extension name.")
            s=f.readline()
