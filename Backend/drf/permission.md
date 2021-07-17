# Object level permissions
- 종종 인증 수준이 아니라 권한 수준의 퍼미션이 필요할 때가 있다.
- 예를 들면 유저의 프로필은 자신만이 수정할 수 있고 다른 유저들은 수정할 수 없어야한다.
- drf에서 제공하는 `IsAuthenticated`는 인증을 했냐 아니냐는 검증할 수 있지만 권한까지는 검증할 수 없다.
- 따라서 오브젝트 수준으로 권한을 확인하려면 권한을 커스텀하게 정의하고 `has_object_permission`을 오버라이드하고 뷰에서 `check_object_permissions`를 호출해야한다.