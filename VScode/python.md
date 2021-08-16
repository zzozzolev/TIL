# Venv

- `python -m venv {venv folder}`로 가상 환경을 만들 때 가상 환경 폴더가 워크 스페이스 바로 밑에 있어야 vscode가 인식을 할 수 있다.
- 예를 들면 `django-project`라는 워크 스페이스가 있다면 `django-project/venv` 이렇게 있어야 한다.
- 만약 이렇게 안 하면 가상 환경에 아무리 패키지를 설치해도 인식을 못해서 VScode에서 패키지 관련된 클래스나 함수를 자동완성해주지 않는다 ㅠ
- 그리고 나중에 인터프리터를 잘못 지정하거나 한 번 가상환경을 잘못 만들면 아무리 VScode를 재시작하거나 워크 스페이스를 지우고 해도 안 된다. 아마 VScode에서 caching 하는 것 때문에 그런듯...
- 그래서 뭘 해도 안 된다면 그냥 워크 스페이스를 새로운 이름으로 git clone해서 가장 상위에 가상 환경 폴더를 만들어주면 된다.
- 정확환 원인을 파악하지 못하겠지만 setting에서 `"python.experiments.enabled"`가 체크돼있다면(true라면) 창을 끄고 나서 다시 열었을 때 아무런 definition도 찾지 못한다 ㅠㅠ 따라서 이 설정을 꺼줘야한다. venv 뿐만 아니라 [다른 곳](https://github.com/microsoft/vscode-python/issues/15520)에서도 이거 때문에 안 되는 사례가 종종 있는 것 같다.
