# Load Balancing
- [Client Side Load Balancing Vs Server Side Load Balancing: How Client Side Load Balancing works?](http://soaessentials.com/client-side-load-balancing-vs-server-side-load-balancing-how-client-side-load-balancing-works/)을 번역했다.

## 레이어에 따른 분류
- L4: 네트워크와 트랜스포트 레이어 프로토콜에서 동작한다. IP, 포트 이용. (IP, TCP, FTP, UDP)
- L7: HTTP 같이 애플리케이션 레이어 프로토콜에 있는 데이터를 기반으로 요청들을 나눈다. 쿠키, 리소스 확장자에 따른 라우팅 등 더 많은 작업을 할 수 있다.

## 알고리즘
- 업계에서 많이 쓰이는 알고리즘은 다음과 같다고 한다.
- Round robin: 서버에 번갈아 가면서 요청을 보내는 것.
- Least connections: 가장 적은 active 커넥션이 있는 서버를 고른다.
- Least response time: 가장 적은 active 커넥션이 있고 가장 적은 평균 응답 시간을 가지는 서버를 고른다.

## Server Side Load Balancing
- 서버 사이드 로드 밸런서는 클라이언트와 서버군 사이에 있다.
- 들어오는 네트워크와 어플리케이션 트래픽을 받고 여러 백앤드 서버에 트래픽을 분산시킨다.
- 대게 로드 밸런서는 아래에 있는 서버 풀의 헬스를 체크한다.

## Client Side Load Balancing
- 서버 사이드 로드 밸런싱은 클라이언트의 요청들을 서버로 분산 시킬 책임이 있는 중간에 있는 컴포넌트이다.
- 하지만 클라이언트 사이트 로드 밸런싱은 리퀘스트를 포워딩할 서버를 직접 고른다.
- 동작 방식은 간단하다.
- 클라이언트가 서버 IP의 리스트를 가지고 있다.
- 클라이언트는 랜덤하게 IP를 고르고 해당 서버에 요청을 보낸다.
- MSA에서는 클라이언트 사이드 로드 밸런싱이 중요한 역할을 한다.
- 네플릭스 Ribbon과 Eureka를 예시로 들 수 있는데 한 번 살펴보자.
- (위의 링크에서 그림 참고) 예를 들어 마이크로 서비스 B가 마이크로 서비스 C와 통신하고 싶다고 해보자.
- 그러면 마이크로 서비스 B는 클라이언트이고 Eureka 클라이언트를 사용해 마이크로 서비스 C에서 어떤 노드들이 가능한지 알아낼 것이다.
- 그다음 마이크로 서비스 B에 있는 ribbon 클라이언트를 이용해서 마이크로 서비스 C를 호출할 것이다.
- 이때 바로 ribbon 클라이언트가 한 것을 클라이언트 사이드 로드 밸런싱이라고 한다.
- 서버 사이드 로드 밸런싱처럼 중간에 있는 클라이언트를 호출할 필요 없이 클라이언트가 어떤 서버에 연결할지를 결정한다.
