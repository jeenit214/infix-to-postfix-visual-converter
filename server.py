"""
HTTP server for the Infix to Postfix Visual Converter.
Standard Python library only (http.server, urllib.parse, html, os, sys, re).
Zero external dependencies, zero JavaScript.
"""

import html
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, quote, urlparse

from converter import MAX_LENGTH, ConversionError, convert

BASE = os.path.dirname(os.path.abspath(__file__))
MAX_BODY = 8192
EXAMPLES = [
    "A+B*C",
    "(A+B)*(C-D)",
    "total + price * (quantity - 2)",
    "(12 + 8) * 3",
    "A + B * C ^ D",
    "2^3^2",
    "-A+B",
    "A*-B",
    "-(A+B)",
    "A*(B+(C-D))",
    "3.5 + 2.25 * x",
    "2(A+B)"
]
esc = html.escape


def read_file_content(*parts):
    """Safely reads template or static files from disk."""
    path = os.path.join(BASE, *parts)
    with open(path, encoding="utf-8") as f:
        return f.read()


def fill(template, **values):
    """Single-pass {{name}} substitution preventing nested injection."""
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values.get(m.group(1), ""), template)


def chip(sym):
    """Generates a styled token chip for operands, operators, or parentheses."""
    if sym in ("(", ")"):
        cls = "paren"
    elif sym in ("+", "-", "*", "/", "%", "^", "u+", "u-"):
        cls = "op"
    else:
        cls = "operand"
    return f'<span class="chip {cls}">{esc(sym)}</span>'


def stack_cell(stack):
    """Renders the stack column in the conversion table from Bottom to Top."""
    if not stack:
        return '<span class="muted-empty">&empty; empty</span>'
    chips = "".join(chip(s) for s in stack)
    return (
        f'<div class="stack-cell-flow">'
        f'<span class="flow-tag bot" title="Bottom of Stack">BOT</span>'
        f'<span class="chips-group">{chips}</span>'
        f'<span class="flow-tag top" title="Top of Stack (LIFO)">TOP</span>'
        f'</div>'
    )


def stack_card(step):
    """
    Renders an individual vertical stack vessel diagram for a specific step.
    Displays items from Top (opening) to Bottom (base).
    """
    st = step["stack"]
    if st:
        blocks = []
        for i, s in enumerate(reversed(st)):
            is_top = (i == 0)
            cls = "paren" if s in ("(", ")") else "op"
            top_mark = '<span class="top-indicator">TOP</span>' if is_top else ""
            top_cls = " is-top" if is_top else ""
            blocks.append(
                f'<div class="blk {cls}{top_cls}">'
                f'<span class="blk-val">{esc(s)}</span>{top_mark}'
                f'</div>'
            )
        blocks_html = "".join(blocks)
    else:
        blocks_html = '<div class="blk none">&empty; (empty)</div>'

    token_label = esc(step["token"])
    return (
        f'<figure class="stack-card">'
        f'<figcaption class="card-caption">'
        f'Step {step["step"]}<br>'
        f'<span class="card-tok">Token: <code>{token_label}</code></span>'
        f'</figcaption>'
        f'<div class="stack-vessel">'
        f'<div class="vessel-rim">&#9650; TOP (LIFO)</div>'
        f'<div class="vessel-body">{blocks_html}</div>'
        f'<div class="vessel-base">&#9660; BOTTOM</div>'
        f'</div>'
        f'</figure>'
    )


def render_result(r):
    """Renders the result section containing infix, postfix, table, and stack cards."""
    role_cls = {
        "operand": "operand",
        "binary": "op",
        "unary": "op",
        "lparen": "paren",
        "rparen": "paren"
    }
    tokens = "".join(
        f'<span class="chip {role_cls.get(role, "op")}">{esc(sym)}</span>'
        for role, sym, _ in r["items"]
    )
    tags = {"output": "Output", "push": "Push", "pop": "Pop"}
    rows = "".join(
        f'<tr>'
        f'<th scope="row" class="step-num">{s["step"]}</th>'
        f'<td><code class="tok-code">{esc(s["token"])}</code></td>'
        f'<td><span class="tag {s["action"]}">{tags.get(s["action"], s["action"].capitalize())}</span> <span class="op-desc">{esc(s["operation"])}</span></td>'
        f'<td>{stack_cell(s["stack"])}</td>'
        f'<td><code class="postfix-code">{esc(s["output"]) or "&mdash;"}</code></td>'
        f'</tr>'
        for s in r["steps"]
    )
    cards = "".join(stack_card(s) for s in r["steps"])
    return fill(
        read_file_content("templates", "result.html"),
        infix=esc(r["infix"]),
        tokens=tokens,
        token_count=str(len(r["items"])),
        step_count=str(len(r["steps"])),
        postfix=esc(r["postfix_text"]),
        rows=rows,
        cards=cards
    )


def render_page(expr="", implicit=True, content=""):
    """Renders the full HTML5 page shell with the given form parameters and content."""
    examples = "".join(
        f'<li><a class="ex-link" href="/convert?expr={quote(e)}&amp;implicit=1" title="Test example: {esc(e)}">{esc(e)}</a></li>'
        for e in EXAMPLES
    )
    return fill(
        read_file_content("templates", "index.html"),
        expr=esc(expr, quote=True),
        checked="checked" if implicit else "",
        examples=examples,
        content=content,
        maxlen=str(MAX_LENGTH)
    )


class ConverterRequestHandler(BaseHTTPRequestHandler):
    """Custom HTTP Request Handler serving GET and POST requests."""
    server_version = "InfixVisualizer/1.0"

    def send_body(self, status, body, ctype="text/html; charset=utf-8"):
        """Sends an HTTP response with security headers and given status code."""
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy",
                         "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; form-action 'self'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(data)

    def error_page(self, status, message, expr="", implicit=True):
        """Renders an error banner within the main page shell."""
        content = fill(read_file_content("templates", "error.html"), message=esc(message))
        self.send_body(status, render_page(expr, implicit, content))

    def convert_and_send(self, params):
        """Processes conversion request and returns rendered response."""
        expr = params.get("expr", [""])[0]
        implicit = "implicit" in params
        try:
            result = convert(expr, implicit)
        except ConversionError as exc:
            self.error_page(400, str(exc), expr[:MAX_LENGTH * 2], implicit)
            return
        self.send_body(200, render_page(expr, implicit, render_result(result)))

    def do_GET(self):
        """Handles HTTP GET requests."""
        url = urlparse(self.path)
        if url.path == "/":
            self.send_body(200, render_page())
        elif url.path == "/convert":
            self.convert_and_send(parse_qs(url.query, max_num_fields=10))
        elif url.path == "/static/style.css":
            self.send_body(200, read_file_content("static", "style.css"), "text/css; charset=utf-8")
        elif url.path == "/favicon.ico":
            svg = (
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
                '<rect width="100" height="100" rx="20" fill="#6a96ff"/>'
                '<text x="50" y="68" font-family="sans-serif" font-weight="bold" font-size="50" '
                'fill="#0c1222" text-anchor="middle">RPN</text>'
                '</svg>'
            )
            self.send_body(200, svg, "image/svg+xml")
        else:
            self.error_page(404, "Page not found.")

    def do_POST(self):
        """Handles HTTP POST requests from the conversion form."""
        if urlparse(self.path).path != "/convert":
            return self.error_page(404, "Page not found.")
        content_type = self.headers.get("Content-Type") or ""
        if not content_type.startswith("application/x-www-form-urlencoded"):
            return self.error_page(415, "Unsupported form encoding. Expected application/x-www-form-urlencoded.")
        length = self.headers.get("Content-Length")
        if length is None:
            return self.error_page(411, "Content-Length header is required.")
        if not length.isdigit():
            return self.error_page(400, "Invalid Content-Length header.")
        if int(length) > MAX_BODY:
            return self.error_page(413, "Request payload too large.")
        try:
            body = self.rfile.read(int(length)).decode("utf-8")
            params = parse_qs(body, keep_blank_values=True, max_num_fields=10)
        except (UnicodeDecodeError, ValueError):
            return self.error_page(400, "Malformed form data.")
        self.convert_and_send(params)

    def handle_one_request(self):
        """Intercepts internal errors to prevent server crash and return HTTP 500."""
        try:
            super().handle_one_request()
        except Exception as exc:
            sys.stderr.write(f"Internal Server Error: {exc!r}\n")
            try:
                self.error_page(500, "An internal server error occurred. Please verify your input and try again.")
            except Exception:
                pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server_address = ("127.0.0.1", port)
    server = ThreadingHTTPServer(server_address, ConverterRequestHandler)
    print("=" * 65)
    print(" INFIX TO POSTFIX VISUAL CONVERTER (Standard Python)")
    print(f" Web Server running at: http://127.0.0.1:{port}")
    print(" Press Ctrl+C to terminate.")
    print("=" * 65)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gracefully shut down.")


if __name__ == "__main__":
    main()
