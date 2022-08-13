### 소모 시간
- 29분 28초

### 통과율
- 100%

### my solution
```java
class Solution {
    public void merge(int[] nums1, int m, int[] nums2, int n) {
        // nums1 is empty;
        if (nums1.length == nums2.length) {
            for(int i = 0; i < nums1.length; i++)
                nums1[i] = nums2[i];
            return;
        }
        
        // nums2 is empty;
        if (nums2.length == 0) {
            return;
        }
        
        // Copy nums1 elems to a new array.
        int[] nums1Copied = Arrays.copyOf(nums1, nums1.length - nums2.length);
        
        // i = nums1 pointer, j = nums2 pointer.
        int i = 0;
        int j = 0;
        int k = 0;
        
        // Iterate before len(nums1).
        while (k < nums1.length) {
            if (nums1Copied[i] < nums2[j]) {
                nums1[k] = nums1Copied[i];
                i += 1;
            }
            else {
                nums1[k] = nums2[j];
                j += 1;
            }
            
            k += 1;
            
            if (i == nums1Copied.length || j == nums2.length)
                break;
        }
        
        if (i < nums1Copied.length) {
            while (i < nums1Copied.length) {
                nums1[k] = nums1Copied[i];
                k += 1;
                i += 1;
            }
        }
        
        if (j < nums2.length) {
            while (j < nums2.length) {
                nums1[k] = nums2[j];
                k += 1;
                j += 1;
            }
        }
        
    }
}
```

### other solution
- https://leetcode.com/problems/merge-sorted-array/discuss/29503/Beautiful-Python-Solution
```python
def merge(self, nums1, m, nums2, n):
        while m > 0 and n > 0:
            if nums1[m-1] >= nums2[n-1]:
                nums1[m+n-1] = nums1[m-1]
                m -= 1
            else:
                nums1[m+n-1] = nums2[n-1]
                n -= 1
        if n > 0:
            nums1[:n] = nums2[:n]
```
- 배열 복사가 필요 없다.
- `nums1`의 0이 아닌 유효값부터 시작한다.
- `nums1`을 모두 이터레이트 못했다면 원래 자리에 있는 것이다.
- `nums2`를 모두 이터레이트 못했다면 `nums1`보다 작은 수를 옮기지 못한 것이다.
