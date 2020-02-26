### Manifest Constants: `#define`
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

### File Inclusion: `#include`
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

### The `#undef` Directive
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

### The `#ifdef`, `#else`, and `#endif` Directives
- The `#ifdef` directive says that if the following identifier has been defined by the preprocessor, follow all the directives and compile all the C code up to the next `#else` or `#endif`, whichever comes first. If there is an `#else`, everything from the `#else` to the `#endif` is done if the identifier isn't defined.
- You can use this approach, for example, to help in program debugging.

### The `#ifndef` Directive
- The `#ifndef` asks whether the following identifier is not defined; `#ifndef` is the negative of `#ifdef`.
- Typically, this idiom is used to prevent multiple definitions of the same macro when you include several header files, each of which may contain a definition.

### The `#if` and `#elif` Directives
- The `#if` directive is more like the regular C `if`.
- Instead of using `#ifdef VAX` you can use this form: `#if defined (VAX)`. Here, `defined` is a preprocessor operator that returns `1` if its argument is `#defined` and `0` otherwise. The advantage of this newer form is that it can be used with `#elif`.

### Predefined Macros
- `__DATE__`: A character string literal in the form "Mmm dd yyyy" representing the date of preprocessing
- `__FILE__`: A character string literal representing the name of the current source code file
- `__TIME__`: The time of translation in the form "hh:mm:ss"
- 번외 `__func__`: expands to a string representing the name of the function containing the identifier (a C language predefined identifier rather than a predefined macro.)

### `#error`
- The `#error` directive causes the preprocessor to issue an error message that includes any text in the directive.

### Inline Functions
- Making a function an inline function may shortcut the usual function call mechanism, or it may do nothing at all.
- The way to create an inline function is to use the function specifier `inline` in the function declaration.
```
#include <stdio.h>
inline void eatline()   // inline definition/prototype
{
    while (getchar() != '\n')
        continue;
}

int main()
{
...
    eatline();  // function call
...    
}
```
- The inline function definition has to be in the same file as the function call. For this reason, an inline function ordinarily has internal linkage. 
- The simplest way to accomplish this is to put the inline function definition in a header file and then include the header file in those files that use the function. An inline function is an exception to the rule of not placing executable code in a header file.

### The General Utilities Library
- The general utilities library contains a grab bag of functions, including a random-number generator, searching and sorting functions, conversion functions, and memory-management functions. 
- Under ANSI C, prototypes for these functions exist in the `stdlib.h` header file.

### The `exit()` and `atexit()` Functions
- `atexit()`은 function을 register하고 `exit()`이 call 됐을 때 마지막에 추가된 순서로 실행하게 만들어줌.
- ANSI C defined a macro called `EXIT_FAILURE` that can be used portably to indicate failure. Similarly, it defined `EXIT_SUCCESS` to indicate success, but `exit()` also accepts `0` for that purpose.
- Using the `exit()` function in a nonrecursive `main()` function is equivalent to using the keyword `return`. However, `exit()` also terminates programs when used in functions other than `main()`.

### The `qsort()` Function
- `void qsort (void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));`
- `qsort` 예제
```
#include <stdio.h>
#include <stdlib.h>

#define NUM 40
int mycomp(const void * p1, const void * p2);

int main(void)
{
    double vals[NUM];
    ...
    qsort(vals, NUM, sizeof(double), mycomp);
    return 0;
}

/* sort by increasing value */
int mycomp(const void * p1, const void * p2)
{
    /* need to use pointers to double to access values */
    const double * a1 = (const double *) p1; // you need to dereference a pointer to type double.
    const double * a2 = (const double *) p2;

    if (*a1 < *a2)
        return -1;
    else if (*a1 == *a2)
        return 0;
    else
        return 1;
}
```
- C and C++ treat pointer-to-`void` differently. C++ requires a type cast when assigning a `void *` pointer to a pointer of another type, whereas C doesn't have that requirement.

### The Assert Library
- The assert library, supported by the `assert.h` header file, is a small one designed to help with debugging programs. It consists of a macro named `assert()`.
- If you think you've eliminated the program bugs, place the macro definition `#define NDEBUG` before the location where `assert.h` is included and then recompile the program, and the compiler will deactivate all `assert()` statements in the file.

### `memcpy()` and `memmove()` from the `string.h` Library
- `strcpy()` and `strncpy()` 처럼 looping 없이 array copy하는 편의성 제공.
- The `memcpy()` is free to assume that there is no overlap between the two memory ranges. (같은 array에서 copy하는 거)
- The `memmove()` function doesn't make that assumption, so copying takes place as if all the bytes are first copied to a temporary buffer before being copied to the final destination.
- Note that for an array, the number of bytes is not, in general, the number of elements. So if you were copying an array of 10 `double` values, you would use `10*sizeof(double)`, not `10`, as the third argument.

### Variable Arguments: `stdarg.h`
- variadic macros와 비슷한 기능을 함.
- The prototype for such a function should have a parameter list with at least one parameter followed by ellipses:
```
void f1(int n, ...);    // valid
int f2(const char * s, int k, ...);     // valid
char f3(char c1, ..., char c2);     // invalid, ellipses not last
double f3(...);     // invalid, no parameter
```
- The actual argument passed to this parameter will be the number of arguments represented by the ellipses section.
```
f1(2, 200, 400);    // 2 additional arguments
```
- Next, the `va_list` type, which is declared in the `stdargs.h` header file, represents a data object used to hold the parameters corresponding to the ellipses part of the parameter list. The beginning of a definition of a variadic function would look something like this:
```
double sum(int lim,...)
{
    va_list ap;
...
```
- After this, the function will use the `va_start()` macro, also defined in `stdargs.h`, to copy the argument list to the `va_list`variable.
```
va_start(ap, lim);      // initialize ap to argument list
```
- The next step is gaining access to the contents of the argument list. This involves using `va_arg()`, another macro. It takes two arguments: a type `va_list` variable and a `type` name. The first time it's called, it returns the first item in the list; the next time it's called, it returns the next item, and so on.
```
double tic;
int toc;
tic = va_arg(ap, double);   // retrieve first argument
toc = va_arg(ap, int);  // retrieve second argument       
```
- Finally, you should clean up by using the `va_end()` macro. It may, for example, free memory dynamically allocated to hold the arguments.
```
va_end(ap);     // clean up
```
- Because `va_arg()` doesn't provide a way to back up to previous arguments, it may be useful to preserve a copy of the `va_list` type variable. C99 has added a macro for that purpose. It's called `va_copy()`.