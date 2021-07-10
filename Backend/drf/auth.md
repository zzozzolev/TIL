# authtoken
- token으로 해도 request.user에 유저가 남는다.
- `urls.py`
    ```python
    from rest_framework.authtoken.views import obtain_auth_token

    urlpatterns = [
        url(r"^get-auth-token/", obtain_auth_token, name="get-auth-token"),
        url(r"^users/", ListUsersView.as_view())
    ]
    ```
- `views.py`
    ```python
    from rest_framework.permissions import AllowAny, IsAuthenticated

    class ListUsersView(ListAPIView):
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)
        serializer_class = RegisterSerializer

        def get(self, request, *args, **kwargs):
            print(request.user)
            return self.list(request, *args, **kwargs)
    ```