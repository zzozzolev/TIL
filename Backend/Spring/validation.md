## 참고
- [공식 문서](https://beanvalidation.org/2.0/spec/#builtinconstraints)

## 스프링에서 validator 동작 원리
- 스프링 부트가 `spring-boot-starter-validation` 라이브러리를 넣으면 자동으로 Bean Validator를 인지하고 스프링에 통합한다.
- `LocalValidatorFactoryBean`을 글로벌 밸리데이터로 등록한다.
- 이 밸리데이터는 검증 애노테이션을 보고 검즘을 수행한다.
- 검증을 원하는 파라미터에 `@Valid`, `@Validated`만 적용하면 된다.
- 검증 오류가 발생하면 `FieldError`, `ObjectError`를 생성해서 `BindingResult`에 담아준다.

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
