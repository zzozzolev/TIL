## 왜 쓸까?
- 데이터 파이프라인을 관리할 수 있다.
- 태스크들을 신뢰할 수 있는 방법으로 실행할 수 있다.

## 무엇일까?
- 태스크들을 올바른 시간에, 올바른 방법으로, 올바른 순서로 실행할 수 있게 해주는 오케스트레이터.

### 이점
- dynamic: 파이썬으로 데이터 파이프라인을 구축 가능하다.
- scaleability: 병렬적으로 원하는 만큼의 태스크를 수행할 수 있다.
- UI: UI를 통해 모니터링, 재실행등 편리하게 할 수 있다.
- extensibility: 필요한 게 있다면 airflow 업그레이드와 상관없이 플러그인을 만들어서 앱에 추가할 수 있다.

### 핵심 컴포넌트들
- web server: UI를 서빙하는 Gunicorn으로 이루어진 플라스크 서버.
- scheduler: 워크플로우들을 스케줄링하는 것을 책임지는 데몬. 에어플로우의 심장.
- metastore: 메타데이터가 저장되는 DB.
- executor: 어떻게 태스크들이 수행돼야할지 정의하는 클래스.
- worker: 태스크를 수행하는 프로세스와 서브 프로세스.

### DAG
- loop가 없고 방향성이 있는 그래프

### Operator
- 태스크에 대한 wrapper
- 종류
  - Action Operators: 함수나 커맨드를 수행하는 오퍼레이터
  - Transfer Operators: 소스와 데스티네이션 간에 데이터를 옮기는 오퍼레이터
  - Sensor Operators: 다음 태스크로 넘어가기 전에 뭔가가 일어나기 기다리는 오퍼레이터

### Task / Task Instance
- 오퍼레이터를 수행하면 오퍼레이터는 태스크 인스턴스가 된다.

### Workflow
- 오퍼레이터, 태스크, 디펜던시를 가지는 DAG.

### airflow가 아닌 것
- 데이터 스트리밍 솔루션이나 데이터 프로세싱 프레임워크가 아니다.
- 에어플로우 내에서 TB 단위의 데이터를 처리하지 마라.

## airflow 동작 방식
### One Node Architecture
- 노드 하나에 웹 서버, 스케줄러, 메타 스토어, 익스큐터(큐)가 있다.
- 웹 서버는 메타스토어에서 메타 데이터를 페치한다.
- 스케줄러는 메타스토어와 익스큐터에 태스크를 수행하기 위해 요청을 보낼 수 있다.
- 익스큐터는 메타스토어에 태스크들의 상태를 업데이트할 것이다.
- 큐는 익스큐터의 일부분이다.
- 작은 규모에서는 싱글 노드로 해도 괜찮다.

### Multi Nodes Architecture (Celery)
- 노드 하나에 웹 서버, 스케줄러, 익스큐더가 있고 다른 노드에 메타스토어와 큐가 있다.
- 주의할 점은 큐가 익스큐터 밖에 있다는 것이다.
- 태스크를 수행할 워커 노드들도 가진다.
- 워커 노드들은 태스크들을 나눠서 수행한다.
- 웹 서버는 메타스토어에서 메타 데이터를 가져온다.
- 스케줄러는 태스크를 스케줄하기 위해 메타스토어와 익스큐터에 말을 건다.
- 익스큐터는 큐에 태스크를 푸쉬한다.
- 태스크들이 큐에 있다면, 워커들은 태스크들을 가져와서 자신의 머신에서 수행한다.

### 동작 방식
- 싱글 노드 아키텍처 기준으로 설명한다.
- 데이터 파이프라인을 넣는 folder dags가 있다.
1. 새로운 DAG 파이썬 파일을 여기에 넣으면 웹 서버와 스케줄러가 새로운 데이터 파이프라인을 알기 위해 파싱을 한다.
2. 파싱이 끝나면 스케줄러는 `DagRun` 오브젝트(DAG의 인스턴스)를 만든다.
3. 메타스토어에서 `DagRun` 오브젝트는 running으로 표시된다.
4. 데이터 파이프라인에서 수행될 첫번째 태스크는 스케줄된다.
5. 태스크 인스턴스 오브젝트가 생성된다면 스케줄러에의해 익스큐터에 보내진다.
6. 익스큐터는 태스크를 수행하고 태스크의 상태를 메타스토어에 업데이트한다.
7. 스케줄러는 태스크가 끝났는지 체크한다.
8. 웹서버는 UI에 태스크의 상태를 업데이트한다.

## CLI
- `airflow db init`: 처음 메타스토어를 초기화할 때 필요하고 이후에는 하면 안 된다.
- `airflow db reset`: 메타스토어 내용을 모두 비우는 것이므로 프로덕션에서는 추천하지 않는다.
- `airflow scheduler`: 스케줄러를 실행한다.
- `airflow dags list`: dag들을 볼 수 있다.
- `airflow tasks list {dag name}`: dag와 관련된 태스크들을 볼 수 있다. 만약 태스크가 뜨지 않았다면 파싱 에러가 발생한 것이다.
- `airflow dags trigger`: 데이터 파이프라인을 실행할 수 있게 해준다.

## DAG가 뭘까?
- 데이터 파이프라인
- Directed Acyclic Graph
- 루프가 없고 노드가 태스크이고 엣지가 디펜던시인 그래프

## Operator가 뭘까?
- 데이터 파이프라인에 하나의 태스크를 정의하는 것이다.
- **One operator One task**
- 이렇게 하는 이유는 오퍼레이터 하나에 여러 태스크를 넣으면, 특정 태스크는 성공하고 이후 태스크가 실패하더라도 전체 태스크를 다시 해야하기 때문이다.
- 3가지 종류의 오퍼레이터가 있다.
  - Action Operator: 액션을 수행한다.
  - Transfer Operator: 출발지에서 도착지까지 데이터를 트랜스퍼한다.
  - Sensors: 컨티션이 만족되길 기다린다.

## DAG scheduling
- 두 가지 argument들은 항상 정의해야한다.
  - start_date: 언제 DAG가 스케줄 되기 시작할 건지
  - schedule_interval: 데이터 파이프라인이 트리거되는 빈도를 정의함.
- **start_date + schedule_interval이 지나야 실제로 트리거된다.**
  - 예를 들어, start_date가 2020/01/01 10AM 이고 schedule_interval이 10mins이면 2020/01/01 10:10AM에 트리거된다.
- 문제
  ```
  Let's assume a DAG start_date to the 28/10/2021:10:00:00 PM UTC and the DAG is turned on at 10:30:00 PM UTC with a schedule_interval of */10 * * * * (After every 10 minutes). How many DagRuns are going to be executed?
  
  2.
  You right! The first one is executed at 10:10 for the execution_date 10:00, then 10:20 for the execution_date 10:20. DAG Run 3 is not yet executed since a DAG Run runs once the schedule_interval (10 minutes here) is passed.
  ```

## Backfilling and catchup
- start date 이후 특정 시점에 DAG 실행을 멈췄다가 다시 수행하면 이전에 트리거 되지 않았던 DAG들도 모두 수행된다. 이걸 `catchup`이라고 한다.
  - 예를 들면 01/01, 02/01, 03/01, 04/01 DAG 들이 있었고 02/01 멈췄다가 05/01에 다시 트리거한다고 해보자.
  - 그러면, 02/01, 03/01, 04/01 DAG들도 다시 수행된다.
- airflow는 기본적으로 catchup을 한다. `catchup=True` 파라미터에 의해 이렇게 동작한다.
- `catchup`을 `True`로 설정하면 트리거 되지 않았던 DAG run들은 최신 실행 시간부터 자동적으로 트리거 된다. start data부터 시작되지 않는다.
- 단, DAG를 한 번도 수행하지 않았다면 start date부터 시작된다.
- 모든 date는 UTC이다.

## Start scaling with the Local Executor
- 기본적으로는 태스크가 하나하나 수행되도록 설정돼있다.
- 기본적으로 두 개의 파라미터가 익스큐터를 설정하기 위해 사용된다.
  - (sqlite 사용) `sql_alchemy_conn` `airflow config get-value core sql_alchemy_conn`
  - `executor`: `SequentialExecutor` `airflow config get-value core executor`
- 따라서 이 두 가지를 바꿔야 parallel 하게 수행된다.
  - sqlite가 아닌 다른 DB 사용.
  - `LocalExecutor` 사용: 같은 머신내에서 여러 개의 태스크들을 병렬적으로 수행할 수 있게 해준다.
- LocalExecutor
  - 태스크를 가질 때마다, 태스크는 서브 프로세스가 된다. 해당 서브 프로세스에서 태스크가 수행된다.

## Airflow at Scale
- 로컬 익스큐터만으로는 한계가 있다. 원하는 만큼 태스크를 수행하기 위해서는 다른 익스큐터를 찾아야한다.
- 선택은 샐러리 익스큐터와 쿠버네티스 익스큐터이다. (강의에서는 샐러리 익스큐터 선택)
- 에어플로우 내에서 태스크가 수행될 때마다 먼저 큐에 추가된다.
- 태스크를 수행할 때 큐에서 가져와서 수행된다.
- 태스크들은 워커들에서 수행된다.
- 더 많은 워커가 있을 수록, 더 많은 태스크들이 실행될 수 있다.
- 분산된 환경에서는 큐가 웹 서버에 있는 게 아니라 별도로 존재한다. 레디스 같은 인메모리 DB를 쓸 수 있다.

### How it works
1. 스케줄러에 트리거 될 준비가 완료된 태스크가 있다.
2. 레디스에 푸쉬된다.
3. 워커 중 하나가 레디스로부터 태스크를 빼간다.
- `worker_concurrency` 파라미터는 워커 내에서 최대로 실행할 수 있는 태스크의 개수를 정의한다.
