### The Text View and the Binary View
- When a C program takes the text view of an MS-DOS text file, it converts `\r\n` to `\n` when reading from a file, and it converts `\n` to `\r\n` when writing to a file. When a C program takes the text view of a Macintosh text file, it converts the `\r` to `\n` when reading from a file, and it converts `\n` to `\r` when writing to a file.

### Standard Files
- C programs automatically open three files on your behalf. They are termed the *standard input*, the *standard output*, and the *standard error output*.

### Checking for Command-Line Arguments
- In particular, the standard requires that the value 0 or the macro `EXIT_SUCCESS` be used to indicate successful termination, and the macro `EXIT_FAILURE` be used to indicate unsuccessful termination.
- After your program successfully opens a file, `fopen()` returns a file pointer, which the other I/O functions can then use to specify the file.
- The file pointer is of type pointer- to-`FILE`; `FILE` is a derived type defined in `stdio.h`. The pointer doesn't point to the actual file. Instead, it points to a data package containing information about the file.
- The `fopen()` function returns the null pointer (also defined in stdio.h) if it cannot open the file.

### The getc() and putc() Functions
- The two functions `getc()` and `putc()` work very much like `getchar()` and `putchar()`. The difference is that you must tell these newcomers which file to use.
- Uses `stdout` for the second argument of `putc()`. It is defined in `stdio.h` as being the file pointer associated with the standard output, so `putc(ch,stdout)` is the same as `putchar(ch)`.

### End-of-File
- The `getc()` function returns the special value `EOF` if it tries to read a character and discovers it has reached the end of the file.
- To avoid problems attempting to read an empty file, you should use an entry-condition loop.
```
// good design #2
int ch;
FILE * fp;
fp = fopen("wacky.txt", "r"); 
while (( ch = getc(fp)) != EOF) 
{
    putchar(ch); // process input 
}
```
- You should avoid a design of this sort:
```
// bad design (two problems) 
int ch;
FILE * fp;
fp = fopen("wacky.txt", "r");
while (ch != EOF) // ch undetermined value first use
{
    ch = getc(fp); // get input
    putchar(ch); // process input
}
```

### The `fclose()` Function
- The fclose(fp) function closes the file identified by fp, flushing buffers as needed. The function `fclose()` returns a value of `0` if successful, and `EOF` if not.

### Pointers to the Standard Files
- The `stdio.h` file associates three file pointers with the three standard files automatically opened by C programs:
    - standard input -> `stdin`
    - standard output -> `stdout`
    - standard error -> `stderr`

### The `fgets()` and `fputs()` Functions
- The `fgets()` function takes three arguments to the `gets()` function's one. The first argument, as with `gets()`, is the address (type `char *`) where input should be stored. The second argument is an integer representing the maximum size of the input string. The final argument is the file pointer identifying the file to be read. A function call, then, looks like this:
```
fgets(buf, MAX, fp);
// buf is the name of a char array, MAX is the maximum size of the string, and fp is the pointer-to-FILE
```
- If `fgets()` reads in a whole line before running into the character limit, it adds the newline character, marking the end of the line into the string, just before the null character.
- Like `gets()`, `fgets()` returns the value NULL when it encounters `EOF`. You can use this to check for the end of a file.
- Unlike puts(), fputs() does not append a newline when it prints. 
- Because `fgets()` can be used to prevent storage overflow, it is a better function than `gets()` for serious programming. Because it does read a newline into a string and because `puts()` appends a newline to output, `fgets()` should be used with `fputs()`.