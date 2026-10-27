# Infix to Postfix Visual Converter

An interactive, educational Data Structures and Algorithms (DSA) project built exclusively with **Python (Standard Library)**, **HTML5**, and **CSS3**.

The application converts mathematical infix expressions into postfix notation (Reverse Polish Notation — RPN) using Dijkstra's **Shunting-Yard Algorithm** backed by a **Stack (LIFO)** data structure. It dynamically visualizes every single push, pop, and output step with a comprehensive trace table and styled physical stack container diagrams.

---

## Quick Start Guide

### 1. Requirements
- Python 3.8 or higher.
- Any modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari).
- **Zero external dependencies**: No Flask, Django, Node.js, React, Bootstrap, or JavaScript.

### 2. Execution Commands

#### Run the Web Server:
Open your terminal / command prompt, navigate to the `infix_postfix_visualizer` directory, and start the server:

```bash
cd infix_postfix_visualizer
python server.py
```

By default, the server binds to `http://127.0.0.1:8000`. You can also specify a custom port:

```bash
python server.py 8080
```

#### Access the Application:
Open your web browser and navigate to:
```
http://127.0.0.1:8000
```



## File Structure

```
infix_postfix_visualizer/
│
├── server.py              # HTTP server (ThreadingHTTPServer), routing, HTML escaping & security
├── converter.py           # Tokenizer, syntax validator, stack conversion engine & step generator
├── README.md              # Documentation, technical specs, and complete project report
│
├── templates/
│   ├── index.html         # Main page shell, expression form, quick examples & algorithm guide
│   ├── result.html        # Dynamic conversion report: infix/postfix cards, trace table, stack strip
│   └── error.html         # User-friendly validation error banner and diagnostic tips
│
└── static/
    └── style.css          # Modern dark-navy theme, responsive CSS3 styling & animations
```

---

## Expression Support & Grammar Conventions

| Feature | Supported Syntax | Example Input | Postfix Output |
|---|---|---|---|
| **Single-letter Variables** | `A-Z`, `a-z` | `A + B` | `A B +` |
| **Multi-character Identifiers** | Letters, digits, `_` | `total + price * (quantity - 2)` | `total price quantity 2 - * +` |
| **Integers & Decimals** | Digits, decimal points | `3.5 + 2.25` | `3.5 2.25 +` |
| **Multi-digit Integers** | Whole numbers | `(12 + 8) * 3` | `12 8 + 3 *` |
| **Scientific Notation** | Standard notation | `2.5e3 + 4` / `1E-4 * x` | `2.5e3 4 +` / `1E-4 x *` |
| **Basic Binary Operators** | `+`, `-`, `*`, `/`, `%` | `A + B * C - D / E` | `A B C * + D E / -` |
| **Exponentiation (`^`)** | Right-associative | `2 ^ 3 ^ 2` / `A + B * C ^ D` | `2 3 2 ^ ^` / `A B C D ^ * +` |
| **Unary Minus (`u-`)** | Right-associative | `-A + B` / `A * -B` | `A u- B +` / `A B u- *` |
| **Unary Plus (`u+`)** | Right-associative | `+A * B` | `A u+ B *` |
| **Nested Parentheses** | Any valid depth | `A * (B + (C - D))` | `A B C D - + *` |
| **Implicit Multiplication** | Configurable toggle | `2(A + B)` / `(A+B)(C+D)` / `2x` | `2 A B + *` / `A B + C D + *` |

### Operator Precedence and Associativity Table

| Precedence Level | Operators | Associativity | Description |
|:---:|:---:|:---:|---|
| **4 (Highest)** | `^` | Right-to-Left | Exponentiation (e.g. `2^3^2 = 2^(3^2) = 512`) |
| **3** | `u+`, `u-` | Right-to-Left | Unary Sign (e.g. `-A^B = -(A^B) -> A B ^ u-`) |
| **2** | `*`, `/`, `%` | Left-to-Right | Multiplication, True Division, Modulus |
| **1 (Lowest)** | `+`, `-` | Left-to-Right | Binary Addition and Subtraction |

---

# Comprehensive Project Report

## 1. Abstract
The **Infix to Postfix Visual Converter** is a dedicated educational software system designed to bridge theoretical understanding and practical implementation of the **Stack (LIFO)** data structure. In computer science pedagogy, expression conversion and evaluation represent a fundamental rite of passage. This project delivers an interactive, server-rendered web application that transforms arbitrary arithmetic expressions into postfix notation while recording and visualizing every intermediate state of the operator stack and output stream. Built strictly without external libraries, backend frameworks, or client-side JavaScript, the application achieves high performance, security, and algorithmic transparency.

## 2. Introduction
In standard mathematical notation, arithmetic expressions are written in **infix notation**, where operators are positioned between operands (e.g., $A + B$). While natural for humans, infix notation is notoriously complex for computational machines because evaluation order depends on non-local precedence rules and arbitrary parenthetical groupings.

To evaluate expressions efficiently in linear time, compilers and runtime interpreters translate infix expressions into **postfix notation** (also known as **Reverse Polish Notation** or RPN), introduced by Jan Łukasiewicz and popularized by Edsger Dijkstra. In postfix notation, operators immediately succeed their operands (e.g., $A B +$), which eliminates all parentheses and enables single-pass evaluation using a data structure known as the **Stack**.

## 3. Problem Statement
Beginner students frequently struggle to visualize how operator precedence, left/right associativity, and parentheses interact dynamically with the stack during the conversion process. Static textbook diagrams only show final answers or isolated steps. Existing online converters often rely on heavyweight JavaScript single-page application (SPA) frameworks or unsafely use Python's `eval()` function, hiding the true algorithmic mechanics. There is a need for a lightweight, secure, and visually expressive converter that reveals the internal stack operations step-by-step.

## 4. Objectives
- **Algorithmic Integrity:** Implement a pure Python stack conversion engine without `eval()`, `exec()`, or external parsers.
- **Robust Tokenization:** Handle multi-character identifiers, multi-digit numbers, floating-point literals, scientific notation, and unary signs.
- **Syntax Validation:** Detect and gracefully report syntax anomalies (consecutive operators, unmatched parentheses, missing operands/operators).
- **Dual Visual Representation:** Deliver both an exact tabular trace and a vertical "stack vessel" diagram for every step.
- **Zero-Dependency Architecture:** Implement server-side routing, HTML generation, and responsive styling using Python's built-in `http.server`, standard HTML5, and pure CSS3.

## 5. Scope
The application covers:
- General arithmetic expressions over numbers and variable names.
- Operators: `+`, `-`, `*`, `/`, `%`, `^`, unary `+`, and unary `-`.
- Explicit nested parentheses and optional implicit multiplication.
- Educational visualization and step generation.
The application intentionally focuses on expression conversion and syntactic analysis; it does not evaluate numerical results, support custom functions (e.g. `sin(x)`), or persist user data to an external database.

## 6. Hardware and Software Requirements
- **Hardware:** Any standard x86-64 or ARM architecture computer (minimum 512 MB RAM, 50 MB free disk space).
- **Operating System:** Cross-platform (Windows 10/11, macOS, Linux).
- **Runtime Environment:** Python 3.8+ (standard library only).
- **Client Software:** Any modern web browser supporting HTML5 and CSS3 (Chrome, Edge, Firefox, Safari).

## 7. System Architecture

The application adopts a clean, decoupled **Model-View-Controller (MVC)** architectural pattern:

```
+-------------------------------------------------------------------+
|                        Client Web Browser                         |
|   (HTML5 Form / CSS3 Visual Vessel / Pure Server-Driven Navigation)|
+-------------------------------------------------------------------+
                                  |
                           HTTP GET / POST
                                  |
                                  v
+-------------------------------------------------------------------+
|                      server.py (Controller)                       |
|   - ThreadingHTTPServer & BaseHTTPRequestHandler                  |
|   - Form extraction (urllib.parse) & Security sanitization (html)  |
|   - Template filling & Static file delivery (style.css)           |
+-------------------------------------------------------------------+
                                  |
                         Dispatches Expression
                                  |
                                  v
+-------------------------------------------------------------------+
|                     converter.py (Model/Engine)                   |
|   1. Tokenizer (Regex lexical analysis)                           |
|   2. Pre-processor (Unary sign & Implicit mult resolution)        |
|   3. Syntax Validator (Parentheses & operator placement check)   |
|   4. Shunting-Yard Stack Converter (LIFO list engine)             |
|   5. Step Recorder (Snapshot generator per token)                 |
+-------------------------------------------------------------------+
```

## 8. DSA Concepts Used
1. **Stack (LIFO):** A linear data structure governed by Last-In, First-Out semantics. Implemented in Python using list operations `append()` (Push), `pop()` (Pop), and index `[-1]` (Peek).
2. **Operator Precedence:** Priority levels assigned to operators ensuring that higher-binding operations (e.g., exponentiation and multiplication) are processed before lower-binding operations (addition and subtraction).
3. **Associativity:**
   - *Left-associative* (`+`, `-`, `*`, `/`, `%`): When operators of equal precedence collide, the left operator is executed first. Stack top is popped.
   - *Right-associative* (`^`, unary `+`, unary `-`): Chained operations group right-to-left ($2^{3^2} = 2^{(3^2)}$). Incoming operator is pushed onto the stack without popping equal-precedence operators.
4. **Finite-State Validation:** Tracks lexical expectation (`expect_operand` vs `expect_operator`) to immediately catch consecutive operators or misplaced symbols.

## 9. Algorithm and Pseudocode

### Shunting-Yard Infix to Postfix Algorithm
```text
Initialize:
  stack = empty stack of operators
  output = empty list of output tokens
  steps = empty list of trace dictionaries

For each token T in input stream:
  Case 1: T is an Operand (number or variable identifier):
    Append T to output.
    Log step (T, Output, stack, output).

  Case 2: T is Left Parenthesis '(':
    Push T onto stack.
    Log step (T, Push, stack, output).

  Case 3: T is Unary Operator ('u+', 'u-'):
    Push T onto stack (unary has right-associativity).
    Log step (T, Push, stack, output).

  Case 4: T is Right Parenthesis ')':
    While stack is not empty and stack.top != '(':
      Popped_Op = stack.pop()
      Append Popped_Op to output.
    If stack is not empty and stack.top == '(':
      stack.pop() // Discard matching '('
    Log step (T, Pop, stack, output).

  Case 5: T is Binary Operator:
    While stack is not empty and stack.top != '(' and:
      (Precedence(stack.top) > Precedence(T)) OR
      (Precedence(stack.top) == Precedence(T) AND Associativity(T) == LEFT):
        Popped_Op = stack.pop()
        Append Popped_Op to output.
    Push T onto stack.
    Log step (T, Push, stack, output).

After all tokens are processed:
  While stack is not empty:
    Popped_Op = stack.pop()
    Append Popped_Op to output.
    Log step ([EOF], Pop, stack, output).

Return output joined by single spaces.
```

## 10. Flowchart

```
                 +-----------------------+
                 |    User Submits Expr   |
                 +-----------------------+
                             |
                             v
                 +-----------------------+
                 |  Tokenize Expression  |
                 +-----------------------+
                             |
                   Valid Tokens Found?
                     /               \
                  No                  Yes
                  /                     \
                 v                       v
      +--------------------+   +-----------------------+
      | Return Syntax Error|   |  Validate Token Flow  |
      +--------------------+   +-----------------------+
                                         |
                                Balanced Parens & Ops?
                                 /               \
                              No                  Yes
                              /                     \
                             v                       v
                  +--------------------+   +-----------------------+
                  | Return Syntax Error|   | Initialize Stack & Out|
                  +--------------------+   +-----------------------+
                                                     |
                                                     v
                                          +---------------------+
                                     +--> |  Fetch Next Token T |
                                     |    +---------------------+
                                     |               |
                                     |     Operand? --> Append to Output
                                     |     '('?     --> Push to Stack
                                     |     Unary?   --> Push to Stack
                                     |     ')'?     --> Pop to Output until '('
                                     |     Binary?  --> Pop higher/equal prec,
                                     |                  then Push T
                                     |               |
                                     |    More Tokens Remaining?
                                     +---       Yes / \ No
                                                       |
                                                       v
                                          +-----------------------+
                                          | Pop Remainder of Stack|
                                          +-----------------------+
                                                       |
                                                       v
                                          +-----------------------+
                                          | Render HTML & Vessels |
                                          +-----------------------+
```

## 11. Sample Input and Output Traces

### Example 1: `A + B * C`
- **Infix:** `A + B * C`
- **Postfix:** `A B C * +`
- **Trace Walkthrough:**
  1. Token `A`: Operand &rarr; Output: `A`, Stack: `[]`
  2. Token `+`: Stack empty &rarr; Push `+`, Stack: `[+]`
  3. Token `B`: Operand &rarr; Output: `A B`, Stack: `[+]`
  4. Token `*`: Precedence(`*`)=2 > Precedence(`+`)=1 &rarr; Push `*`, Stack: `[+, *]`
  5. Token `C`: Operand &rarr; Output: `A B C`, Stack: `[+, *]`
  6. End of input: Pop `*` &rarr; Output: `A B C *`, Stack: `[+]`
  7. End of input: Pop `+` &rarr; Output: `A B C * +`, Stack: `[]`

### Example 2: `total + price * (quantity - 2)`
- **Infix:** `total + price * (quantity - 2)`
- **Postfix:** `total price quantity 2 - * +`
- Demonstrates preservation of multi-character variable names without character fragmentation.

### Example 3: `2 ^ 3 ^ 2` (Right Associativity)
- **Infix:** `2 ^ 3 ^ 2`
- **Postfix:** `2 3 2 ^ ^`
- When the second `^` is scanned, the top of the stack is `^` (equal precedence). Because `^` is **right-associative**, the stack top is *not* popped. Both `^` operators are pushed and subsequently popped at the end.

### Example 4: `A * -B` (Unary Minus)
- **Infix:** `A * -B`
- **Postfix:** `A B u- *`
- The `-` following binary operator `*` is resolved as unary `u-` (precedence 3). Since 3 > 2, it pushes directly above `*`.

## 12. Time and Space Complexity

### Time Complexity: $\mathcal{O}(N)$
- **Tokenization:** Scanning an input string of length $L$ takes linear time $\mathcal{O}(L)$.
- **Validation:** Single linear pass over $N$ tokens takes $\mathcal{O}(N)$.
- **Conversion Loop:** Each of the $N$ tokens is pushed to the operator stack at most once and popped from the stack at most once. No token is ever visited more than a constant number of times.
- **Overall Time Complexity:** **$\mathcal{O}(N)$**, which is optimal.

### Space Complexity: $\mathcal{O}(N)$
- **Operator Stack:** In the worst-case scenario (e.g. all operators with strictly increasing precedence or deeply nested opening parentheses `((((...))))`), the stack holds at most $N$ elements $\mathcal{O}(N)$.
- **Output Token Buffer:** Stores exactly the operands and operators present in the expression $\mathcal{O}(N)$.
- **Visualization Snapshots:** Storing intermediate stack copies for the step table scales with the bounded expression length ($N \le 300$).
- **Overall Auxiliary Space Complexity:** **$\mathcal{O}(N)$**.

## 13. Comprehensive Test Cases
The project includes a 34-test unit test suite (`test_converter.py`) covering:
1. `TestArithmeticAndPrecedence`: Tests all basic operators, precedence order, left associativity (`A-B-C`), and right associativity (`2^3^2`).
2. `TestParenthesesHandling`: Simple grouping, dual groups `(A+B)*(C-D)`, nested grouping `A*(B+(C-D))`, and redundant parentheses `((A))`.
3. `TestNumbersAndIdentifiers`: Multi-digit integers `(12+8)*3`, decimals `3.5+2.25`, scientific notation `2.5e3+4` / `1E-4*x`, and identifiers with underscores.
4. `TestUnaryOperators`: Unary minus at expression start `-A+B`, after operator `A*-B`, with exponentiation `-A^B`, and unary plus `+A`.
5. `TestImplicitMultiplication`: Parentheses products `2(A+B)` and `(A+B)(C+D)`, number-variable adjacency `2x`, and strict rejection when disabled.
6. `TestSyntaxValidationErrors`: Consecutive operators (`A++B`, `A*/B`), missing operands (`A+`, `*A`), mismatched parentheses (`(A+B`, `A+B)`), empty parentheses (`()`), invalid characters (`@`, `$`), and length overflow.
7. `TestStepTraceAndInvariants`: Validates exact step-by-step traces against known manual conversions and verifies output growth and symbol conservation invariants.

## 14. Advantages and Limitations

### Advantages:
- **Zero External Dependencies:** Runs immediately on any computer with Python 3.8+ without `pip install`.
- **Pure JavaScript-Free Interaction:** Uses standard HTML5 form submissions and semantic GET/POST navigation, ensuring 100% functionality even in restricted or script-disabled environments.
- **Security-First Design:** Strict absence of `eval()` or `exec()`; comprehensive HTML escaping prevents Cross-Site Scripting (XSS); payload size limits prevent denial-of-service.
- **Pedagogical Clarity:** High-contrast dark navy UI with color-coded chips and clear physical stack vessel diagrams.

### Limitations:
- Maximum expression length is bounded to 300 characters to ensure responsive visual table rendering.
- Mathematical function calls (e.g., `sin(x)`, `max(a, b)`) and postfix factorial (`!`) are not part of the standard grammar.
- Does not compute the numeric result of the postfix expression.

## 15. Future Enhancements
- **Postfix Expression Evaluator:** Add an interactive numerical evaluation engine demonstrating how postfix simplifies execution using an operand stack.
- **Expression Tree Generator:** Render a pure CSS binary expression tree representing the hierarchical syntax of the formula.
- **Prefix (Polish Notation) Mode:** Add support for right-to-left scanning to generate Polish prefix notation alongside postfix notation.
- **Step Navigation Controls:** Implement pure CSS radio-button pagination to allow clicking through steps sequentially without JavaScript.

## 16. Conclusion
The **Infix to Postfix Visual Converter** successfully demonstrates how abstract Data Structures and Algorithms principles can be implemented and made tangible through clean software engineering. By constraining the implementation strictly to Python's standard library, HTML5, and CSS3, the project serves as an ideal reference implementation for students, educators, and software engineers seeking to master stack operations, operator precedence mechanics, and zero-dependency web application architecture.
