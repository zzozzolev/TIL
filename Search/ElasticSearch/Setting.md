## ES_JAVA_HOME
- 자신의 자바 버전을 사용하고 싶을 때 사용한다.
- 기본적으로 ES가 자바를 이용해 빌드되기 때문에 번들된 버전의 OpenJDK를 포함한다.
- 번들된 JVM이 추천되는 JVM이다.

## single node 구성
- 어떤 클러스터와도 조인시키지 않게 하기 위해서는 `discovery.type: single-node` 설정을 해줘야한다.
