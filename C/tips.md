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

## 문자열 포인터로 `strcpy` 하기
```
#include <stdio.h>
#include <string.h>    // strcat 함수가 선언된 헤더 파일
#include <stdlib.h>    // malloc, free 함수가 선언된 헤더 파일

int main()
{
    char *s1 = "world";                      // 문자열 포인터
    char *s2 = malloc(sizeof(char) * 20);    // char 20개 크기만큼 동적 메모리 할당

    strcpy(s2, "Hello");   // s2에 Hello 문자열 복사

    strcat(s2, s1);       // s2 뒤에 s1을 붙임

    printf("%s\n", s2);   // Helloworld

    free(s2);    // 동적 메모리 해제

    return 0;
}
```

## NULL(0) vs NUL('\0')
- `NULL`: `stdio.h`에 정의돼 있음. 0 주소를 의미하기 때문에 포인터 변수를 초기화 시에 사용.
- `NUL`: null 문자.