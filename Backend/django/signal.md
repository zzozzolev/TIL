# Signal이 뭘까?
- [Django Signals- master pre_save and post_save](https://medium.com/@singhgautam7/django-signals-master-pre-save-and-post-save-422889b2839)
- "Signal hooks some piece of code to be executed as soon as a specific model’s save method is triggered."
- "Signals are best used when multiple pieces of code are interested in the same model instance events."
- 단, bulk로 object를 만들거나 업데이트할 때 `pre_save` 혹은 `post_save`는 호출되지 않는다.