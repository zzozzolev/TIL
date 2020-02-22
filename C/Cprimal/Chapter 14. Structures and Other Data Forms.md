### Setting Up the Structure Declaration
- A member can be any C data type—and that includes other structures.
- If the declaration is placed inside a function, its tag can be used only inside that function. If the declaration is external, it is available to all the functions following the declaration in the file.
- The process of declaring a structure and the process of defining a structure variable can be combined into one step. Combining the declaration and the variable definitions, as shown here, is the one circumstance in which a tag need not be used. -> lambda 이런 느낌이네
```
struct { /* no tag */ 
    char title[MAXTITL]; 
    char author[MAXAUTL]; 
    float value;
} library;
```

### Initializing a Structure
- If you are initializing a structure with static storage duration, the values in the initializer list must be constant expressions.

### Designated Initializers for Structures
- initializing하는 방법
```
struct book gift = { .value = 25.99,
                     .author = "James Broadfool",
                     .title = "Rue for the Toad"};
```
- The last value supplied for a particular member is the value it gets.
```
// The value 0.25 is assigned to the `value` member
struct book gift= { .value = 18.90,
                    .author = "Philionna Pestle",
                    0.25};
```

### Declaring and Initializing a Structure Pointer
- Unlike the case for arrays, the name of a structure is not the address of the structure; you need to use the `&` operator.

### Member Access by Pointer
- The first method, and the most common, uses a new operator, `->`.
```
him->income is fellow[0].income if him == &fellow[0]
```
- The second method for specifying the value of a structure member follows from this sequence: If `him == &fellow[0]`, then `*him == fellow[0]` because `&` and `*` are reciprocal operators. Hence, by substitution, you have the following:
```
// The parentheses are required because the . operator has higher precedence than *.
fellow[0].income == (*him).income
```

### Telling Functions About Structures
- Of course, if you want a called function to affect the value of a member in the calling function, you can transmit the address of the member.
- Note that you must use the & operator to get the structure's address. Unlike the array name, the structure name alone is not a synonym for its address.

### More on Structure Features
- Modern C allows you to assign one structure to another. This causes each member of n_data to be assigned the value of the corresponding member of o_data.
```
o_data = n_data; // assigning one structure to another
```

### Structures or Pointer to Structures?
- The disadvantage is that you have less protection for your data. Some operations in the called function could inadvertently affect data in the original structure. However, the ANSI C addition of the const qualifier solves that problem.
- One advantage of passing structures as arguments is that the function works with copies of the original data, which is safer than working with the original data. Also, the programming style tends to be clearer.
- The two main disadvantages to passing structures are that older implementations might not handle the code and that it wastes time and space. It's especially wasteful to pass large structures to a function that uses only one or two members of the structure. In that case, passing a pointer or passing just the required members as individual arguments makes more sense.
- Typically, programmers use structure pointers as function arguments for reasons of efficiency, using const when needed to protect data from unintended changes.

### Character Arrays or Character Pointers in a Structure
- So if you want a structure to store the strings, use character array members. Storing pointers- to-char has its uses, but it also has the potential for serious misuse.
- One instance in which it does make sense to use a pointer in a structure to handle a string is if you use `malloc()` to allocate memory and use a pointer to store the address.
- Make sure you understand that the two strings are not stored in the structure. They are stored in the chunk of memory managed by `malloc()`.

### Compound Literals and Structures (C99)
- You can use compound literals to create a structure to be used as a function argument or to be assigned to another structure. The syntax is to preface a brace-enclosed initializer list with the type name in parentheses. For example, the following is a compound literal of the `struct book` type:
```
(struct book) {"The Idiot", "Fyodor Dostoyevsky", 6.99}
```

### Flexible Array Members (C99)
- One special property is that the array doesn't exist—at least, not immediately. The second special property is that, with the right code, you can use the flexible array member as if it did exist and has whatever number of elements you need.
- Here are the rules for declaring a flexible array member:
    - The flexible array member must be the last member of the structure.
    - There must be at least one other member.
    - The flexible array is declared like an ordinary array, except that the brackets are empty.
- 근데 memory가 자동으로 할당되지 않기 때문에 `malloc ()`으로 memory를 직접 할당해줘야 됨.
```
struct flex 
{
    int count;
    double average;
    double scores[]; // flexible array member
};

struct flex * pf; // declare a pointer
// ask for space for a structure and an array
pf = malloc(sizeof(struct flex) + 5 * sizeof(double));
```

### Functions Using an Array of Structures
- You can use the array name to pass the address of the first structure in the array to a function.
- You can then use array bracket notation to access the successive structures in the array.

### Saving the Structure Contents in a File
- The entire set of information held in a structure is termed a *record*, and the individual items are *fields*.
- We chose the binary mode because `fread()` and `fwrite()` are intended for binary files.
- The `rewind()` command ensures that the file position pointer is situated at the start of the file, ready for the first read.

### Unions: A Quick Look
- A *union* is a type that enables you to store different data types in the same memory space (but not simultaneously). A typical use is a table designed to hold a mixture of types in some order that is neither regular nor known in advance.
- list된 거 중 가장 큰 size를 이용. 
- You can initialize a union to another union of the same type, you can initialize the first element of a union, or, with C99, you can use a designated initializer:
```
union hold valA;
valA.letter = 'R';
union hold valB = valA; // initialize one union to another union hold valC = {88}; // initialize digit member of union union hold valD = {.bigfl = 118.2}; // designated initializer
```
- You can use the `->` operator with pointers to unions in the same fashion that you use the operator with pointers to structures.

### Enumerated Types
- You can use the *enumerated* type to declare symbolic names to represent integer constants.
- The first declaration establishes `spectrum` as a tag name, which allows you to use `enum` `spectrum` as a type name. The second declaration makes `color` a variable of that type. The identifiers within the braces enumerate the possible values that a `spectrum` variable can have. Therefore, the possible values for `color` are `red`, `orange`, `yellow`, and so on. Then, you can use statements such as the following:
```
enum spectrum {red, orange, yellow, green, blue, violet}; 
enum spectrum color;

int c;
color = blue;
if (color == yellow)
    ...;
for (color = red; color <= violet; coloc++)
    ...;
```

### `enum` Constants
- By default, the constants in the enumeration list are assigned the integer values 0, 1, 2, and so on.
- You can choose the integer values that you want the constants to have. Just include the desired values in the declaration:
```
enum levels {low = 100, medium = 500, high = 2000};
```
- If you assign a value to one constant but not to the following constants, the following constants will be numbered sequentially.
```
enum feline {cat, lynx = 10, puma, tiger};
```
- Then `cat` is `0`, by default, and `lynx`, `puma`, and `tiger` are `10`, `11`, and `12`, respectively.
- string을 `enum`과 조합해서 사용하고 싶으면 `const char[]`를 선언해서 사용하면 됨.

### `typedef`: A Quick Look
- The `typedef` facility is an advanced data feature that enables you to create your own name for a type. It is similar to `#define` in that respect, but with three differences.
    - Unlike `#define`, `typedef` is limited to giving symbolic names to types only and not to values.
    - The `typedef` interpretation is performed by the compiler, not the preprocessor.
    - Within its limits, `typedef` is more flexible than `#define`.
- Often, uppercase letters are used for these definitions to remind the user that the type name is 513 really a symbolic abbreviation, but you can use lowercase, too.
- `typedef`는 선언할 때 같은 라인에 있는 거 모두 해당 타입으로 변경해주지만 `#define`의 경우는 그렇지 않음.
```
typedef char * STRING;
STRING name, sign; // menas char * name, * sign;

#define STRING char *
STRING name, sign; // means char * name, sign;
```
- You can use typedef with structures, too.  One reason to use `typedef` is to create convenient, recognizable names for types that turn up often.
- A second reason for using `typedef` is that `typedef` names are often used for complicated types.
```
/*
makes FRPTC announce a type that is a function that returns a pointer to a five-element array of
char.
*/
typedef char (* FRPTC ()) [5];
```

### Functions and Pointers
- When declaring a function pointer, you have to declare the type of function pointed to. To specify the function type, you indicate the return type for the function and the parameter types for a function.
```
void ToUpper(char *); // convert string to uppercase
void (*pf)(char *); // pf a pointer-to-function
```
- Probably the simplest way to create this declaration is to note that it replaces the function name `ToUpper` with the expression `(*pf)`.
- As mentioned earlier, the first parentheses are needed because of operator precedence rules. Omitting them leads to something quite different:
```
void *pf(char *); // pf a function that returns a pointer
```
