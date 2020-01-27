-  Sometimes you might use an array that's intended to be a read-only array. That is, the program will retrieve values from the array, but it won't try to write new values into the array. In such cases, you can, and should, use the `const` keyword when you declare and initialize the array.
- If you don't initialize array members, they might have any value. (Variables and arrays of some of the other storage classes have their contents set to 0 if they are not initialized.) If you partially initialize an array, the remaining elements are set to 0.
- When you use empty brackets to initialize an array, the compiler counts the number of items in the list and makes the array that large.
- The `sizeof` operator gives the size, in bytes, of the object, or type, following it. So `sizeof days` is the size, in bytes, of the whole array, and `sizeof days[0]` is the size, in bytes, of one element. Dividing the size of the entire array by the size of one element tells us how many elements are in the array. (그켬)
- With C99, you can use an index in brackets in the initialization list to specify a particular
element. 
```
int arr[6] = {[5] = 212}; // initialize arr[5] to 212
```
- designated initializers. First, if the code follows a designated initializer with further values, as in the `sequence [4] = 31,30,31,` these further values are used to initialize the subsequent elements. That is, after initializing `days[4]` to `31`, the code initializes `days[5]` and `days[6]` to `30` and `31`, respectively. Second, if the code initializes a particular element to a value more than once, the last initialization is the one that takes effect. (override)
- C doesn't let you assign one array to another as a unit. Nor can you use the list-in-braces form except when initializing.
```
/* nonvalid array assignment */ 
#define SIZE 5
int main(void)
{
    int oxen[SIZE] = {5,3,2,8}; /* ok here */
    int yaks[SIZE];
    yaks = oxen; /* not allowed */
    yaks[SIZE] = oxen[SIZE]; /* invalid */
    yaks[SIZE] = {5, 3, 2, 8}; /* doesn't work */
}
```
- Then it's your responsibility to make sure the program uses indices only in the given range, because the compiler won't check for you. (세상에...)
- Using out-of-bounds array indices resulted in the program altering the value of other variables.
- C trusts the programmer to do the coding correctly and rewards the programmer with a faster program. Of course, not all programmers deserve that trust, and then problems can arise. (재능충을 위한 언어...)
- One simple thing to remember is that array numbering begins with 0. One simple habit to develop is to use a symbolic constant in the array declaration and in other places the array size is used.
- Initializing two dimensional array 
```
int sq[2][3] = {
    {5, 6},
    {7, 8}
};

/*
[
    [5, 6, 0],
    [7, 8, 0]
]
*/

int sq[2][3] = {5, 6, 7, 8};

/*
[
    [5, 6, 7],
    [8, 0, 0]
]
*/
```
- A name of array is the address of the first element
- pointer에 +1을 하면 일반 산술처럼 주소값이 1 증가하는 게 아니라 pointer의 type만큼 증가한다. 예를 들면 short type의 pointer에 +1을 하면 2 byte(16 bit) 만큼 증가한다.
- `*(array + index) == array[index]`. This turns out to be important when you have a function with an array as an argument.
- Suppose you want to write a function that operates on an array. What would the prototype be? `int sum (int ar[], int n);` The first parameter tells the function where to find the array and the type of data in the array, and the second parameter tells the function how many elements are present.
- main에서 `sizeof` 하는 거랑 function argument로 array 넘겨주고 안에서 `sizeof` 하는 거랑 다름. 후자는 array 자체가 아닌 첫번째 element 주소값
- 그냥 상수값을 그대로 넘겨주는 방법 말고도 어디서 시작하고 끝나는지를 넘겨줄 수도 있음.
```
answer = sump(marbles, marbles + SIZE);

...

int sump(int * start, int * end)
{
    int total = 0;

    while (start < end)
    {
        total += *start;
        start++;
    }
    return total;
}

```
- `*start++;` The unary operators `*` and `++` have the same precedence but associate from right to left. This means the `++` applies to start, not to `*start`. That is, the pointer is incremented, not the value pointed to. The use of the postfix form (`start++` rather than `++start`) means that the pointer is not incremented until after the pointed-to value is added to total.
- pointer에 ++을 하더라도 pointing 하는 게 바뀌지 자체의 메모리 주소는 바뀌지 않는다.
- 같은 값을 pointing 할 수 있음.
- Do not dereference an uninitialized pointer. Remember, creating a pointer only allocates memory to store the pointer itself; it doesn't allocate memory to store data. Therefore, before you use a pointer, it should be assigned a memory location that has already been allocated.
```
int * pt;
*pt = 5;
```
### Protecting Array Contents
- If a function's intent is that it not change the contents of the array, use the keyword `const` when declaring the formal parameter in the prototype and in the function definition. It's important to understand that using const this way does not require that the original array be constant; it just says that the function has to treat the array as though it were constant.
- array 자체를 `const`로 선언할 수도 있고 pointer 자체를 `const`로 선언할 수도 있음. 근데 pointer 자체를 `const`로 선언했을 때 값을 할당하지 못하지만 다른 곳은 point하게 할 수 있음. 
```
const double * pd = rates;
*pd = 29.89; // not allowed
pd[2] = 222.22; // not allowed
pd++; // make pd point to rates[1] -- allowed
```
- A pointer-to-constant is normally used as a function parameter to indicate that the function won't use the pointer to change data.
- There are some rules you should know about pointer assignments and const. First, it's valid to assign the address of either constant data or nonconstant data to a pointer-to-constant. However, only the addresses of nonconstant data can be assigned to regular pointers.
```
double rates[5] = {88.99, 100.12, 59.45, 183.11, 340.5};
const double locked[4] = {0.08, 0.075, 0.0725, 0.07};

const double * pc = rates; // valid
pc = locked; // valid
pc = &rates[3]; //valid

double * pnc = rates; // valid
pnc = locked; // not valid
pnc = &rates[3]; // valid
```
- Therefore, using const in a function parameter definition not only protects data, it also allows the function to work with arrays that have been declared const.
- You can declare and initialize a pointer so that it can't be made to point elsewhere.
```
double rates[5] = {88.99, 100.12, 59.45, 183.11, 340.5};
double * const pc = rates;
pc = &rates[2]; // not allowed
*pc = 92.99; // ok -- changes rates[0]
```
### Multidimensional array
```
int zippo[4][2]; /* an array of arrays of ints */
*zippo = &zippo[0]
*zippo+2 = &zippo[1][0] // ?
```
- How would you declare a pointer variable pz that can point to a two-dimensional array such as zippo? `int (* pz)[2]; // pz points to an array of 2 ints` `[ ]`가 더 높은 우선 순위를 가지기 때문에 꼭 괄호를 해줘야 됨. Foraml parameter라면 `int pz[][2];` 이렇게 쓸 수도 있음. 앞에 있는 index에 숫자를 쓸 수 있지만 무시됨.
- you can use notation such as  `pz[2][1]`, even though pz is a pointer, not an array name.
### Variable-Length Arrays (VLAs)
- Here's how to declare a function with a two-dimensional VLA argument.
```
int sum2d(int rows, int cols, int ar[rows][cols]); // ar a VLA, rows와 cols 이전에 ar을 선언하면 error
```
- The C99 standard says you can omit names from the prototype; but in that case, you need to replace the omitted dimensions with asterisks.
```
int sum2d(int, int, int ar[*][*]); // ar a VLA, names omitted
```
### Compound Literals
- python에서 lambda 개념인가?
- Here's a compound literal that creates a nameless array containing the same two int
values.
```
(int [2]){10, 20} // a compound literal
```
- Because these compound literals are nameless, you can't just create them in one statement and then use them later. Instead, you have to use them somehow when you make them. One way is to use a pointer to keep track of the location.
- You can extend the technique to two-dimensional arrays, and beyond.
```
int (*pt2)[4]; // declare a pointer to an array of 4-int arrays pt2 = (int [2][4]) { {1,2,3,-9}, {4,5,6,-8} };
```