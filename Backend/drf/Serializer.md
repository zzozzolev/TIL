### model에 없는 key 값을 넘겨주면 어떻게 될까?
- serializer에 model에 없는 key가 있어도 `is_valid`를 거친 `data`에는 해당 key가 존재하지 않는다. 즉 이상한 key 넘겨줘도 알아서 걸러줌

### read_only, write_only
- 해당 옵션들을 이용해 인스턴스를 업데이트 하거나 생성할 때 (deserialization) 사용할 것인지, representation에 내보낼 것인지 (serialization)를 결정할 수 있다.