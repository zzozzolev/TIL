## Testing the Web Layer
- [공식 문서](https://spring.io/guides/gs/testing-web/)
  - `MockMvc`를 통한 테스트 방법 가이드
- [블로그](https://shinsunyoung.tistory.com/52)
  - GET, POST 테스트 방법을 예제를 통해 설명

## `@WebMvcTest` vs `@AutoConfigureMockMvc`
### 공통점
- `MockMvc`를 사용할 때 필요하다.
### `@WebMvcTest`
- 컨트롤러 테스트에 사용한다.
- `@SpringBootTest`와 같이 사용할 수 없다.

### `@AutoConfigureMockMvc`
- 컨트롤러 뿐만 아니라 테스트 대상이 아닌 `@Service`나 `@Repository`가 붙은 객체들도 모두 메모리에 올린다.

### 참고
- https://we1cometomeanings.tistory.com/65

## MockMvcResult
- `MockMvcResult`에서는 응답에서 쿠키를 받을 수 없다.
- [참고](https://stackoverflow.com/a/26281932)
