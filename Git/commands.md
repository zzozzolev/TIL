### branch 한번에 삭제하기
```
git branch -d feature/a feature/b

or

git branch | grep 'feature' | xargs git branch -d
```

### 특정 커밋만을 머지하기
```
git cherry-pick <commit-id>
```

### 로컬 브랜치의 내용을 리모트 브랜치에 강제하기
```
git push --force origin <branch>
```

### stash한 내용 보기
```
git show stash@{stash 번호}
```

### 파일 간 변경 이력 보기
```
git blame -C {파일명}
```

### remote tag 최신 master로 변경
```
git pull origin master
git tag v0.1.0 -f
git push origin v0.1.0 -f
```

### remote 명령어 사용을 위해 username 및 password 설정
```
git remote remove origin
git remote add origin https://username:password@<repository url>
```

### 버전 간의 차이점을 비교할 때 
```
git diff '버전 id'..'버전 id2'
```