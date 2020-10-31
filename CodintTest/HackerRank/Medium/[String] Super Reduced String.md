### 소모 시간
- 26분 27초

### 통과율
- 100%

### 문제점
- 쓸데없이 복잡하다.
- stack을 사용하려다 결국 안 썼는데 다른 사람 풀이보니 그냥 스택을 사용했어도 될 거 같다.
- for문을 사용하면 사이가 없어져서 같은 게 되버리는 게 문제여서 안 썼는데 그냥 `i`만 초기화했으면 해결됐다.

### my solution
```
def superReducedString(s):
    char_counter = dict(Counter(s))

    while True:
        in_flag = False
        for i in range(len(s)-1):
            count = 1 # i
            if s[i] == s[i+1]:
                in_flag = True
                k = i + 1
                while k < len(s) and s[i] == s[k]:
                    count += 1
                    k += 1

                # k는 그 다음 인덱스
                if count % 2 == 0:
                    char_counter[s[i]] -= count
                    s = s[:i] + s[k:]
                    
                else:
                    char_counter[s[i]] -= count - 1
                    s = s[:i] + s[k-1:]           
                break
    
        if len(s) <= 1 or not in_flag:
            break
    
    if len(s) == 0:
        return "Empty String"
    else:
        return s
```

### other solution
- https://www.hackerrank.com/challenges/reduced-string/forum
```
public static void main(String[] args) {
        Scanner stdin = new Scanner(System.in);
        StringBuffer s = new StringBuffer(stdin.nextLine());
        for(int i = 1; i < s.length(); i++) {
            if(s.charAt(i) == s.charAt(i-1)) {
                s.delete(i-1, i+1);
                i = 0; # 조건 맞을 때 0으로 초기화하면 사이에 제거되고 밖에 있던 게 같아지더라도 괜찮음
            }
        }
        if(s.length() == 0) System.out.println("Empty String");
        else System.out.println(s);
    }
}
```
```
int top = -1;

for(int i=0;i<strlen(string);i++){

    if(i==0)
        stack[++top]=string[i];
    else
        {
        if(stack[top]==string[i])
            top--;
        else
            stack[++top]=string[i];


    }
}

if(top==-1)
    printf("Empty String");
else
    {
    for(int i=0;i<=top;i++)
        printf("%c",stack[i]);
}
```
