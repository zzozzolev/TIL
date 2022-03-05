## 스프링 부트는 왜 사용할까?
- 복잡한 설정을 할 필요가 없도록 한다.
- WAS인 tomcat 서버를 내장해 별도로 설치하고 War를 빌드해서 배포할 필요가 없도록한다. 빌드 결과인 Jar에 tomcat이 포함돼있다.

## Object Mapper
- Spring MVC는 `HttpMessageConverters`를 사용한다.
- 만약 Jackson을 사용하면 `com.fasterxml.jackson.databind.Module`이 디폴트 `ObjectMapper`로 등록된다.
- 따라서 `ObjectMapper`를 bean으로 등록하면 원래 동작하던 게 동작하지 않을 수 있다.
- 특히, `writeValueAsString`이 디폴트와 다르게 동작한다. 디폴트는 객체를 json string으로 바꿔주지만 `ObjectMapper`를 그대로 bean으로 등록하면 다르게 나온다.
  ```
  // spring boot default ObjectMapper 사용 시
  {"username":"test2","bio":"bio"}

  // ObjectMapper를 직접 생성했을 때
  {"username":{"empty":false,"present":true},"bio":{"empty":false,"present":true}} 
  ```
