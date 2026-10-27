"""Infix -> postfix conversion engine (tokenizer, validator, stack algorithm, step trace).

Conventions (applied consistently):
  * Precedence: '^' = 4 (right-assoc), unary +/- = 3 (right-assoc, prefix),
    '*', '/', '%' = 2 (left-assoc), '+', '-' = 1 (left-assoc).
  * Unary operators appear in postfix as 'u+' / 'u-'.  Because unary (3) is below '^' (4),
    -A^B means -(A^B) -> "A B ^ u-".  A prefix operator is pushed without popping anything.
  * A sign may follow '(' , the start of input, or one of '* / % ^'.  Sign after '+' or '-'
    (A++B, A+-B) and stacked signs (--A) are rejected as consecutive operators.
  * Implicit multiplication (optional): <number or ')'> followed by <identifier or '('>,
    or ')' followed by <number>.  'A(B)' and '2 3' are rejected (ambiguous).
  * Identifiers are letters/digits/underscore starting with a non-digit, so 'AB' is ONE variable.
  * Numbers: 12, 3.5, .5, 2.5e3, 1E-4.  The engine never evaluates anything (no eval/exec).
"""
import re

MAX_LENGTH = 300
BINARY = {"+": (1, "L"), "-": (1, "L"), "*": (2, "L"), "/": (2, "L"), "%": (2, "L"), "^": (4, "R")}
UNARY = {"+": "u+", "-": "u-"}
UNARY_PREC = 3

TOKEN_RE = re.compile(
    r"(?P<num>(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?)"
    r"|(?P<id>[A-Za-z_][A-Za-z0-9_]*)|(?P<op>[-+*/%^])|(?P<lp>\()|(?P<rp>\))"
)


class ConversionError(ValueError):
    """Raised for any invalid expression; the message is safe to show to users."""


def precedence(sym):
    return UNARY_PREC if sym in ("u+", "u-") else BINARY[sym][0]


def tokenize(expr):
    """Split text into (kind, text) tokens; multi-digit numbers / names stay whole."""
    tokens, pos = [], 0
    while pos < len(expr):
        if expr[pos].isspace():
            pos += 1
            continue
        m = TOKEN_RE.match(expr, pos)
        if not m:
            raise ConversionError(f"Invalid character {expr[pos]!r} at position {pos + 1}. "
                                  "Use letters, numbers, + - * / % ^ and parentheses.")
        tokens.append((m.lastgroup, m.group()))
        pos = m.end()
    return tokens


def validate(tokens, implicit=True):
    """Check syntax and classify tokens as (role, text, is_implicit).
    Roles: operand, lparen, rparen, binary, unary."""
    items, expect_operand, depth, prev = [], True, 0, None
    for kind, text in tokens:
        if kind in ("num", "id", "lp") and not expect_operand:
            allowed = implicit and ((prev[0] in ("num", "rp") and kind in ("id", "lp"))
                                    or (prev[0] == "rp" and kind == "num"))
            if not allowed:
                hint = "" if implicit else " (implicit multiplication is turned off)"
                raise ConversionError(f"Missing operator between {prev[1]!r} and {text!r}{hint}.")
            items.append(("binary", "*", True))
            expect_operand = True
        if kind in ("num", "id"):
            items.append(("operand", text, False))
            expect_operand = False
        elif kind == "lp":
            items.append(("lparen", "(", False))
            depth += 1
        elif kind == "rp":
            if expect_operand:
                raise ConversionError("Missing operand before ')' (empty parentheses or a dangling operator).")
            depth -= 1
            if depth < 0:
                raise ConversionError("Unmatched closing parenthesis ')'.")
            items.append(("rparen", ")", False))
        elif expect_operand:  # operator where an operand is required
            if text not in UNARY:
                raise ConversionError(f"Operator {text!r} is missing its left operand.")
            last = items[-1] if items else None
            if last and (last[0] == "unary" or (last[0] == "binary" and last[1] in "+-" and not last[2])):
                raise ConversionError(f"Consecutive operators {last[1].lstrip('u')!r} and {text!r}: operand missing.")
            items.append(("unary", UNARY[text], False))
        else:
            items.append(("binary", text, False))
            expect_operand = True
        prev = (kind, text)
    if not items:
        raise ConversionError("Expression is empty. Try something like A + B * C.")
    if expect_operand:
        raise ConversionError("Expression is incomplete: an operator is missing its right operand.")
    if depth > 0:
        raise ConversionError(f"Unmatched opening parenthesis: {depth} '(' never closed.")
    return items


def to_postfix(items):
    """Stack-based conversion (stack = Python list). Returns (postfix_tokens, steps)."""
    stack, output, steps = [], [], []

    def log(token, action, text):
        steps.append({"step": len(steps) + 1, "token": token, "action": action,
                      "operation": text, "stack": list(stack), "output": " ".join(output)})

    for role, sym, implicit in items:
        label = sym + (" (implicit)" if implicit else "")
        if role == "operand":
            output.append(sym)
            log(label, "output", f"Operand: append '{sym}' to the output.")
        elif role == "lparen":
            stack.append(sym)
            log(label, "push", "Push '(' onto the stack.")
        elif role == "unary":
            stack.append(sym)
            log(label, "push", f"Unary operator: push '{sym}' (prefix operators pop nothing).")
        elif role == "rparen":
            popped = []
            while stack[-1] != "(":
                popped.append(stack.pop())
                output.append(popped[-1])
            stack.pop()
            what = ", ".join(f"'{p}'" for p in popped) if popped else "nothing"
            log(label, "pop", f"Pop until '(': {what} moved to output; '(' discarded.")
        else:
            popped = []
            while stack and stack[-1] != "(" and (
                    precedence(stack[-1]) > precedence(sym)
                    or (precedence(stack[-1]) == precedence(sym) and BINARY[sym][1] == "L")):
                popped.append(stack.pop())
                output.append(popped[-1])
            top = stack[-1] if stack else None
            stack.append(sym)
            if popped:
                log(label, "pop", "Pop " + ", ".join(f"'{p}'" for p in popped)
                    + f" to output (priority >= '{sym}'), then push '{sym}'.")
            else:
                why = ("stack is empty" if top is None else "top is '('" if top == "("
                       else f"'{sym}' is right-associative, equal precedence stays" if precedence(top) == precedence(sym)
                       else f"'{sym}' has higher precedence than '{top}'")
                log(label, "push", f"Push '{sym}' ({why}).")
    while stack:
        op = stack.pop()
        output.append(op)
        log("end", "pop", f"End of input: pop '{op}' to output.")
    return output, steps


def convert(expr, implicit=True):
    """Full pipeline. Raises ConversionError for invalid input."""
    if not isinstance(expr, str):
        raise ConversionError("Expression must be text.")
    expr = expr.strip()
    if not expr:
        raise ConversionError("Expression is empty. Try something like A + B * C.")
    if len(expr) > MAX_LENGTH:
        raise ConversionError(f"Expression is too long ({len(expr)} characters; the limit is {MAX_LENGTH}).")
    items = validate(tokenize(expr), implicit)
    postfix, steps = to_postfix(items)
    return {"infix": expr, "items": items, "postfix": postfix,
            "postfix_text": " ".join(postfix), "steps": steps}
