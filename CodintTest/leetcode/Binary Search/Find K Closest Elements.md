### 소모 시간
- 44분

### 통과율
- 15%

### 문제 분석
- 슬라이딩 윈도우를 움직이는 것으로 생각해야됨.
- 절대값을 사용하면 안 됨.

### My Solution
```java
class Solution {
    public List<Integer> findClosestElements(int[] arr, int k, int x) {
        int low = 0, high = arr.length - 1, mid = (high + low) / 2;

        // Find min abs value
        while (low < high) {
            mid = (high + low) / 2;
            int leftAbs = (mid != 0) ? Math.abs(arr[mid - 1] - x) : -1;
            int rightAbs = (mid != arr.length - 1) ? Math.abs(arr[mid + 1] - x) : -1;

            // mid is min.
            if (Math.abs(arr[mid] - x) == 0)
                break;
            // left side is min.
            else if (leftAbs != -1 && leftAbs < rightAbs)
                high = mid - 1;
            // right side is min.
            else if (rightAbs != -1 && rightAbs < leftAbs)
                low = mid + 1;
            else
                break;
        }
        
        // Find k closest elem by mid.
        List<Integer> answer = new ArrayList<>();
        int idx = mid;
        int left = mid - 1, right = mid + 1;
        
        while (answer.size() != k) {
            answer.add(arr[idx]);

            if (left == -1 || Math.abs(arr[idx] - arr[left]) > Math.abs(arr[idx] - arr[right])) {
                idx = right;
                right++;
            }
            else if (right == arr.length || Math.abs(arr[idx] - arr[left]) <= Math.abs(arr[idx] - arr[right])) {
                idx = left;
                left--;
            }
        }

        answer.sort(Comparator.naturalOrder());
        return answer;
    }
}
```