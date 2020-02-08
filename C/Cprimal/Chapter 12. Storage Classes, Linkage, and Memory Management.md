### Storage Classes
- The different storage classes offer different combinations of scope, linkage, and storage duration.

### Scope
- All the compiler cares about when handling a function prototype argument is the types; the names you use, if any, normally don't matter. One case in which the names matter a little is with variable-length array parameters:
```
void use_a_VLA(int n, int m, ar[n][m]);
```

### Linkage
- A C variable has one of the following linkages: external linkage, internal linkage, or no linkage. Variables with block scope or prototype scope have no linkage. A variable with file scope can have either internal or external linkage. A variable with external linkage can be used anywhere in a multifile program. A variable with internal linkage can be used anywhere in a single file.
```
int giants = 5; // file scope, external linkage static int dodgers = 3; // file scope, internal linkage
```

### Storage Duration
- A C variable has one of the following two storage durations: static storage duration or automatic storage duration. If a variable has static storage duration, it exists throughout program execution. Variables with file scope have static storage duration. Variables with block scope normally have automatic storage duration. These variables have memory allocated for them when the program enters the block in which they are defined, and the memory is freed when the block is exited.
    |Storage Class|Duration|Scope|Linkage|How Declared|
    |---|---|---|---|---|
    |`automatic`|Automatic|Block|None|In a block|
    |`automatic`|Automatic|Block|None|In a block with the keyword `register`|
    |`static` with external|Static|File|External|Outside of all functions|
    |`static` with internal|Static|File|Internal|Outside of all functions with the keyword `static`|
    |`static` with no linkage|Static|Block|None|In a block with the keyword `static`|

### Automatic Variables
- By default, any variable declared in a block or function header belongs to the automatic storage class. The keyword `auto` is termed a storage class *specifier*. 
- Block scope and no linkage implies that only the block in which the variable is defined can access that variable by name. 
- Normally, you wouldn't use this feature(inner block) when designing a program. Sometimes, however, it is useful to define a variable in a sub-block if it is not used elsewhere.
- Automatic variables are not initialized unless you do so explicitly. The `repid` variable ends up with whatever value happened to previously occupy the space assigned to `repid`. You cannot rely on this value being `0`.
```
int repid;
```

### Register Variables
- Variables are normally stored in computer memory. With luck, register variables are stored in the CPU registers or, more generally, in the fastest memory available, where they can be accessed and manipulated more rapidly than regular variables. Because a register variable may be in a register rather than in memory, you can't take the address of a register variable. A variable is declared by using the storage class specifier register:
```
register int quick;
```
- 근데 선언한다고 모두 register variable이 되는 건 아님. 그렇게 처리할 수 없으면 그냥 automatic variable이 됨.

### Static Variables with Block Scope
- Variables with file scope automatically have static storage duration. These variables have the same scope as automatic variables, but they don't vanish when the containing function ends its job.
- Static variables are initialized to zero if you don't explicitly initialize them to some other value.
- 함수 내에서 static variable 초기화하는 부분을 넣어도 skip 될 거임.
- You can't use static for function parameters:
```
int wontwork(static int flu); // not allowed
```

### Static Variables with External Linkage
- A static variable with external linkage has file scope, external linkage, and static storage duration. This class is sometimes termed the external storage class, and variables of this type are called external variables. As a matter of documentation, an external variable can additionally be declared inside a function that uses it by using the extern keyword. If the variable is defined in another file, declaring the variable with extern is mandatory.
- function 내부에서 automatic variable이 아닌 external linkage를 쓰려면 `extern` keyword 사용.

### Initializing External Variables
- Unlike the case for automatic variables, you can use only constant expressions to initialize file scope variables:
```
int x = 10; // ok, 10 is constant
int y = 3 + 20; // ok, a constant expression size_t z = sizeof(int); // ok, a constant expression int x2 = 2 * x; // not ok, x is a variable
```

### External Names
- The C99 standard requires compilers to recognize the first 63 characters for local identifiers and the first 31 characters for external identifiers.

### Definitions and Declarations
- The first declaration is called a defining declaration, and the second is called a referencing declaration. The keyword extern indicates that a declaration is not a definition because it instructs the compiler to look elsewhere.
```
int tern = 1; /* tern defined */
main()
{
    external int tern; /* use a tern defined elsewhere */
```
- Don't use the keyword `extern` to create an external definition; use it only to refer to an existing external definition.
```
extern char permis = 'Y'; /* error */
```

### Static Variables with Internal Linkage
- Variables of this storage class have static storage duration, file scope, and internal linkage. You create one by defining it outside of any function (just as with an external variable) with the storage class specifier `static`:
```
int traveler = 1; // external linkage
static int stayhome = 1; // internal linkage
int main() 
{
    extern int traveler; // use global traveler
    extern int stayhome; // use global stayhome
    ...
```

### Multiple Files
- Complex C programs often use several separate files of code. Sometimes these files might need to share an external variable.

### Storage-Class Specifiers
- you can't use one of the other storage-class specifiers as part of a `typedef`.
- The `auto` specifier indicates a variable with automatic storage duration. It can be used only in declarations of variables with block scope, which already have automatic storage duration, so its main use is documenting intent.
- The `register` specifier also can be used only with variables of block scope. It puts a variable into the register storage class, which amounts to a request that the variable be stored in a register for faster access. It also prevents you from taking the address of the variable.
- The `static` specifier, when used in a declaration for a variable with block scope, gives that variable static storage duration so it exists and retains its value as long as the program is running, even at times the containing block isn't in use. The variable retains block scope and no linkage. When used in a declaration with file scope, it indicates that the variable has internal linkage.
- The `extern` specifier indicates that you are declaring a variable that has been defined elsewhere. If the declaration containing `extern` has file scope, the variable referred to must have external linkage. If the declaration containing `extern` has block scope, the referred-to variable can have either external linkage or internal linkage, depending on the defining declaration for that variable.

### Storage Classes and Functions
- A function can be either external (the default) or static.
- An external function can be accessed by functions in other files, but a static function can be used only within the defining file.

### Allocated Memory: `malloc()` and `free()`
- C goes beyond this. You can allocate more memory as a program runs. The main tool is the `malloc()` function, which takes one argument: the number of bytes of memory you want.
- The memory is anonymous; that is, `malloc()` allocates memory but it doesn't assign a name to it. However, it does return the address of the first byte of that block. Therefore, you can assign that address to a pointer variable and use the pointer to access the memory.
- The ANSI C standard, however, uses a new type: pointer-to-`void`. This type is intended to be a "generic pointer."
- Assigning a pointer-to-`void` value to a pointer of another type is not considered a type clash. 
- If `malloc()` fails to find the required space, it returns the null pointer.
- This code requests space for 30 type `double` values and sets `ptd` to point to the location. Note that `ptd` is declared as a pointer to a single double and not to a block of 30 `double` values. Remember that the name of an array is the address of its first element. Therefore, if you make ptd point to the first element of the block, you can use it just like an array name.
- Normally, you should balance each use of `malloc()` with a use of `free()`. The `free()` function takes as its argument an address returned earlier by `malloc()` and frees up the memory that had been allocated.
- The argument to `free()` should be a pointer to a block of memory allocated by `malloc()`; you can't use `free()` to free memory allocated by other means, such as declaring an array. 

### The Importance of `free()`
- pointer는 automatic variable로 function이 끝나면 사라지지만 이게 가리키던 여전히 남아있어서 재활용을 못 함.
- This sort of problem is called a `memory leak`, and it could have been prevented by having a call to `free()` at the end of the function.

### The `calloc()` Function
- `malloc()`이랑 argument 똑같음. 
- It sets all the bits in the block to zero.

### Dynamic Memory Allocation and Variable-Length Arrays
- One difference is that the VLA is automatic storage. One consequence of automatic storage is that the memory space used by the VLA is freed automatically when the execution leaves the defining block. Therefore, you don't have to worry about using `free()`.
-  On the other hand, the array created using `malloc()` needn't have its access limited to one function.
- VLAs are more convenient for multidimensional arrays. You can create a two-dimensional array using `malloc()`, but the syntax is awkward.

### ANSI C Type Qualifiers
- `const`, `volatile`, `restrict`
- you can use the same qualifier more than once in a declaration, and the superfluous(필요 없는) ones are ignored.
-  In short, a const anywhere to the left of the `*` makes the data constant, and a const to the right of the `*` makes the pointer itself constant.

### Using `const` with Global Data
- You can have `const` variables, `const` arrays, and `const` structures.
```
/* file1.c -- defines some global constants */ const double PI = 3.14159;
const char * MONTHS[12] =
{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
/* file2.c -- use global constants defined elsewhere */ extern const double PI;
extern const * MONTHS[];
```
- The advantage of the header file approach is that you don't have to remember to use defining declarations in one file and reference declarations in the next; all files simply include the same header file. The disadvantage is that the data is duplicated. For the preceding examples, that's not a real problem, but it might be one if your constant data includes enormous arrays.
```
/* constant.h -- defines some global constants */ static const double PI = 3.14159;
static const char * MONTHS[12] =
{"January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
/* file1.c -- use global constants defined elsewhere */ #include "constant.h"
/* file2.c -- use global constants defined elsewhere */ #include "constant.h"
```

### The volatile Type Qualifier
- The `volatile` qualifier tells the compiler that a variable can have its value altered by agencies other than the program.

### The restrict Type Qualifier
- The `restrict` keyword enhances computational support by giving the compiler permission to optimize certain kinds of code. It can be applied only to pointers, and it indicates that a pointer is the sole initial means of accessing a data object.
- You can use the `restrict` keyword as a qualifier for function parameters that are pointers. This means that the compiler can assume that no other identifiers modify the pointed-to data within the body of the function.
