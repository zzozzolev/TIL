# 참조, 역참조
- 참고: https://velog.io/@ikswary/django-%EC%B0%B8%EC%A1%B0%EC%99%80-%EC%97%AD%EC%B0%B8%EC%A1%B0
- 참조는 model 내에서 `FoerignKey`로 선언해서 참조하면 된다.
- 역참조는 여러가지 방법이 있지만 `ForeignKey`를 만들 때 설정한 `related_name`으로 접근하는 게 제일 빠르다고 한다.