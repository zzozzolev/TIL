## Docker in docker
```
# docker file
RUN apt-get install -y --no-install-recommends apt-utils
RUN curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh
```
```
docker run -v /var/run/docker.sock:/var/run/docker.sock
```

## How to search for containers that don't match the result of “docker ps --filter”?
- https://stackoverflow.com/questions/31959553/how-to-search-for-containers-that-dont-match-the-result-of-docker-ps-filter

## How to add health check
- https://howchoo.com/g/zwjhogrkywe/how-to-add-a-health-check-to-your-docker-container