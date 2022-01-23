## 참고
- [공식 문서](https://beanvalidation.org/2.0/spec/#builtinconstraints)

## 패키지
- `implementation 'org.springframework.boot:spring-boot-starter-validation'`를 추가한다.

## @Valid
- 스프링에 javax validation을 쓰는 것을 알려주는 역할을 한다.
```java
public class Form {
    @NotEmpty
    private String name;
    ...
}

public String create(@Valid Form form) {

}
```

## @NotNull, @NotEmpty, @NotBlank 차이
- [참고](https://sanghye.tistory.com/36)

## test 코드 작성
- [참고](https://www.baeldung.com/javax-validation)
