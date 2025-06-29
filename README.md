# C++ to Python Converter 

## Overview
The C++ to Python Converter is a web-based tool built using Pyodide, PLY (Python Lex-Yacc), HTML, and JavaScript. It takes C++ code as input, parses it using a lexer and parser, and generates equivalent Python code. The tool runs in a browser, leveraging Pyodide’s WebAssembly environment to execute Python code and the PLY library for lexical analysis and parsing.

## Supported C++ Constructs
The converter, implemented in `transpiler.py`, supports the following C++ constructs, converting them to equivalent Python code:

1. **Preprocessor Directives**:
   - `#include <iostream>` and `#include <string>`: Recognized and skipped (no Python equivalent needed, as Python uses built-in `print` for output).
   - Example:
     ```cpp
     #include <iostream>
     ```
     Output: Skipped in Python, no code generated.

2. **Variable Declarations**:
   - `int` and `float` declarations with or without initialization.
   - Examples:
     ```cpp
     int x = 5;
     float y = 3.14;
     int z;
     ```
     Output:
     ```python
     x = 5
     y = 3.14
     z = 0
     ```

3. **Assignments**:
   - Variable assignments using `=`.
   - Example:
     ```cpp
     int x = 5;
     x = 10;
     ```
     Output:
     ```python
     x = 5
     x = 10
     ```

4. **Increment Operations**:
   - Postfix increment (`i++`) in loops or standalone statements.
   - Example:
     ```cpp
     int i = 1;
     i++;
     ```
     Output:
     ```python
     i = 1
     i = i + 1
     ```

5. **Output Statements**:
   - `cout << expression` with or without `endl`.
   - Example:
     ```cpp
     cout << "Hello" << endl;
     cout << 42;
     ```
     Output:
     ```python
     print("Hello", end='\n')
     print(42, end='')
     ```

6. **If-Else Statements**:
   - Simple and nested `if` and `if-else` constructs with comparison operators (`<`, `>`, `&&`, `||`, `!`).
   - Example:
     ```cpp
     int x = 20;
     if (x > 15) {
         cout << "Greater" << endl;
     } else {
         cout << "Smaller" << endl;
     }
     ```
     Output:
     ```python
     x = 20
     if x > 15:
         print("Greater", end='\n')
     else:
         print("Smaller", end='\n')
     ```

7. **For Loops**:
   - `for (int i = start; i < end; i++)` style loops.
   - Example:
     ```cpp
     for (int i = 0; i < 5; i++) {
         cout << i << endl;
     }
     ```
     Output:
     ```python
     for i in range(0, 5):
         print(i, end='\n')
     ```

8. **While Loops**:
   - `while (condition)` loops with increment operations.
   - Example:
     ```cpp
     int i = 1;
     while (i <= 3) {
         cout << i << endl;
         i++;
     }
     ```
     Output:
     ```python
     i = 1
     while i <= 3:
         print(i, end='\n')
         i = i + 1
     ```

9. **Function Definitions**:
   - Functions with `int` return type and parameters.
   - Example:
     ```cpp
     int add(int a, int b) {
         return a + b;
     }
     ```
     Output:
     ```python
     def add(a, b):
         return a + b
     ```

10. **Class Definitions**:
    - Simple classes with `int` or `float` member variables (no methods or access specifiers).
    - Example:
      ```cpp
      class MyClass {
          int x;
          int y;
      };
      ```
      Output:
      ```python
      class MyClass:
          def __init__(self):
              self.x = 0
              self.y = 0
      ```

11. **Arithmetic and Logical Expressions**:
    - Supports `+`, `-`, `*`, `/`, `<`, `>`, `&&`, `||`, `!`.
    - Example:
      ```cpp
      int x = 5 + 3 * 2;
      ```
      Output:
      ```python
      x = 5 + 3 * 2
      ```

## Limitations
The converter has the following limitations:
- **Unsupported Constructs**:
  - Pointers, references, or memory management (`new`, `delete`).
  - Templates or generics.
  - `using namespace std;`.
  - Complex expressions with multiple operators beyond basic arithmetic and logical.
  - Function overloading or default arguments.
  - Access specifiers (`public`, `private`) in classes.
  - Complex `cout` chains (e.g., `cout << x << y;`).
- **Error Handling**: Errors like `Syntax error at '='` may occur if the input doesn’t match expected grammar, though recent fixes have improved robustness.
- **Increment Translation**: `i++` is translated to `i = i + 1` (can be changed to `i += 1` if desired).
- **Line Numbers**: Error reporting is accurate for most cases but may misreport in complex inputs.

## How It Works
1. **Lexer (`transpiler.py`)**:
   - Uses PLY’s lexer to tokenize C++ input.
   - Recognizes tokens like `IDENTIFIER`, `NUMBER`, `INCLUDE`, `PLUSPLUS`, etc.
   - Handles `#include <identifier>` as a single token and tracks line numbers with `t_newline`.

2. **Parser (`transpiler.py`)**:
   - Builds an Abstract Syntax Tree (AST) using PLY’s parser.
   - Supports grammar for declarations, loops, conditionals, functions, classes, and increments.
   - Updated to handle `#include` directives and `i++` correctly.

3. **Code Generator (`transpiler.py`)**:
   - Traverses the AST to generate Python code.
   - Maps C++ constructs to Python equivalents (e.g., `cout << x << endl` to `print(x, end='\n')`).

4. **JavaScript Integration (`main.js`)**:
   - Loads Pyodide and PLY, writes `transpiler.py` to the virtual file system, and executes the `transpile` function.
   - Escapes triple quotes in input to prevent string literal issues.
   - Uses cache-busting (`?t=`) to ensure fresh `transpiler.py` loading.

5. **Web Interface (`index.html`)**:
   - Provides a UI with textareas for C++ input and Python output, a convert button, and error display.
   - Loads Pyodide and `main.js` via CDN.

## Tested Sample Inputs
Below are sample inputs tested with the converter, along with their outputs:

1. **Class Definition** (Confirmed Working):
   ```cpp
   #include <iostream>
   class MyClass {
       int x;
       int y;
   };
   int main() {
       cout << "Class defined" << endl;
       return 0;
   }
   ```
   **Output**:
   ```python
   class MyClass:
       def __init__(self):
           self.x = 0
           self.y = 0
   def main():
       print("Class defined", end='\n')
       return 0
   ```

2. **While Loop** (Now Working with Latest Fix):
   ```cpp
   #include <iostream>
   int main() {
       int i = 1;
       while (i <= 3) {
           cout << i << endl;
           i++;
       }
       return 0;
   }
   ```
   **Output**:
   ```python
   def main():
       i = 1
       while i <= 3:
           print(i, end='\n')
           i = i + 1
       return 0
   ```

3. **Simple Declaration** (Previously Working):
   ```cpp
   #include <iostream>
   int main() {
       int x = 5;
       cout << x << endl;
       return 0;
   }
   ```
   **Output**:
   ```python
   def main():
       x = 5
       print(x, end='\n')
       return 0
   ```

## Recommendations for Improvement
- **Add Support for `i += 1`**: Modify `generate_code` for `increment` to use `+=`:
  ```python
  elif node.type == 'increment':
      result += f"{indent_str}{node.value} += 1\n"
  ```
- **Extend Parser**: Add rules for `using namespace std;`, pointers, or complex `cout` chains.
- **Enhance UI**: Include syntax highlighting for C++ and Python using libraries like Prism.js.
- **Execute Python Output**: Add a button to run the generated Python code in Pyodide.
- **Better Error Messages**: Include C++ code snippets in error outputs for clarity.

## Deployment Notes
- **Files**: Use `index.html` (artifact ID: a9337ba1-00ef-42d5-bed4-4a900047839d), `transpiler.py` (artifact ID: b04eeb79-db15-468f-b255-da60f07fc812), and `main.js` (artifact ID: 470c8240-1aec-4639-ad6b-9af68e266bdd).
- **Hosting**: Run `python -m http.server 8000` and access at `http://localhost:8000`.
- **Cache**: Clear browser cache or use incognito mode to ensure latest files are loaded.
- **Dependencies**: Requires internet for Pyodide and PLY.
