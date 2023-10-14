### 소모 시간
- sorting: 10분 11초
- sorting 안하고 bucket sort 비스무리하게: 11분 23초

### 통과율
- 100%

### my solution
- sorting
```python
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counter = defaultdict(int)
        for num in nums:
            counter[num] += 1
        
        sorted_pairs = sorted([(k, v) for k, v in counter.items()], key = lambda x: x[1], reverse=True)
        
        return [k for k, v in sorted_pairs[:k]]
```
- sorting 안하고 bucket sort 비스무리하게
```python
from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count_matrix = [[] for _ in range(len(nums) + 1)]
        
        counter = defaultdict(int)
        for num in nums:
            counter[num] += 1
        
        for num in counter:
            count_matrix[counter[num]].append(num)
        
        result = []
        for group in count_matrix[::-1]:
            while len(result) < k and len(group) != 0:
                result.append(group.pop())
        
        return result
```

### other solution
- https://leetcode.com/problems/top-k-frequent-elements/solutions/81602/java-o-n-solution-bucket-sort/
```java
public List<Integer> topKFrequent(int[] nums, int k) {

	List<Integer>[] bucket = new List[nums.length + 1];
	Map<Integer, Integer> frequencyMap = new HashMap<Integer, Integer>();

	for (int n : nums) {
		frequencyMap.put(n, frequencyMap.getOrDefault(n, 0) + 1);
	}

	for (int key : frequencyMap.keySet()) {
		int frequency = frequencyMap.get(key);
		if (bucket[frequency] == null) {
			bucket[frequency] = new ArrayList<>();
		}
		bucket[frequency].add(key);
	}

	List<Integer> res = new ArrayList<>();

	for (int pos = bucket.length - 1; pos >= 0 && res.size() < k; pos--) {
		if (bucket[pos] != null) {
			res.addAll(bucket[pos]);
		}
	}
	return res;
}
```
