### 소모 시간
- 25분 52초

### 통과율
- 36%

### 문제점
- 별로 안 어렵다고 생각했는데 개박살났다...
- 오름차순일때만 길이가 짝수냐 홀수냐에 따라 이긴 사람을 정했는데 오름차순일때만 아니라 맥시멈을 카운트해서 짝수냐 홀수냐로 이긴 사람을 정하는 거였다.
- 결국 모든 엘리먼트가 사라지면 다음 사람이 지는 거니까 0번째가 몇번째로 지워지는지 카운트를 하면 된다.

### my solution
```
def gamingArray(arr):
    targets = list(sorted( [(v, i) for i, v in enumerate(arr)] ))
    
    # 오름차순일때는 길이로 바로 알 수 있음
    if arr == [v for v, i in targets]:
        if len(arr) % 2 != 0:
            return "BOB"
        else:
            return "ANDY"

    player = "BOB"
    while sum(arr) != 0:
        _, index = targets.pop()
        arr[index:] = [0] * (len(arr) - index)
        player = who_next(player)

    return who_next(player)

def who_next(cur_player):
    if cur_player == "BOB":
        return "ANDY"
    else:
        return "BOB"
```

### other solution
- https://www.hackerrank.com/challenges/an-interesting-game-1/forum
```
public class Solution {

    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int g = in.nextInt();
        for(int a0 = 0; a0 < g; a0++){
            int n = in.nextInt();
            int count = 0;
            int max = 0;
            for (int i = 0; i < n; i++) {
                int number = in.nextInt();
                if (max < number) {
                    max = number;
                    count++;
                }
            }
            System.out.println(count % 2 == 0 ? "ANDY" : "BOB");
        }
    }
}
```