### 소모 시간
- 40분

### 통과율
- 100%

### my solution
```java
class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        // (gas, index)에서 gas 내림차순으로 정렬
        List<List<Integer>> gasIndexPairs = new ArrayList<>();
        for (int i = 0; i < gas.length; ++i)
            gasIndexPairs.add(new ArrayList<>(Arrays.asList(gas[i], i)));
        
        gasIndexPairs.sort((a, b) -> b.get(0).compareTo(a.get(0)));
        
        // 리스트 순화하면서 조건에 맞는 곳 발견
        for (List<Integer> list : gasIndexPairs) {
            int index = list.get(1);
            
            // 시작 지점으로 초기화
            int tank = gas[index] - cost[index];
            
            // 다음 지점으로 갈 수 없음
            if (tank < 0)
                continue;
            
            int cur = index + 1;
            // 마지막 인덱스인 경우
            if (index == gas.length - 1)
                cur = 0;
            boolean fail = false;
            while (cur != index) {
                tank += gas[cur] - cost[cur];
                if (tank < 0) {
                    fail = true;
                    break;
                }
                if (cur == gas.length - 1)
                    cur = 0;
                else
                    cur += 1;
            }
            
            if (!fail) {
                return index;
            }
            
        }
        
        return -1;
    }
}
```

### other solution
- https://leetcode.com/problems/gas-station/discuss/1706142/JavaC%2B%2BPython-An-explanation-that-ever-EXISTS-till-now!!!!
```java
class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        int n = gas.length;
        int total_surplus = 0;
        int surplus = 0;
        int start = 0;
        
        for(int i = 0; i < n; i++){
            total_surplus += gas[i] - cost[i];
            surplus += gas[i] - cost[i];
            if(surplus < 0){
                surplus = 0;
                start = i + 1;
            }
        }
        return (total_surplus < 0) ? -1 : start;
    }
}
```
- 어디서 시작하든 어차피 한 번 다 순회해야한다. 따라서 전체 값을 더하고 뺀 게 0보다 작다면 어디든 없는 거다.
- 정답은 유일하다. 현재 위치에서 시작했을 때 전체 값이 0보다 크다면 무조건 정답니다.

---
### 소모 시간
- 40분

### 통과율
- 97%

### 접근법
- (gas, cost)를 (desc, asc)로 정렬시키고 앞에서부터 시작점으로 정한다. 즉, gas가 많으면서 cost가 적은 것부터 시작하는 것이다.
- 시작점을 제일 처음으로 하고 원래의 처음부터 시작점 이전을 시작점 다음으로 바꿔준다. 예를 들면 시작점을 i라고 하면 `ls[i:] + ls[:i]` 이렇게 바꿔준다.
- 최종으로 얻는 gas가 0보다 크거나 같다면 해당 인덱스를 정답으로 반환한다.

### 문제점
- Time Limit Exceeded에 걸렸다. 이거 빼고 나머지는 통과했다. 로직 자체는 맞은 것 같다.
- 잘 안 되서 자세히 보니까 `reorder` 변수를 정의해놓고 안 쓰고 있었다..

### my solution
```
from collections import deque

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        pairs = list( sorted([ (g, c, i) for i, (g, c) in enumerate(zip(gas, cost)) ], 
                                key = lambda x: (-x[0], x[1])) )
        queue = deque(pairs)
        cur_gas = -1
        
        while cur_gas < 0 and len(queue) > 0:
            s_g, s_c, s_i = queue.popleft()
            reorder_gas = gas[s_i:] + gas[:s_i]
            reorder_cost = cost[s_i:] + cost[:s_i]
            
            cur_gas = s_g
            
            for i in range(len(gas)):
                if cur_gas < reorder_cost[i]:
                    cur_gas = -1
                    break
                    
                # last
                if i == len(gas) - 1:
                    cur_gas -= reorder_cost[i]
                else:
                    cur_gas = cur_gas - reorder_cost[i] + reorder_gas[i+1]
                
            
        if cur_gas >= 0:
            return s_i
        else:
            return -1
```

### other solution
- 출처: https://leetcode.com/problems/gas-station/discuss/42568/Share-some-of-my-ideas.
```
class Solution {
    public int canCompleteCircuit(int[] gas, int[] cost) {
        //determine if we have a solution
        int total = 0;
        for (int i = 0; i < gas.length; i++) {
            total += gas[i] - cost[i];
        }
        if (total < 0) {
            return -1;
        }
   
        // find out where to start
        int tank = 0;
        int start = 0;
        for (int i = 0; i < gas.length;i++) {
            tank += gas[i] - cost[i];
            if (tank < 0) {
                start = i + 1;
                tank = 0;
            }
        }
        return start;
    }
}
```
- If car starts at A and can not reach B. Any station between A and B
can not reach B.(B is the first station that A can not reach.)
- If the total number of gas is bigger than the total number of cost. There must be a solution.