## Lambda foundations
### Lambda programming model
- 함수의 클래스는 메모리에 남아있기 때문에 핸들러 메서드 밖에서 초기화된 건 계속 재사용될 수 있다.
- 그래서 처리 시간을 줄이기 위해 SDK 같은 재사용 가능한 리소스는 초기화할 때 만들어라.
- `/tmp` 디렉토리에 로컬 스토리지를 가질 수 있다. 디렉토리 내용은 execution environment이 멈출 때 남아있는다.
- 여러 호출에서 사용할 수 있는 임시 캐시로 사용할 수 있다.
- 별도로 명시되지 않는 한, 인커밍 리퀘스트는 순서가 바뀌거나 동시에 처리될 수 있다.
- 함수를 오래 걸리게 만들지 말고 애플리케이션 상태를 다른 곳에 저장하라.
- 퍼포먼스를 높이기 위해 로컬 스토리지나 클래스 레벨 오브젝트를 사용하지만 배포 패키지와 execution environment로 전달되는 데이터 양을 줄여라.

### Lambda execution environment
- 람다는 함수를 execition environment에서 호출한다.
- 함수의 런타임은 Runtime API를 사용해 람타와 통신한다.
- 런타임과 함수는 execution environment내에서 프로세스로 수행된다.
- execution enviroment의 lifecycle은 init -> invoke -> shutdown 순으로 진행된다.
- lambda는 요청을 받자마자 수행 가능한 게 아니고 먼저 init에서 runtime과 모든 extension들에서 준비를 마쳐야한다.
- init 시간이 길어지면 cold start가 발생할 수 있다.
- 만약 lambda 함수가 invoke 동안 망가지거나 타임아웃이 발생하면 lambda는 executuin enviroment를 리셋한다. (like shutdown)
- 해당 environment가 새로운 invocation에 쓰이면 lambda는 re-init을 한다. (called suppressed init)
- CloudWatch Logs에서 명시적으로 re-init을 리포트하지 않는다.
- shutdown 이후에도 handler 메서드 밖에 선언된 객체는 초기화된 상태로 남아있는다.
- 함수 코드를 짤 때, lambda가 알아서 뒤이은 함수 invoke에서 execution environment를 재사용할 거라고 가정하면 안 된다.

## Lambda function scaling
- 초기화된 execution environment가 다음 호출에 바로 사용되면 init 없이 바로 사용될 수 있다.
- 만약 요청을 처리할 execution environment가 없으면 새로운 execution environment를 사용한다.
- concurrency는 rps랑 다르다.
- concurrency는 다음과 같이 계산할 수 있다.
  ```
  Concurrency = (average requests per second) * (average request duration in seconds)
  ```

### Reserved concurrency
- 함수에서 특정 만큼의 concurrency를 보장하고 싶을 때 사용하면 된다.
- 함수에서 최대로 수행 가능한 concurrency이다.
- 대신 reserved concurrency를 설정하면 unreserved concurrency pool을 사용할 수 없다.

### Provisioned concurrency
- pre-initialized execution environment의 개수이다.
- init이 이미 끝난 lambda를 바로 사용할 수 있기 때문에 cold start를 겪을 가능성이 줄어든다.
- reserved concurrency랑 다른 거니 헷갈리지 말자.

### Burst concurrency
- lambda가 즉시 concurrency를 늘릴 수 있는 정도이다.
- 리전마다 최대 quota가 다르다. (seoul은 500)
- 리퀘스트에 대해서 available burst quota만큼 급증시킬 수 있다.
- burst quota는 1분 후 500씩 다시 찬다. 그래서 다음 burst에서 사용할 수 있다.
- 현재 active execution environments에서 burst quota만큼 계속 축적해서 maximum scaling capacity를 늘릴 수 있다.
