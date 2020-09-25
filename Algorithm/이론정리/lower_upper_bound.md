# binary search와 비교
- 공통점
    - 인덱스를 찾는다면 오름차순으로 정렬돼 있어야 한다. (특정 조건 만족이라서 인덱스가 필요없다면 정렬돼 있을 필요는 없다.)
    - 구간을 나눠서 찾는다는 것이다.
- 차이점은 찾고자 하는 대상이 정확히 일치하는 것이 아니다. 그리고 인덱스를 포함하는 방식이 다르다.

# lower bound
- 찾고자 하는 값 **이상**이 처음으로 나타나는 인덱스를 찾는다.
- 배열이 `a`이고 찾고자 하는 값이 `k`일 때, `a[mid] <= k`인 최소 `mid`를 찾으면 된다.
- `a[mid] == k`이어도 다음 탐색에 포함시킨다.
- implementation
    ```
    int lower_bound(int arr[], int target, int size)
    {
        int mid, start, end;
        start = 0, end = size-1;

        while (end > start) // end가 start보다 같거나 작아지면, 그 값이 Lower Bound이므로 반복을 종료한다.
        {
            mid = (start + end) / 2; 
            if (arr[mid] >= target) // 중간값이 원하는 값보다 크거나 같을 경우, 끝값을 중간값으로 설정하여 다시 탐색한다.
                end = mid;
            else start = mid + 1; // 중간값이 원하는 값보다 작을 경우, 시작값을 중간값+1로 설정하여 다시 탐색한다.
        }
        return end;
    }
    ```

# upper bound
- 찾고자 하는 값 **초과**가 처음으로 나타나는 인덱스를 찾는다.
- 배열이 `a`이고 찾고자 하는 값이 `k`일 때, `a[mid] > k`인 최소 `mid`를 찾으면 된다.
- `a[mid] == k`이면 다음 탐색에 포함시키지 않는다.
- implementation
    ```
    int upper_bound(int arr[], int target, int size)
    {
        int mid, start, end;
        start = 0, end = size-1;

        while (end > start) // end가 start보다 같거나 작아지면, 그 값이 Upper Bound이므로 반복을 종료한다.
        {
            mid = (start + end) / 2; 
            if (arr[mid] > target) // 중간값이 원하는 값보다 클 경우, 끝값을 중간값으로 설정하여 다시 탐색한다.
                end = mid;
            else start = mid + 1; // 중간값이 원하는 값보다 작거나 같을 경우, 시작값을 중간값+1로 설정하여 다시 탐색한다.
        }
        return end;
    }
    ```

# Reference
- https://12bme.tistory.com/120
- https://m.blog.naver.com/PostView.nhn?blogId=bestmaker0290&logNo=220820005454&proxyReferer=https:%2F%2Fwww.google.com%2F