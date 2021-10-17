## @Configuration
### 사용하는 이유
- singleton을 보장하기 위해서

### 원리
- CGLIB를 이용해 해당 클래스를 상속받은 클래스를 만들어준다.
- 원래 클래스에서는 새로운 객체를 만들었지만, 만들어진 클래스에서는 이미 스프링 컨테이너로 등록돼있다면 등록된 컨테이너를 사용하고 그렇지 않을 때만 새로 객체를 만든다.