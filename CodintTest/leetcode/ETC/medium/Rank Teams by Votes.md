### 소모 시간
- 42분

### 통과율
- 22%

### 문제 분석
- 각 Char에 대해서 더 낮은 인덱스를 많이 가질수록 정렬 우선 순위를 갖게 하는 문제. -> 인덱스 카운트 + 정렬.
- 만약 동일하다면 다음 인덱스로 비교함.
- 모든 인덱스로 비교해도 동일하면 알파벳순으로 비교함.

### My Solution
```java
class Solution {
    public String rankTeams(String[] votes) {
        Map<Character, Integer> sum = new HashMap<>();

        for (int i = 0; i < votes.length; i++) {
            for (int j = 0; j < votes[i].length(); j++) {
                char c = votes[i].charAt(j);
                sum.put(c, sum.getOrDefault(c, 0) + j);
            }
        }

        StringBuilder sb = new StringBuilder();
        List<Map.Entry<Character, Integer>> entries = new LinkedList<>(sum.entrySet());
        entries.sort(Map.Entry.comparingByValue());
        for(Map.Entry<Character, Integer> entry: entries)
            sb.append(entry.getKey());
        return sb.toString();
    }
}
```
- 동일한 카운트를 제대로 처리하지 못함.

### Other Solution
- https://leetcode.com/problems/rank-teams-by-votes/solutions/524853/java-o-26n-26-2-log26-sort-by-high-rank-vote-to-low-rank-vote/
```java
class Solution {
    public String rankTeams(String[] votes) {
      Map<Character, int[]> map = new HashMap<>();
      int l = votes[0].length();
      // 각 char 별로 인덱스를 카운트한다.
      for(String vote : votes){
        for(int i = 0; i < l; i++){
          char c = vote.charAt(i);
          map.putIfAbsent(c, new int[l]); // 이런 식으로 없는 경우 새 인스턴스 생성 가능함.
          map.get(c)[i]++;
        }
      }
      
      List<Character> list = new ArrayList<>(map.keySet());
      // 별도의 정렬 함수 필요.
      Collections.sort(list, (a,b) -> { // list.sort도 가능함.
        // 낮은 인덱스부터 시작함. 왜냐하면 낮은 인덱스가 정렬 우선순위를 갖기 때문임.
        for(int i = 0; i < l; i++){
          if(map.get(a)[i] != map.get(b)[i]){
            // a, b를 인자로 할 때 내림차순으로 정렬하기 위해 b - a로 비교함.
            return map.get(b)[i] - map.get(a)[i];
          }
        }
        // 모두 동일하면 알파벳순으로 비교함. 이때는 내림차순으로 X
        return a - b;
      });
      
      StringBuilder sb = new StringBuilder();
      for(char c : list){
        sb.append(c);
      }
      return sb.toString();
    }
}
```
