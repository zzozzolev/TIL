### 소모 시간
- 33분 3초

### 통과율
- 99%

### 문제점
- 긴 인풋에 대해서 시간초과가 나왔다. `O(n)`이 아니고 `O(n^2)`에 가까워서 그런 것 같다.
- 정렬 없이 지금까지의 min과 비교하면 복잡하게 할 필요가 없다. 쓸데없이 복잡하다.

### my solution
```
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) == 0:
            return 0
        
        min_p_to_i, max_p_to_i = {}, {}
        for i, p in enumerate(prices):
            if p not in min_p_to_i:
                min_p_to_i[p] = i
            max_p_to_i[p] = i
        
        prices.sort()
        
        max_profit = 0
        left, right = 0, len(prices)-1
        while left < right:
            min_price = prices[left]
            max_price = prices[right]
            
            if min_p_to_i[min_price] < max_p_to_i[max_price] \
                and max_price - min_price > max_profit:
                max_profit = max_price - min_price
            
            right -= 1
            if right == left:
                left += 1
                right = len(prices)-1
        
        return max_profit
```

### other solution
- https://leetcode.com/problems/best-time-to-buy-and-sell-stock/discuss/39049/Easy-O(n)-Python-solution
```
def maxProfit(prices):
    max_profit, min_price = 0, float('inf')
    for price in prices:
        min_price = min(min_price, price)
        profit = price - min_price
        max_profit = max(max_profit, profit)
    return max_profit
```