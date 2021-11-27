## instanceof vs getClass()
- `instanceof`는 서브 클래스와 비교해도 `true`를 반환한다.
- 하지만 `getClass()`는 subclass 객체와 비교하면 `false`를 반환한다.
- 자세한 예시는 [여기](http://burucodegallery.blogspot.com/2013/08/4-3-instance-of-getclass.html) 참고.

## generic method와 wild card의 차이
- [when-to-use-generic-methods-and-when-to-use-wild-card](https://stackoverflow.com/questions/18176594/when-to-use-generic-methods-and-when-to-use-wild-card)
1. 여러 argument가 있을 때 argument끼리 특정 타입으로 강제해야된다면 wildcard가 아닌 generic을 사용해야한다.
    - 예를 들어 아래 예시에서 `dest`와 `src`의 타입을 같게 만들고 싶다면 generic을 이용해야한다. wildcard의 경우 `dest`는 `List<Integer>`이고 `src`는 `List<Float>`일 수도 있다.
    ```java
    public static <T extends Number> void copy(List<T> dest, List<T> src) // ok
    
    public static void copy(List<? extends Number> dest, List<? extends Number> src) // x
    ```
2. wildcard는 upper bound와 lower bound 모두 제공해주지만 type parameter는 upper bound만 제공한다.
  - 예를 들어 `Integer` 타입의 `List`를 취하거나 슈퍼 클래스를 취하는 메서드를 정의하고 싶다면 wild card를 써야한다.
    ```java
    public void print(List<? super Integer> list)  // OK

    public <T super Integer> void print(List<T> list)  // Won't compile
    ```
