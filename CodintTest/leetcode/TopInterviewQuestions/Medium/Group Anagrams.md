### 소모 시간
- 20분

### 통과 여부
- 100%

### 문제점
- 제네릭에 대한 이해가 부족한 것 같다. 

### 배운점
- 타입은 추상 타입으로 명시하고 인스턴스 타입은 구체 타입으로 작성한다. 이때 인스턴스 타입은 가장 상위 타입만 작성하면 된다.
  ```java
  List<List<String>> answer = new ArrayList<List<String>>(); (x)
  List<List<String>> answer = new ArrayList<>(); (o)
  ```

### my solution
```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        if (strs.length == 0)
            return new ArrayList<List<String>>();
    
        Map<String, List<String>> map = new HashMap<>();
        
        for (String str : strs) {
            char[] tmp = str.toCharArray();
            Arrays.sort(tmp);
            String key = new String(tmp);
            
            if (!map.containsKey(key)) {
                map.put(key, new ArrayList<String>());
            }
            
            map.get(key).add(str);
        }
        
        List<List<String>> answer = new ArrayList<List<String>>();
        for (List<String> value: map.values()) {
            answer.add(value);
        }
        
        return answer;
    }
}
```

---

### 소모 시간
- 6분

### 통과 여부
- 100%

### 접근법
- 딕셔너리의 key를 `str`로 value를 `list`로 한다.
- 리스트로 바꾼 단어를 정렬하고 빈 문자열로 `join`을 한 것을 key로 하고 해당 단어를 list에 append한다.
- 딕셔너리의 values를 리턴한다.

### 문제점
- `tuple`을 key로 사용하면 굳이 `join`을 안 써도 된다.

### my solution
```
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        
        for word in strs:
            groups["".join(sorted(list(word)))].append(word)
        
        return groups.values()
```
