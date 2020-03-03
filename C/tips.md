## Initializing every elements in array and pointer to zero
```
# array
int a[10] = {0, };
int a2[5][4] = {0, };

# pointer
int *a;
memset(a, 0, sizeof(int) * 10);

int **a;
a = malloc(sizeof(int *) * 5);
for (int i = 0; i < 5; i++)
{
   memset(a[i], 0, sizeof(int) * 4); 
}
```

## Variable Length Array or malloc?
- https://softwareengineering.stackexchange.com/questions/143858/array-or-malloc
- use malloc
- 근데 2차원에서 `memfree`하는 거 너무 번거로움.

## char * vs char[]
- size가 다름.
- `char *`의 경우 읽기 전용으로 선언 이후에 요소를 변경할 수 없지만 `char[]`의 경우 요소를 변경할 수 있음.