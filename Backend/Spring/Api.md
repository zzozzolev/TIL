## 데이터 객체와 화면 객체를 분리
- 서비스 요구 사항이 간단할 때는 Entity로 바로 화면을 뿌려도 된다.
- 하지만 서비스가 복잡해지고 Entity에 화면 처리를 위한 기능이 들어가면 화면 종속적인 기능이 들어간다.
- 결국 유지보수가 어려워진다.
- 따라서 Entity는 핵심 비즈니스 로직만 담고 있어야한다.
- API를 제공할 때는 절대 Entity를 반환하면 안 되고 DTO를 사용해야한다.
  1. Entity에 중요한 정보를 담는 경우 그대로 노출된다.
  2. Entity에 로직을 추가하면 API 스펙이 변한다.

## List API에서 array가 아닌 object로 결과 내보내기
- 서비스에서 얻은 list를 바로 return하면 json array로 결과가 나가게 된다. 예를 들면 아래와 같다.
    ```json
    [
        {
            "id": 1,
        }
    ]
    ```
- 하지만 이렇게 하면 확장성이 떨어진다.
- 따라서 결과를 위한 객체를 만들면 object로 결과가 나가게 된다. 멤버 이름 그대로 API에 노출된다.
    ```java

    @Data
    @AllArgsConstructor
    static class Result<T> {
        private int count;
        private T data;
    }
    ```
    ```json
    {
        "count": 1,
        "data": [
            {
                "id": 1,
            }
        ]
    }
    ```

## Lazy 강제 초기화
- Lazy 로딩이 걸려있는 객체의 멤버를 가져오면 Lazy가 강제 초기화된다.
- 따라서 객체의 멤버들을 가져올 수 있다.
```java
public class Member {
    ...
    private String name;
    ...
}
```
```java
for (Order order : all) {
    order.getMember().getName(); // Lazy 강제 초기화
}
```

## N + 1 문제
- 1개의 쿼리를 날렸을 때 N개의 객체가 반환된다면 추가로 M * N번만큼의 쿼리가 추가로 발생할 수 있는 문제이다.
- 예를 들어, `Order` 객체에 `Member`, `Delivery`라는 객체가 연관 관계를 맺고 있다고 해보자.
- `Order`를 조회해서 2개의 `Order`를 가져왔고 이를 순회하면서 DTO로 만든다고 해보자.
- 이때 `Order` 하나당 `Member`, `Delivery`를 가져와야 하므로 2번의 쿼리가 추가로 필요하다.
- 즉, 1(`Order`) + 2 * (1(`Member`) + 1(`Delivery`)) = 5번의 쿼리가 필요하다.
- 다만 지연로딩인 경우 영속성 컨텐스트에서 조회하므로 이미 조회된 경우 쿼리를 생략한다.

### fetch join
- N + 1 문제의 해결 방법이다.
- 엔티티를 fetch join을 사용해서 쿼리 1번에 조회한다.
- fetch join에서 필요한 객체를 이미 조회했으므로 지연 로딩이 발생하지 않는다.
