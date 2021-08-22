# queryset vs get_queryset

- https://www.django-rest-framework.org/api-guide/generic-views/#attributes
- `queryset`은 클래스 변수이므로 한 번만 evaluated 되고, 그러한 결과들을 모든 뒤이은 리퀘스트들에 캐쉬된다.
- 따라서 `view` 메서드를 오버라이딩할 때는 해당 property에 바로 접근하기보다는 `get_queryset` 호출하는 것이 중요하다.
- 좀 더 구체적으로 말하면 `queryset`은 쿼리셋에서 가장 일반적인 부분으로 지정하고 `get_queryset`은 `filter`를 이용해 리퀘스트마다 달라지는 부분으로 지정한다.
- 예를 들어 post에 대한 viewset을 만든다고 가정해보자. 그러면 `queryset`과 `get_queryset`은 다음과 같이 지정할 수 있을 것이다.

  ```
  class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.select_related("author", "author__user")

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author is not None:
            queryset = queryset.filter(author__user__username=author)
  ```

# ViewSet
## 정의하지 않은 메서드
- `ViewSet`에 정의하지 않은 메서드는 요청시 `405 METHOD_NOT_ALLOWED`가 응답으로 온다.
  - 예를 들면 `ViewSet`에 `partial_update`만 정의하고 `PUT`으로 요청하면 해당 응답이 온다.
  - 단, `APIView`는 `http_method_names`로 직접 지정하지 않으면 이렇게 처리가 안 되는 것 같다.