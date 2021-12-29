## 정렬하기
- arrays sort와 기본형 박싱 클래스의 `compare` 메서드를 이용한다,
```java
Arrays.sort(intervals, (i1, i2) -> Integer.compare(i1[0], i2[0]));
```
- 만약 다중 정렬이 필요하다면 `Comparator`의 `thenComparing`을 이용한다. 기본형은 기본형을 위한 메서드를 이용한다.
```java
Comparator.comparing(Employee::getAge)
        .thenComparing(Employee::getName);
```
```java
Arrays.sort(intervals, Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]))
```
