# python

- 아무리 `settings.json`에 `"editor.formatOnSave": true`를 해도 prettier가 먹지 않는다면 아래 내용을 더해주자.
  ```json
  {
    "editor.formatOnSave": true,
    "[python]": {
      "gitlens.codeLens.symbolScopes": ["!Module"],
      "editor.defaultFormatter": "ms-python.python"
    }
  }
  ```
- [관련 이슈](https://github.com/prettier/prettier-vscode/issues/1395)
