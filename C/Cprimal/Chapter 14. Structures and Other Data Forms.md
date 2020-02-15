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
