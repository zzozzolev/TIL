## fabric with background
```
# apt-get install dtach 필요

def runbg(cmd, sockname="dtach"):
    return run('dtach -n `mktemp -u /tmp/%s.XXXX` %s' % (sockname, cmd))
```

## What's the difference between IP address 0.0.0.0 and 127.0.0.1?
- https://serverfault.com/questions/78048/whats-the-difference-between-ip-address-0-0-0-0-and-127-0-0-1
- `0.0.0.0`에서 listen 하고 있다는 건 호스트에 있는 모든 인터페이스로 들어오는 요청을 듣겠다는 것임.

## cpu millicore란?
- https://www.quora.com/What-is-Millicores
> A millicore is a metric measurement that is used to measure CPU usage. It is a CPU core split into 1000 units (milli = 1000).
If you have 4 cores, then the CPU capacity of the node is 4000m.

## 다양한 데이터 접근 기술 조합
- `JdbcTemplate`이나 `MyBatis`같은 기술들은 SQL을 직접 작성해야하는 단점은 있지만 기술이 단순하기 때문에 SQL에 익숙한 개발자라면 금방 적응할 수 있다.
- JPA, 스프링 데이터 JPA, QueryDSL 같은 기술들은 개발 생산성을 혁신할 수 있지만 학습 곡선이 높기 때문에 감안해야한다.
- 추천 방향은 JPA, 스프링 데이터 JPA, QueryDSL을 기본으로 사용하고, 복잡한 쿼리를 써야하는데 해결이 잘 안 되면 `JdbcTemplate`이나 `MyBatis`를 함께 사용하는 것이다.
