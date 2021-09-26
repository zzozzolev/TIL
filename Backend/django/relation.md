# 참조, 역참조
- 참고: https://velog.io/@ikswary/django-%EC%B0%B8%EC%A1%B0%EC%99%80-%EC%97%AD%EC%B0%B8%EC%A1%B0
- 참조는 model 내에서 `FoerignKey`로 선언해서 참조하면 된다.
- 역참조는 여러가지 방법이 있지만 `ForeignKey`를 만들 때 설정한 `related_name`으로 접근하는 게 제일 빠르다고 한다.

# relationship
- [문서](https://docs.djangoproject.com/en/3.2/ref/models/fields/#foreignkey)
- 장고에서는 realtionship을 나타낼 수 있는 필드가 3가지가 있다.
  1. `ForeignKey`
    - A many-to-one relationship.
  2. `ManyToManyField`
  3. `OneToOneField`
    - A one-to-one relationship.
    - Conceptually, this is similar to a `ForeignKey` with `unique=True`.
    - the “reverse” side of the relation will directly return a single object.

# ManyToManyField와 junction table
- `Foreignkey`, `OneToOneField`와 달리 `ManyToManyField`는 한 테이블로 나타낼 수 없다.
- 따라서 junction table이라고 불리는 associative table이 만들어진다.
- table에는 `(해당 테이블에 대한 id)`, `(ManyToManyField를 선언한 모델의 id)`, `(ManyToManyField가 가리키는 모델의 id)`를 기록한다.
- [참고](https://brunch.co.kr/@ddangdol/6)
- 단, 헷갈리지 말아야할 것은 선언한 `ManyToManyField`에 접근하면 `ManyToManyField`가 가리키는 모델과 동일하다. 그래서 해당 테이블 id와 해당 필드의 id는 서로 다르다.
  - 예를 들어 다음과 같이 모델에 `ManyToManyField`가 선언돼있다.
    ```
    class Profile():
      liked_posts = models.ManyToManyField(
        "posts.Post", related_name="liked_authors")
    ```
  - `liked_posts`에 post를 추가하면 table은 다음과 같이 만들어진다.
    ```
    | id | profile_id | post_id |
    | -- | ---------- | ------- |
    | 1  |          7 |       1 |
    | 10 |          7 |       5 |
    ```
  - 이때 `profile.liked_posts`에서 쿼리를 얻으면 다음과 같이 `post_id`가 `id`로 나온다. 즉, junction table id가 아니다.
    ```
    <QuerySet [{'id': 5, ... }, {'id': 1, ... }] >
    ```