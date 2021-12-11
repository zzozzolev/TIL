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

## Varargs
- 하나의 타입에 대해서 임의의 개수를 가지는 파라미터를 지원하는 메서드를 처리하기 위한 편리한 방법이다.
- 메서드의 내용은 같은데 단순히 파라미터 개수만 차이가 나는 경우에 유용하게 사용할 수 있다.
- 예를 들어 다음과 같이 정의하면 임의의 숫자만큼 argument들을 넘겨줄 수 있다.
  ```java
  public String function(String... values) {
    // ...
  }
  formatWithVarArgs();
  formatWithVarArgs("a", "b", "c", "d");
  ```
- varargs는 array처럼 다루면 된다.
- 단 각각의 메서드는 하나의 varargs 파라미터만 가질 수 있고 마지막 파라미터여야한다.
- varargs를 사용할 때마다 자바 컴파일러는 주어진 파라미터들을 가지고 있는 어레이를 만든다.
- varargs를 제네릭 타입과 사용할 때는 런타임 예외가 발생할 위험이 있다.
- [참고](https://www.baeldung.com/java-varargs)