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

## 문자열 자르기 `strtok`
- `string.h`에 존재
- `strtok(대상문자열, 기준문자); char *strtok(char *_String, char const *_Delimiter)`: 자른 문자열을 반환, 더 이상 자를 문자열이 없으면 `NULL`을 반환
- NULL을 넣었을 때는 직전 strtok 함수에서 처리했던 문자열에서 잘린 문자열만큼 다음 문자로 이동한 뒤 다음 문자열을 자름. 
```
#include <stdio.h>
#include <string.h>    // strtok 함수가 선언된 헤더 파일

int main()
{
    char s1[30] = "The Little Prince";  // 크기가 30인 char형 배열을 선언하고 문자열 할당

    char *ptr = strtok(s1, " ");      // " " 공백 문자를 기준으로 문자열을 자름, 포인터 반환

    while (ptr != NULL)               // 자른 문자열이 나오지 않을 때까지 반복
    {
        printf("%s\n", ptr);          // 자른 문자열 출력
        ptr = strtok(NULL, " ");      // 다음 문자열을 잘라서 포인터를 반환
    }

    return 0;
}

// The
// Little
// Prince
```
- pointer를 사용하는 경우, 아래와 같이 `malloc`과 `strcpy` 사용.
```
char *s1 = malloc(sizeof(char) * 30);    // char 30개 크기만큼 동적 메모리 할당

strcpy(s1, "The Little Prince");    // s1에 문자열 복사

char *ptr = strtok(s1, " ");    // 동적 메모리에 들어있는 문자열은 자를 수 있음

while (ptr != NULL)
{
   printf("%s\n", ptr);
   ptr = strtok(NULL, " ");
}

free(s1);    // 동적 메모리 해제
```
- 다음과 같이 delimiter에 여러 개 지정 가능.
```
char s1[30] = "2015-06-10T15:32:19";    // 크기가 30인 char형 배열을 선언하고 문자열 할당
char *ptr = strtok(s1, "-T:");    // -, T, 콜론을 기준으로 문자열을 자름
                                      // 포인터 반환

while (ptr != NULL)               // 자른 문자열이 나오지 않을 때까지 반복
{
    printf("%s\n", ptr);          // 자른 문자열 출력
    ptr = strtok(NULL, "-T:");    // 다음 문자열을 잘라서 포인터를 반환
}
// 2015
// 06
// 10
// 15
// 32
// 19
```
- 자른 문자열 보관하는 법.
```
#include <stdio.h>
#include <string.h>    // strtok 함수가 선언된 헤더 파일

int main()
{
    char s1[30] = "The Little Prince";    // 크기가 30인 char형 배열을 선언하고 문자열 할당
    char *sArr[10] = { NULL, };    // 크기가 10인 문자열 포인터 배열을 선언하고 NULL로 초기화
    int i = 0;                     // 문자열 포인터 배열의 인덱스로 사용할 변수

    char *ptr = strtok(s1, " ");   // 공백 문자열을 기준으로 문자열을 자름

    while (ptr != NULL)            // 자른 문자열이 나오지 않을 때까지 반복
    {
        sArr[i] = ptr;             // 문자열을 자른 뒤 메모리 주소를 문자열 포인터 배열에 저장
        i++;                       // 인덱스 증가

        ptr = strtok(NULL, " ");   // 다음 문자열을 잘라서 포인터를 반환
    }
    return 0;
}
```