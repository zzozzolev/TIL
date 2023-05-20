## Lambda foundations
### Lambda programming model
- 함수의 클래스는 메모리에 남아있기 때문에 핸들러 메서드 밖에서 초기화된 건 계속 재사용될 수 있다.
- 그래서 처리 시간을 줄이기 위해 SDK 같은 재사용 가능한 리소스는 초기화할 때 만들어라.