### 소요 시간
- 1시간 12분
    - 문제 이해: 17분
    - 코드 작성 및 테스트 케이스 반 성공: 45분
    - 고치기 및 포기: 10분

### 통과율
- 80%

### 접근법
- `target`이 `words`에 있는 지 확인
- 각각의 단어를 돌면서 바꿀 수 있는 단어를 queue에 집어 넣음
- level을 이용해 기준 단어로부터 얼마나 떨어져있는지 트랙킹
- target의 level을 반환

### 문제점


### my solution
```
from collections import defaultdict

def solution(begin, target, words):
    if target not in words:
        return 0
    else:
        queue = [begin]
        count = 0
        # 각각의 단어 들에 대한 charset 구하기
        mapping = get_charset_mapping(begin, words) 
        words_level = get_words_level(begin, words)
        # for 문 돌면서 각각의 단어들과 비교
        while queue:
            criterion = queue.pop(0)
            for word in words:
                # 정확히 일치하는 단어가 있는 지 확인
                dif_char_count = get_different_char_count(
                    mapping[criterion],
                    mapping[word]
                )
                if dif_char_count <= 1:
                    count += 1
                    if dif_char_count == 0:
                        break
                    else:
                        words_level[word] += words_level[criterion]
                        queue.append(word)
                        words.remove(word)
        return words_level[target]
    
def get_charset_mapping(begin, words):
    concated = words + [begin]
    mapping = {}
    for word in concated:
        mapping[word] = [c for c in word]
    return mapping

def get_words_level(begin, words):
    words_level = {word: 1 for word in words}
    words_level[begin] = 0
    return words_level

def get_different_char_count(criterion_charset, comp_charset):
    # 1 -> changable, 0 -> same
    return len(set(criterion_charset).difference(set(comp_charset)))
```

### other solution
- https://cocojelly.github.io/algorithm/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%A8%B8%EC%8A%A4-%EC%BD%94%EB%94%A9%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%97%B0%EC%8A%B5-DFS-BFS-(3)/
```
from collections import deque as queue

transistable = lambda a,b: sum((1 if x!=y else 0) for x,y in zip(a,b)) == 1

def solution(begin,target,words):
    q, d = queue(), dict()
    q.append((begin, 0))
    d[begin] = set(filter(lambda x:transistable(x,begin), words))
    
    for w in words:
        d[w] = set(filter(lambda x:transistable(x,w), words))
       
    while q:
        cur, level  = q.popleft()
        if level > len(words):
            return 0
        for w in d[cur]:
            if w == target:
                return level + 1
            else:
                q.append((w, level + 1))
    
    return 0
```