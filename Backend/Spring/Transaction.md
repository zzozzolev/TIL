## 트랜잭션 매니저와 트랜잭션 동기화 매니저 동작 방식
1. 서비스 계층에서 `transactionManager.getTransaction()`을 호출해서 트랜잭션을 시작한다.
2. 트랜잭션을 시작하려면 먼저 데이터베이스 커넥션이 필요하다. 트랜잭션 매니저는 내부에서 데이터소스를 사용해서 커넥션을 생성한다.
3. 커넥션을 수동 커밋 모드로 변경해서 실제 데이터베이스 트랜잭션을 시작한다.
4. 커넥션을 트랜잭션 동기화 매니저에 보관한다.
5. 트랜잭션 동기화 매니저는 쓰레드 로컬에 커넥션을 보관한다. 따라서 멀티 쓰레드 환경에 안전하게 커넥션을 보관할 수 있다.
6. 서비스는 비즈니스 로직을 실행하면서 레포의 메서드들을 호출한다. 이때 커넥션을 파라미터로 전달하지 않는다.
7. 레포 메서드들은 트랜잭션이 시작된 커넥션이 필요하다. 레포는 `DataSourceUtils.getConnection()`을 사용해서 트랜잭션 동기화 매니저에 보관된 커넥션을 꺼내서 사용한다. 이 과정을 통해서 자연스럽게 같은 커넥션을 사용하고, 트랜잭션도 유지된다.
8. 획득한 커넥션을 사용해서 SQL을 데이터베이스에 전달해서 실행한다.
9. 비즈니스 로직이 끝나고 트랜잭션을 종료한다. 트랜잭션은 커밋하거나 롤백하면 종료된다.
10. 트랜잭션을 종료하려면 동기화된 커넥션이 필요하다. 트랜잭션 동기화 매니저를 통해 동기화된 커넥션을 획득한다.
11. 획득한 커넥션을 통해 데이터베이스에 트랜잭션을 커밋하거나 롤백한다.
12. 전체 리소스를 정리한다.
  - 트랜잭션 동기화 매니저를 정리한다. 쓰레드 로컬은 사용후 꼭 정리해야한다.
  - 오토 커밋을 true로 되돌린다. 커넥션 풀을 고려해야한다.
  - `conn.close()`를 호출해 커넥션을 종료한다. 커넥션 풀을 사용하는 경우 커넥션 풀에 반환된다.

## 트랜잭션 AOP 적용 전체 흐름
1. 프록시 호출
2. 스프링 컨테이너를 통해 트랜잭션 매니저 획득
3. 트랜잭션 매니저를 통해 트랜잭션 획득 (`transactionManager.getTransaction()`)
4. 데이터소스 -> 커넥션 생성
5. 커넥션 오토커밋 false 설정
6. 트랜잭션 동기화 매니저에 커넥션 보관
7. 보관된 커넥션
8. 실제 서비스 호출
9. 트랜잭션 동기화 커넥션 획득