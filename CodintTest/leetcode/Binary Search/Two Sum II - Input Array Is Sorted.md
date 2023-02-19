### 소모 시간
- 17분

### 통과율
- 36%

### 문제 분석
- binary search 문제라고 나와있기는 하지만 binary search로 풀면 인덱스를 하나씩 봐야함. 그래서 요상하게 풀어야함.
- two pointer로 푸는 게 제일 깔끔함. 엘리먼트 개수도 3 * 10^4 이면 감당 안 될 정도도 아님.

### My Solution
```java
class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            int mid = left + (right - left) / 2;

            if (sum < target) {
                left = mid + 1;
            }
            else if (sum > target) {
                right = mid;
            }
            else
                break;
        }

        return new int[]{left + 1, right + 1};
    }
}
```

### Other Solution
- https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/solutions/51239/share-my-java-ac-solution/
```java
public int[] twoSum(int[] num, int target) {
    int[] indice = new int[2];
    if (num == null || num.length < 2) return indice;
    int left = 0, right = num.length - 1;
    while (left < right) {
        int v = num[left] + num[right];
        if (v == target) {
            indice[0] = left + 1;
            indice[1] = right + 1;
            break;
        } else if (v > target) {
            right --;
        } else {
            left ++;
        }
    }
    return indice;
}
```
