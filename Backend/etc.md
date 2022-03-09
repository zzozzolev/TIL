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