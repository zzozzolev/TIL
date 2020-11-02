### 소모 시간
- 처음에 풀 때 잘 못 풀어서 다시 풀었음.

### 통과율
- 100%

### 접근법
- `A`와 `B`를 각각 체크하는 리스트를 만든다. 쓰이지 않은 경우 0을 쓰이는 경우 1을 원소로 갖는다.
- `A`와 `B`의 인덱스는 한 번만 쓰일 수 있으므로 한 번 쓰였을 때 1로 할당하고 이후에 다시 쓰이지 않도록 한다.
- 두 개가 동시에 쌍으로 묶이므로 `A`하나만 체크해도 충분하다. 따라서 쌍의 개수는 `A`를 체크하는 리스트의 sum이다.
- 만약 0보다 크고 `len(A)`보다 작다면 `B`의 원소 중 하나를 변경시켜 `A`의 원소 중 하나와 같게 만들 수 있으므로 1을 더하고 `len(A)`와 같다면 변경 시킨 경우 하나의 쌍이 없어지므로 1을 뺀다.

### 문제점
- 처음에는 쓸데없이 복잡하게 짜서 거의 다 실패했었다.
- 고치고나서 문제를 잘못 이해해서 선택적으로 B를 고칠 수 있다는 건 줄 알았는데 무조건 고치는 거였다. 그래서 count에서 1을 빼주지 않아서 통과를 못했었다.

### my solution
```
def beautifulPairs(A, B):
    a_check = [0] * len(A)
    b_check = [0] * len(B)

    for i in range(len(A)):
        for j in range(len(B)):
            if b_check[j] != 1:
                if A[i] == B[j]:
                    a_check[i] = 1
                    b_check[j] = 1
                    break

    count = sum(a_check)
    if 0 < sum(a_check) < len(A):
        count += 1
    elif sum(a_check) == len(A):
        count -= 1
    
    return count
```
