## ES_JAVA_HOME
- 자신의 자바 버전을 사용하고 싶을 때 사용한다.
- 기본적으로 ES가 자바를 이용해 빌드되기 때문에 번들된 버전의 OpenJDK를 포함한다.
- 번들된 JVM이 추천되는 JVM이다.

## single node 구성
- 어떤 클러스터와도 조인시키지 않게 하기 위해서는 `discovery.type: single-node` 설정을 해줘야한다.

## cluster 구성
- 필요한 설정
  - cluster.name
    - 클러스터 이름을 공유해서 연결이 가능하다.
    - 따라서 같은 클러스터 이름을 사용하지 않도록 주의해야한다.
  - node.name
    - 노드의 용도와 목적을 이해하기 위해 읽을 수 있는 식별자로 작성하는 게 좋다.
    - ex) master-node, data-node 등등
  - discovery.seed_hosts
  - cluster.initial_master_nodes
  - node.roles
- 명시적 선언을 꼭 하는 게 좋다.
  - ex) 포트 설정
