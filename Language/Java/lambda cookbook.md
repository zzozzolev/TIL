## 정렬하기
- arrays sort와 기본형 박싱 클래스의 `compare` 메서드를 이용한다,
```java
Arrays.sort(intervals, (i1, i2) -> Integer.compare(i1[0], i2[0]));
// 내림차순 정렬
List<List<Integer>> gasIndexPairs = new ArrayList<>();
gasIndexPairs.sort((a, b) -> b.get(0).compareTo(a.get(0)));
```
- 만약 다중 정렬이 필요하다면 `Comparator`의 `thenComparing`을 이용한다. 기본형은 기본형을 위한 메서드를 이용한다.
```java
Comparator.comparing(Employee::getAge)
        .thenComparing(Employee::getName);
```
```java
// 메서드 체이닝에서는 자바가 타입을 추론하지 못하기 때문에 타입을 명시해준다.
Arrays.sort(intervals, Comparator.<int[]>comparingInt(e -> e[0]).thenComparingInt(e -> e[1]))
```

## 빈도수 세기
- `groupingBy`와 다운스트림 수집기로 `counting`을 사용한다.
```java
// list가 List<String>으로 가정
Map<String, Long> freq = list.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
```
