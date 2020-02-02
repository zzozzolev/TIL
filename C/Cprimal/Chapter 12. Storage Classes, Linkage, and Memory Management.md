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
