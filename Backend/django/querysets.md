# get_or_created
- This is meant to prevent duplicate objects from being created when requests are made in parallel.
- kwargs가 unique 하지 않다면 중복된 row가 생성될 수 있음.
- [잘못 사용하면 발생할 수 았는 문제](https://youngminz.netlify.app/posts/get-or-create-deadlock)