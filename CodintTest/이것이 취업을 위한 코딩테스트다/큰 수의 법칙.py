_, m, k = 5, 8, 3
array = [2, 4, 5, 4, 6]

array.sort()
count = 0
answer = 0

while count < m:
    for _ in range(k):
        answer += array[-1]
        count += 1

        if count == m:
            break
    
    if count < m:
        answer += array[-2]
        count += 1

print(answer)