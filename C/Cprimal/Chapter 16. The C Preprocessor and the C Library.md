### Manifest Constants: #define
- 상수를 정의할 때 `\`를 이용해서 여러 라인으로 정의할 수 있음.
- 단순 상수뿐만 아니라 연산, 함수 등을 미리 정의해서 사용할 수 있음.
```
#define TWO 2
#define FOUR TWO*TWO
#define PX printf("X is %d.\n", x)

int x = FOUR;
PX;
```
- Each `#define` line (logical line, that is) has three parts. The first part is the `#define` directive itself. The second part is your chosen abbreviation, known as a *macro*. Some macros represent values; they are called *object-like macros*. The third part is termed the *replacement list* or *body*. When the preprocessor finds an example of one of your macros within your program, it almost always replaces it with the body. 
- macro와 달리 `const` keyword를 initialization에 쓸 수 없음.
```
#define LIMIT 20
const int LIM = 50;
static int data1[LIMIT]; // valid 
static int data2[LIM]; // invalid 
const int LIM2 = 2 * LIMIT; // valid 
const int LIM3 = 2 * LIM; // invalid
```
- The character string interpretation views the spaces as part of the body, but the token interpretation views the spaces as separators between the tokens of the body.
- Others allow redefinition, perhaps issuing a warning. Having the same definition means the bodies must have the same tokens in the same order. Therefore, these two definitions agree:
```
#define SIX 2 * 3
#define SIX 2  *  3
```
Both have the same three tokens, and the extra spaces are not part of the body. The next definition is considered different:
```
#define SIX 2*3
```
It has just one token, not three, so it doesn't match. (실제로 gcc compile 해보면 warning이 뜬다.) 
If you do have constants that you need to redefine, it might be easier to use the `const` keyword and scope rules to accomplish that end.
- `...` and `_ _VA_ARGS_ _`를 이용해서 argument를 dynamic하게 넘겨줄 수 있음.
```
#define PR(X, ...) printf("Message " #X ": " _ _VA_ARGS_ _)

int main(void)
{   
    PR(1, "x = %g\n", x);
    PR(2, "x = %.2f, y = %.4f\n", x, y);
}
```
- Programmers typically use macros for simple functions such as the following:
```
#define MAX(X,Y)    ((X) > (Y) ? (X) : (Y))
#define ABS(X)   ((X) < 0 ? -(X) : (X))
#define ISSIGN(X)   ((X) == '+' || (X) == '-' ? 1 : 0)
```
- Use capital letters for macro function names. This convention is not as widespread as that of using capitals for macro constants. 
- A macro inside a nested loop is a much better candidate for speed improvements.

### File Inclusion: #include
- When the preprocessor spots an `#include` directive, it looks for the following filename and includes the contents of that file within the current file.
```
#include <stdio.h> # Searches system directories
#include "hot.h"  # Searches your current working directory 
#include "/usr/biff/p.h" # Searches the /usr/biff directory
```
- None of these things are executable code; rather, they are information that the compiler uses when it creates executable code.

### Uses for Header Files
- Manifest constants
- Macro functions
- Function declarations
- Structure template definitions
- Type definitions

### The #undef Directive
- The `#undef` directive "undefines" a given `#define`.
- If you want to use a particular name and you are unsure whether it has been used previously, you can undefine it to be on the safe side.
- *define* 됐다는 것의 의미는 *macro*를 의미하는 것임. 따라서 일반 변수 혹은 상수를 의미하는 게 아님.
```
#define LIMIT 1000 // LIMIT is defined 
#define GOOD // GOOD is defined 
#define A(X) ((-(X))*(X)) // A is defined

int q; // q not a macro, hence not defined
#undef GOOD // GOOD not defined
```

### The #ifdef, #else, and #endif Directives
- The `#ifdef` directive says that if the following identifier has been defined by the preprocessor, follow all the directives and compile all the C code up to the next `#else` or `#endif`, whichever comes first. If there is an `#else`, everything from the `#else` to the `#endif` is done if the identifier isn't defined.
- You can use this approach, for example, to help in program debugging.

### The #ifndef Directive
- The `#ifndef` asks whether the following identifier is not defined; `#ifndef` is the negative of `#ifdef`.
- Typically, this idiom is used to prevent multiple definitions of the same macro when you include several header files, each of which may contain a definition.

### The #if and #elif Directives
- The `#if` directive is more like the regular C `if`.
- Instead of using `#ifdef VAX` you can use this form: `#if defined (VAX)`. Here, `defined` is a preprocessor operator that returns `1` if its argument is `#defined` and `0` otherwise. The advantage of this newer form is that it can be used with `#elif`.

### Predefined Macros
- `__DATE__`: A character string literal in the form "Mmm dd yyyy" representing the date of preprocessing
- `__FILE__`: A character string literal representing the name of the current source code file
- `__TIME__`: The time of translation in the form "hh:mm:ss"
- 번외 `__func__`: expands to a string representing the name of the function containing the identifier (a C language predefined identifier rather than a predefined macro.)