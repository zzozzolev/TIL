### 소모 시간
- 19분 28초

### 통과율
- 100%

### My Solution
```java
class Solution {
    public int[] intersect(int[] nums1, int[] nums2) {
        Map<Integer, Integer> counter1 = getCounter(nums1);
        Map<Integer, Integer> counter2 = getCounter(nums2);

        List<Integer> answer = new ArrayList<>();
        for (Integer key : counter1.keySet()) {
            if (counter2.containsKey(key)) {
                int minCount = Math.min(counter1.get(key), counter2.get(key));
                for (int i = 0; i < minCount; i++) {
                   answer.add(key);
                }
            }
        }
        return answer.stream().mapToInt(Integer::intValue).toArray();
    }

    public Map<Integer, Integer> getCounter(int[] nums) {
        Map<Integer, Integer> counter = new HashMap<>();
        for (int num : nums) {
            counter.put(num, counter.getOrDefault(num , 0) + 1);
        }
        return counter;
    }
}
```

### Other Solution
- https://leetcode.com/problems/intersection-of-two-arrays-ii/solutions/1468295/python-2-approaches-3-follow-up-questions-clean-concise/?orderBy=most_votes
```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        if len(nums1) > len(nums2): return self.intersect(nums2, nums1)
            
        cnt = Counter(nums1)
        ans = []
        for x in nums2:
            if cnt[x] > 0:
                ans.append(x)
                cnt[x] -= 1
        return ans
```
- `nums1`이 더 적다면 `Counter`에 더 적은 원소 저장 가능.

```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1.sort()
        nums2.sort()
        
        ans = []
        i = j = 0
        while i < len(nums1) and j < len(nums2):
            if nums1[i] < nums2[j]:
                i += 1
            elif nums1[i] > nums2[j]:
                j += 1
            else:
                ans.append(nums1[i])
                i += 1
                j += 1
        return ans
``` 
- 같은 원소일 때 추가하고 다르다면 더 작은 수 가진 인덱스를 앞으로 한 칸 이동.
