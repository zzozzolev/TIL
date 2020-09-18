# 핵심
- x와 y 각각에서 서로 다른 어레이의 오른쪽 보다 작으면서 각각의 파티션의 개수를 똑같게 만드는 포인트를 찾는다.
```
x -> x1, x2 | x3, x4, x5, x6
y -> y1, y2, y3, y4, y5 | y6, y7, y8

even: avg(max(x2, y5) + min(x3, y6))
odd: max(x2, y5)

time complexity: O(log(min(m, n)))
```

# 절차
1. `start = 0`, `end = len(x)-1`, `partition_x = (start + end) / 2`, `partition_y = (len(x) + len(y) + 1) / 2 - partition_x`로 초기화한다. 이때 partition은 개수를 의미한다.
2. `maxLeftX <= minRightY and maxLeftY <= minRightX`인지 확인한다.
3-1. 만약 `maxLeftX > minRightY`라면 `partition_x`를 왼쪽으로 이동한다. -> `start = partition_x + 1` 
3-2. 만약 `maxLeftY > minRightX`라면 `partition_x`를 오른쪽으로 이동한다.

# 예시
```
x -> 1, 3, 8, 9, 15
y -> 7, 11, 18, 19, 21, 25
```

```
x -> 1, 3 | 8, 9, 15
y -> 7, 11, 18, 19 | 21, 25

19(maxLeftY) > 8(minRightX) -> move x to right
```

```
x -> 1, 3, 8 | 9, 15
y -> 7, 11, 18 | 19, 21, 25

18(maxLeftY) > 9(minRightX) -> move x to right
```

```
x -> 1, 3, 8, 9 | 15
y -> 7, 11 | 18, 19, 21, 25

9(maxLeftX) < 18(minRightY)
11(maxLeftY) < 15(minRightX)
Done
```


# Reference
- https://www.youtube.com/watch?v=LPFhl65R7ww&t=1013s