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