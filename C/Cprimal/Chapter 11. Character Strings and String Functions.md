- double quotation에 있는 거는 pointer

### Character String Arrays and Initialization
- When you specify the array size, be sure that the number of elements is at least one more (that null character again) than the string length.
- Often, it is convenient to let the compiler determine the array size; recall that if you omit the size in an initializing declaration, the compiler determines the size for you. ex) `const char m2[] = "If you can't think of anything, fake it.";`
- The name of a character array, like any array name, yields the address of the first element of the array. Therefore, the following holds for the array m1:
`m1 == &m1[0] , *m1 == 'L', and *(m1+1) == m1[1] == 'i'`
- Indeed, you can use pointer notation to set up a string.
```
const char *m3 = "\nEnough about me -- what's your name?";
char m3[] = "\nEnough about me -- what's your name?"
```

### Array Versus Pointer
- The quoted string is said to be in static memory. But the memory for the array is allocated only after the program begins running.
- One important point here is that in the array form, m3 is an address constant. You can't change m3, because that would mean changing the location (address) where the array is stored.
- Once the program begins execution, it sets aside one more storage location for the pointer variable m3 and stores the address of the string in the pointer variable. This variable initially points to the first character of the string, but the value can be changed. Therefore, you can use the increment operator. For instance, ++m3 would point to the second character (E).
- In short, initializing the array copies a string from static storage to the array (constant), whereas initializing the pointer merely copies the address of the string(variable). 
- array form으로 선언했을 때 바꾸는 방법은 개별 element에 접근해서 바꾸는 방법이 있음 -> The elements of an array are variables (unless the array was declared as const), but the name
is not a variable.
`heart[7]= 'M';`
- The compiler can replace each instance of "Klingon" with the same address. If the compiler uses this single-copy representation and allows changing p1[0] to 'F', that would affect all uses of the string, so statements printing the string literal "Klingon" would actually display "Flingon"
```
char * p1 = "Klingon";
p1[0] = 'F'; // ok? printf("Klingon");
printf(": Beware the %ss!\n", "Klingon");

// Flingon: Beware the Flingons!
```
- Therefore, the recommended practice for initializing a pointer to a string literal is to use the const modifier.
```
const char * pl = "Klingon"; // recommended usage
```

### Arrays of Character Strings
- It is often convenient to have an array of character strings. Then you can use a subscript to access several different strings. 
```
const char *mytal[LIM] = {
    "Adding numbers swiftly", 
    "Multiplying accurately", 
    "Stashing data", 
    "Following instructions to the letter", "Understanding the C language"
};
```
- One difference is that this second choice (`char mytal_2[LIM][LINLIM];`) sets up a rectangular array with all the rows of the same length. That is, 81 elements are used to hold each string. The array of pointers(`char *mytal[LIM];`), however, sets up a ragged array, with each row's length determined by the string it was initialized. This ragged array doesn't waste any storage space.
- Another difference is that mytal and mytal_2 have different types; mytal is an array of pointers-to-char, but mytal_2 is an array of arrays of char. In short, mytal holds five addresses, but mytal_2 holds five complete character arrays.

### Pointers and Strings
- string pointer를 다른 pointer에 assign하면 그냥 주소값만 넘겨주는 것임.

### String Output
- The `puts()` function is very easy to use. Just give it the address of a string for an argument. It stops when it encounters the null character.
- Unlike `printf()`, `puts()` automatically appends a newline when it displays a string.
- The expression `&str1[5]` is the address of the sixth element of the array `str1`. That element contains the character 'r', and that is what `puts()` uses for its starting point. Similarly, `str2+4` points to the memory cell containing the 'i' of "pointer", and the printing starts there.
```
char str1[80] = "An array was initialized to me."; 
const char * str2 = "A pointer was initialized to me.";
```
- Because dont lacks a closing null character, it is not a string, so `puts()` won't know where to stop.
```
char dont[] = {'W', 'O', 'W', '!' };
puts(dont);
```
- `fgets()` is designed for file I/O. It takes a second argument indicating the maximum number of characters to read. If this argument has the value n, `fgets()` reads up to n-1 characters or through the newline character, whichever comes first. If `fgets()` reads the newline, it stores it in the string. It takes a third argument indicating which file to read.
- The `fputs()` function is the file-oriented version of `gets()`. The `fputs()` function takes a second argument indicating the file to which to write. You can use stdout (for standard output), which is defined in `stdio.h`, as an argument to output to your display. Unlike `puts()`, `fputs()` does not automatically append a newline to the output.
- The point is that `puts()` is designed to work with `gets()`, and `fputs()` is designed to work with `fgets()`.
- One difference is that `printf()` does not automatically print each string on a new line. Instead, you must indicate where you want new lines.

### String Functions
- The C library supplies several string-handling functions; ANSI C uses the `string.h` header file to provide the prototypes.
- The `strlen()` function, as you already know, finds the length of a string. This function does change the string, so the function header doesn't use `const` in declaring the formal parameter `string`.
- The `strcat()` (for string concatenation) function takes two strings for arguments. A copy of the second string is tacked onto the end of the first, and this combined version becomes the new first string.
- The `strcat()` function does not check to see whether the second string will fit in the first array. If you fail to allocate enough space for the first array, you will run into problems as excess characters overflow into adjacent memory locations.
- Alternatively, you can use `strncat()`, which takes a second argument indicating the maximum number of characters to add. For example, `strncat(bugs, addon, 13)` will add the contents of the addon string to bugs, stopping when it reaches 13 additional characters or the null character, whichever comes first.
```
#define BUGSIZE 13
gets(bug);
available = BUGSIZE - strlen(bug) - 1;
strncat(bug, addon, available);
```
- `strcmp()` does for strings what relational operators do for numbers. In particular, it returns 0 if its two string arguments are the same. 
- One of the nice features of `strcmp()` is that it compares strings, not arrays. Therefore, `strcmp()` can be used to compare strings stored in arrays of different sizes.
- Comparing "A" to itself returns 0. Comparing "A" to "B" returns -1, and reversing the comparison returns 1. These results suggest that `strcmp()` returns a negative number if the first string precedes the second alphabetically and that it returns a positive number if the order is the other way.
```
strcmp("A", "A") is 0 
strcmp("A", "B") is -1 
strcmp("B", "A") is 1 
strcmp("C", "A") is 1
```
- Don't use ch or 'q' as arguments for strcmp().
- The `strncmp()` function compares the strings until they differ or until it has compared a number of characters specified by a third argument.
```
if (strncmp(list[i],"astro", 5) == 0)
```
- It is your responsibility to make sure the destination array has enough room to copy the source. The following is asking for trouble:
```
char * str;
strcpy(str, "The C of Tranquility");
```
- In short, `strcpy()` takes two string pointers as arguments. The second pointer, which points to the original string, can be a declared pointer, an array name, or a string constant. The first pointer, which points to the copy, should point to a data object, such as an array, roomy enough to hold the string. Remember, declaring an array allocates storage space for data; declaring a pointer only allocates storage space for one address.
- The `strcpy()` function has two more properties that you might find useful. First, it is type `char *`. It returns the value of its first argument—the address of a character. Second, the first argument need not point to the beginning of an array; this lets you copy just part of an array.
- Note that `strcpy()` copies the null character from the source string. In this example, the null character overwrites the first t in that in `copy` so that the new string ends with `beast`. Also note that `ps` points to the eighth element (index of 7) of copy because the first argument is `copy + 7`. Therefore, `puts(ps)` prints the string starting at that point.
```
#define WORDS "beast"

const char * orig = WORDS;
char copy[SIZE] = "Be the best that you can be.";
char * ps;

puts(orig);
puts(copy);
ps = strcpy(copy + 7, orig); puts(copy);
puts(ps);

beast
Be the best that you can be. 
Be the beast
beast
```
- The safer way to copy strings is to use `strncpy()`. It takes a third argument, which is the maximum number of characters to copy. 
- The function call `strncpy(target, source, n) `copies up to n characters or up through the null character (whichever comes first) from source to target. Therefore, if the number of characters in source is less than `n`, the entire string is copied, including the null character. The function never copies more than n characters, so if it reaches the limit before reaching the end of the source string, no null character is added. For this reason, the program sets n to one less than the size of the target array and then sets the final element in the array to the null character:
```
strncpy(qwords[i], temp, TARGSIZE - 1);
qwords[i][TARGSIZE - 1] = '\0';
```
- The `sprintf()` function is declared in stdio.h instead of string.h. It works like `printf()`, but it writes to a string instead of writing to a display.
- `char *strchr(const char * s, int c);` This function returns a pointer to the first location in the string `s` that holds the character `c`. (The terminating null character is part of the string, so it can be searched for.) The function returns the null pointer if the character is not found. (A reversed version is `char *strrchr(const char * s, int c);`)
- `char *strpbrk(const char * s1, const char * s2);` This function returns a pointer to the first location in the string `s1` that holds any character found in the `s2` string. The function returns the null pointer if no character is found.

### Command-Line Arguments
- main 선언 `int main(int argc, char *argv[])`
- 실행 방법 `<file name> <arg1> <arg2> ...`
- With two arguments, the first argument is the number of strings in the command line. This int argument is called `argc` for argument count. The second argument is an array of pointers to strings. This array of pointers is called `argv`, for argument values. When possible (some operating systems don't allow this), `argv[0]` is assigned the name of the program itself.
- Many programmers use a different declaration for `argv`. `argv` is a pointer to a pointer to `char`.
```
int main(int argc, char **argv)
```
- Incidentally, many environments, including Unix and DOS, allow the use of quotation marks to lump several words into a single argument.
```
repeat "I am hungry" now
```