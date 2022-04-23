## SSL - Server Name Indication
- 하나의 웹 서버에서 여러 개의 SSL 인증서를 로드해야하는 문제를 해결함.
- 초기 SSL 핸드 쉐이크에서 클라이언트가 타겟 서버의 호스트 네임을 명시할 것을 요구함.
- 서버는 올바른 인증서를 찾거나 기본적인 것을 리턴함.

## ASG
- 스케일링 폴리시는 CPU, 네트워크, 커스터 메트릭 혹은 스케줄이 될 수도 있음.
- ASG는 launch configurations 혹은 launch templates를 사용함.
- ASG를 업데이트하기 위해, 새로운 launch configurations 혹은 launch template이 필요함.
- ASG에 붙여진 IAM 롤들은 EC2 인스턴스들에 할당될 것임.
- ASG는 무료임. 런치되는 리소스들에 대한 비용만 지불하면 됨.
- ASG 아래 인스턴스를 갖는 것은 인스턴스가 멈췄을 때, ASG가 자동적으로 새로운 것을 만드는 것임.
- ASG는 LB에 의해 unhealthy 하다고 표시된 인스턴스를 멈출 수 있음.
