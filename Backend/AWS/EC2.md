## Placement Groups
### Cluster
- 같은 rack, 같은 AZ
- 장점: 낮은 latency
- 단점: rack이 망가지면 모든 인스턴스들이 동시에 망가짐.
- 사용 예시: 빅 데이터 job, 네트워크 성능이 중요한 애플리케이션

### Spread
- 서로 다른 hw, 서로 다른 AZ에 걸쳐서 퍼뜨려놓음.
- 장점: 동시에 실패함 위험성을 줄임.
- 단점: AZ당 7개의 인스턴스로 제한됨.
- 사용 예시: HA가 중요한 애플리케이션.

### Partition
- 일부는 같은 rack을 사용하지만 여러 개의 rack을 사용하고 서로 다른 AZ에 걸쳐놓음.
- 100개의 EC2 인스턴스까지 가능함.
- 장점: 파티션이 실패하면 많은 EC2에 영향이 가지만 다른 파티션들에 영향을 주지 않음.
- 단점: AZ당 7개의 파티션만 가능함.
- 사용 예시: HDFS, HBase, Cassandra, Kafka