## 공통점
- visited를 사용해 방문한 노드 표시

## DFS
- start와 연결된 a, a와 연결된 b... 이런 식으로 계속 연결된 것을 보는 알고리즘
- stack이냐 queue이냐가 중요한 거 같지는 않음
- 방문하고 visited의 해당 인데스에 표시하고 인접한 거에 `recursive하게 적용하는 게` 포인트

## BFS
- start와 연결된 a,b,c 이런 식으로 주변에 있는 걸 모두 보고 그 다음으로 이동하는 알고리즘
- queue 사용 (FIFO)
- 방문하고 visited의 해당 인덱스에 표시하고 `인접 인덱스를 모두 queue에 넣는게` 포인트
- queue가 빌 때까지 반복 

## 주의할 점
- tree와 graph를 DFS, BFS로 순회하는 건 다르다