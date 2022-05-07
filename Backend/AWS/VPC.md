## Default VPC
- 모든 새로운 AWS 계정들은 디폴트 VPC를 가진다.
- 새로운 EC2 인스턴스들은 서브셋이 특정되지 않으면 디폴트 VPC에 런치된다.
- 디폴트 VPC는 인터넷 연결성을 가지고 내부에 있는 모든 EC2 인스턴스들은 퍼블릭 IPv4 주소들을 가진다.
- 퍼블릭과 프라이빗 IPv4 DNS 이름들을 가진다.

## VPC in AWS - IPv4
- VPC = Virtual Private Cloud
- AWS 리전에 여러 개의 VPC들을 가질 수 있다. (최대 리전당 5개)
- VPC당 최대 CIDR는 5개. 각각의 CIDR 당
  - 최소 사이즈는 `/28` (16개의 IP 주소)
  - 최대 사이즈는 `/16` (65536개의 IP 주소)
- VPC CIDR는 다른 네트워크들과 중복되면 안 된다.
- AWS는 5개의 IP 주소들을 각각의 서브넷에서 예약해놨다.
- 이 다섯 개의 주소들은 사용할 수 없고 EC2 인스턴스에 할당될 수 없다.
- 만약, CIDR 블록이 `10.0.0.0/24`라면 예약된 IP 주소들은 다음과 같다.
  - `10.0.0.0`: 네트워크 어드레스
  - `10.0.0.1`: VPC 라우터
  - `10.0.0.2`: Amazon-provided DNS에 대한 맵핑
  - `10.0.0.3`: 미래 사용 용도
  - `10.0.0.255`: 네트워크 브로드 캐스트 주소. AWS는 VPC에서 브로드 캐스트를 지원하지 않으므로 해당 주소가 예약돼있다.

## IGW
- VPC에 있는 리소스들이 인터넷에 연결될 수 있도록 해준다.
- 수평적으로 확대, HA, 리던던트하다.
- VPC마다 별도로 생성돼야한다.
- 하나의 VPC는 하나의 IGW에만 어테치될 수 있고 반대도 마찬가지이다.
- IGW 자체는 인터넷 액세스를 허용하지 않는다.
- 라우트 테이블들이 수정돼야한다.
- IGW를 서브넷에 어테치하고 이를 위한 별도의 라우트 테이블을 설정해야한다.
- 라우트 테이블에 VPC 범위에 들어오지 않는 IP는 IGW로 보내야한다.

## NAT Gateway
- AWS-managed NAT
- 특징
  - 더 높은 bandwidth
  - 고가용성
  - 관리 필요없음
- 사용량과 bandwidth에 대해 시간당 지불해야한다.
- NATGW는 특정한 AZ에 생성되고 엘라스틱 IP를 사용한다.
- 같은 서브넷에 있는 EC2 인스턴스에 의해 사용될 수 없다. (다른 서브넷에 있는 것만)
- IGW를 필요로 한다. (private subnet -> NATGW -> IGW)
- 5 Gbps의 bandwidth를 가지고 45 Gbps까지 오토 스케일링이 가능하다.
- 관리할 SG를 필요로 하지 않는다.

### NAT Gateway with High Availability
- NAT 게이트웨이는 하나의 AZ 내에서는 회복탄력성이 있다. (resilient)
- fault-tolerance를 위해서는 여러 개의 AZ들에 여러 개의 NAT 게이트웨이들을 만들어야한다.
- 단 cross-AZ failover는 필요하지 않다.
- 왜냐하면 AZ가 내려갔다면 NAT가 필요하지 않기 때문이다.

## NACL & Security Group
### 비교
- NACL(Network Access Control List)은 **stateless**이기 때문에 인바운드 룰이 허용됐다고 해서 아웃바운드도 허용되는 것은 아니다.
- SG는 **stateful**이기 때문에 인바운드가 허용된다면 아웃바운드도 허용된다.
- 그래서 인바운드 리퀘스트가 NACL, SG의 인바운드 룰에서 허용됐다고 해도 NACL의 아웃바운드 룰이 허용하지 않는다면 클라이언트한테 응답이 나갈 수 없다.

#### SG
- 인스턴스 레벨에서 동작한다.
- allow 룰만 지언한다.
- stateful: 룰과 상관없이, 결과 트래픽은 자동적으로 허용된다.
- 모든 룰들은 트래픽을 허용할 건지 결정하기 전에 평가된다.
- 누군가 정의했을 때 EC2 인스턴스에 적용된다.

#### NACL
- 서브넷 레벨에서 동작한다.
- allow 룰과 deny 룰을 지원한다.
- stateless: 리턴 트래픽은 룰에 의해서 명시적으로 허용돼야한다.
- 룰들이 순서에 맞춰서 평가된다. (낮은 번호부터 높은 번호까지) 처음 매칭된게 적용된다.
- 관련된 서브넷의 모든 EC2 인스턴스들에 적용된다.

### NACL
- 서브넷 간의 트래픽을 컨트롤하는 방화벽같은 것이다.
- 서브넷당 하나의 NACL을 가지고 새로운 서브넷들은 디폴트 NACL로 할당된다.
- NACL 룰 정의
  - 룰들은 1 ~ 32766의 number를 가진다.
  - 작은 숫자일수록 더 높은 우선 순위를 가진다.
  - 처음 매칭된 룰이 결정을 한다. 예를 들면 같은 CIDR에 대해 낮은 번호에서 허용하고 높은 번호에서 거부한다면 허용된다.
  - AWS는 룰을 추가할 때 100씩 증가시키는 걸 권장한다.
- 새롭게 만들어진 NACL들은 모든 것을 거부할 것이다.
- NACL은 서브넷 레벨에서 특정한 IP 주소를 블록킹하는 중요한 수단이다.

### Default NACL
- 모든 인바운드/아웃바운드를 허용한다.
- 강의 추천은 디폴트 NACL을 변경하지 않고 대신 커스텀 NACL을 만드는 것이다.

### Ephemeral(임시) Ports
- 두 개의 앤드포인트가 커넥션을 맺기 위해서는 포트를 사용해야한다.
- 클라이언트는 정의된 포트로 연결하고 임시 포트에서 응답을 기대한다.
- OS 종류마다 다른 포트 레인지를 가진다.
  - 리눅스 커널: 32768 ~ 60999

> ephemeral port: TCP 연결을 맺을때, 클라이언트 소켓은 하나의 포트를 선점해야 합니다. TCP 연결은 출발지(source) 주소, 출발지 포트, 목적지(destination) 주소, 목적지 포트를 그 구분자로 하기 있기 때문입니다. 클라이언트에서 서버로 연결을 맺을때, 특별히 bind() 시스템 콜로 출발지 포트를 지정(bind)하지 않는다면, 커널은 임의의 포트를 할당합니다. 그리고 이러한 포트를 ephemeral port라고 통칭합니다. 출처: https://meetup.toast.com/posts/54

### NACL with Ephemeral Ports
- 웹 서브넷과 DB 서브넷이 분리돼있고 각각의 NACL를 갖고 DB는 3306에 포트를 열어뒀다고 해보자.
- 웹 NACL은 DB 서브넷 CIDR로 가는 아웃바운드 TCP 포트 3306에 대해서 허용해야한다.
- DB NACL은 웹 서브넷 CIDR에서 들어오는 인바운드에 TCP 포트 3306 대해서 허용해야한다.
- 하지만 이때 클라이언트가 ephemeral port를 사용하기 때문에 문제가 발생한다.
- 그래서 특정 포트가 아닌 range로 각각의 NACL에 설정을 하면 된다.

## VPC Reachability Analyzer
- VPC내의 두 앤드포인트 사이의 네트워크 연결성을 트러블 슈팅하는 네트워크 진단 툴
- 네트워크 설정에 대한 모델을 만들고 설정에 기반해 reachability를 체크한다.
- 패킷을 보내지 않는다.