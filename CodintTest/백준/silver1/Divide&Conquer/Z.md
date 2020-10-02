### 소모 시간
- 44분 24초

### 통과 여부
- non-pass (메모리 초과)

### 문제점
- 처음에 굳이 2차원 배열을 사용할 필요가 없다고 생각해서 안 쓰려고 했지만 좀 까다로울 것 같아서 사용하니 메모리 초과가 나버렸다. 2 ** 15 여서 애초에 배열로 접근했으면 안 됐을 것 같다.

### my solution
```
from sys import setrecursionlimit

setrecursionlimit(10**4)

def main():
    n, r, c = list( map(int, input().split()) )
    matrix = [ [-1] * 2 ** n for _ in range(2 ** n) ]
    visit(matrix, 2 ** n * 2 ** n, 0, len(matrix), 0, len(matrix))

    print(matrix[r][c])

def visit(matrix, num, r_start, r_end, c_start, c_end):
    global COUNT
    if num == 4:
        matrix[r_start][c_start] = COUNT
        matrix[r_start][c_start+1] = COUNT + 1
        matrix[r_start+1][c_start] = COUNT + 2
        matrix[r_start+1][c_start+1] = COUNT + 3
        COUNT = COUNT + 4
        return
    
    divided = num // 4
    offset = int(num ** 0.5 // 2) 
    visit(matrix, divided, r_start, r_start + offset, c_start, c_start + offset)
    visit(matrix, divided, r_start, r_start + offset, c_start + offset, c_end)
    visit(matrix, divided, r_start + offset, r_end, c_start, c_start + offset)
    visit(matrix, divided, r_start + offset, r_end, c_start + offset, c_end)

if __name__ == "__main__":
    COUNT = 0
    main()
```

### other solution
- 출처: https://hini7.tistory.com/30
```
import math

N,c,r = map(int,input().split()) #c: y, r: x

def findLocation(loc_index,x,y,n): # 위치 정보 반환
    if n==1: # 가장 작은 Z모양일 때
        return loc_index

    location = 0
    if x<pow(2,n-1):
        if y<pow(2,n-1):
            location = 1
        else:
            location = 3
            y-=pow(2,n-1)
    else:
        if y<pow(2,n-1):
            location = 2
            x-=pow(2,n-1)
        else:
            location = 4
            x-=pow(2,n-1)
            y-=pow(2,n-1)
    loc_index.append(location)
    return findLocation(loc_index,x,y,n-1)


def calIndex(loc_index,n,sum):
    if n!=1:
        for i in range(n-2,-1,-1): # 몇번째 Z인지
            sum+=int(pow(4,n-i-1)*(loc_index[i]-1))
    if r%2: # Z상의 위치 파악
        if c%2:
            sum+=3
        else: 
            sum+=1
    else:
        if c%2:
            sum+=2
        #else:sum+=0
    return sum


location_array = list()
location_array = findLocation(location_array,r,c,N)
if len(location_array)==N-1:
    print(calIndex(location_array,N,0))
else:
    print("error")
```