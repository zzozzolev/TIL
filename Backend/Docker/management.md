## CPU & Memory
- https://www.joinc.co.kr/w/man/12/docker/limits

## 실행중인 컨테이너 정보 보기(cpu, memory 등등)
- https://docs.docker.com/engine/reference/commandline/stats/

## 삭제 관련
- https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

## How to remove <none> images after building
```
docker rmi $(docker images --filter “dangling=true” -q --no-trunc)
```

## Purging All Unused or Dangling Images, Containers, Volumes, and Networks
```
docker system prune

# To additionally remove any stopped containers and all unused images 
# (not just dangling images), add the -a flag to the command:

docker system prune -a
```