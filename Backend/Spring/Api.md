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
