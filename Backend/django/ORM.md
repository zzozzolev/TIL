## ORM의 특징
### Lazy Loading
- 필요한 시점에 SQL을 호출한다.
  ```python
  users = User.objects.all() # 아직 쿼리셋
  ...
  user_list = list(users) # SQL 호출
  ```
- 불필요한 SQL이 두 번 호출될 수 있다. SQL을 한 번 호출해 전체 데이터를 가져와 재사용하면 되지만 ORM은 이를 알 수 없다.
  ```python
  users = User.objects.all()

  first_user = users[0] # SELECT ... LIMIT 1
  user_list = list(users) # SELECT ...
  ```

### Caching
- `QuerySet` 캐싱을 재사용 하는 법
- 쿼리셋을 호출하는 순서가 바뀌는 것만으로도 `QuerySet` 캐싱 때문에 날리는 SQL이 달라질 수 있다.
  ```python
  users = User.objects.all()

  user_list = list(users) # SELECT ...
  # users 쿼리셋은 모든 user를 가져오는 SQL을 이미 호출했다.
  # 0번째 user는 users 쿼리셋에 캐싱된 값을 재활용해 SQL을 호출하지 않는다.
  first_user = users[0]
  ```
- ORM은 SQL 수행결과를 캐싱한다.
- 이를 Result Cache라고 한다.
