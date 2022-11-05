## 다형성 (polymorphism)
- 역할과 구현을 분리하고 구현은 역할을 구현함.
- 클라이언트는 역할에만 의존해서 새로운 구현을 사용하더라도 클라이언트의 코드를 변경하지 않아도 됨.
- 새로운 구현은 무한대로 확장 가능.

## SOLID
- SRP: single responsibility principle
  - 한 클래스는 하나의 책임만 가짐.
  - 변경이 있을 때 파급 효과가 적음.
- OCP: open-closed priciple
  - 확장에는 열려있고 변경에는 닫혀있음.
  - 다형성 활용.
- LSP: liskov substitution principle
  - 구현체는 인터페이스 규약을 지켜야 함.
- ISP: interface segregation principle
  - 범용 인터페이스보다 여러 개가 더 나음.
- DIP: dependency inversion priciple
  - 구현에 의존하지 말고 인터페이스애 의존해야함.
- 다형성 만으로는 구현 객체를 변경할 때 클라이언트 코드도 함께 변경된다.
- 즉, 다형성 만으로는 OCP, DIP를 지킬 수 없다.
