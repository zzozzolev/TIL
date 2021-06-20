# SlugField란?
- [공식 문서 설명](https://docs.djangoproject.com/en/3.2/ref/models/fields/#slugfield)
- letters, numbers, underscores, hyphens로만 이루어진 field.
- URL에 쓰일 수 있는 field. title 같은 것을 그대로 사용하면 보기에 좋지 않음.
  ```
  www.example.com/article/The%2046%20Year%20Old%20Virgin (x)

  www.example.com/article/the-46-year-old-virgin (o)
  ```
- [참고](https://itmining.tistory.com/119)