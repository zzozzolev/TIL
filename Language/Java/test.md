## Mock 객체로 테스트하는 법
```java
package com.example.medium_clone.application;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static java.util.Objects.requireNonNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class LearnMockTest {

    @Test
    void testService() {
        // given
        SimpleRepository repository = mock(SimpleRepository.class);
        SimpleService service = new SimpleService(repository);
        String id = "hello";
        String expected = "Wow_FROM_SERVICE_";

        when(repository.findById(id)).thenReturn("Wow");

        // when
        String actual = service.get(id);

        // then
        assertEquals(expected, actual);
    }
}

class SimpleService {
    private final SimpleRepository repository;

    public SimpleService(final SimpleRepository simpleRepository) {
        repository = requireNonNull(simpleRepository);
    }

    public String get(String id) {
        String fromRepo = repository.findById(id);
        return fromRepo + "_FROM_SERVICE_";
    }
}

class SimpleRepository {
    private final Map<String, String> map;

    public SimpleRepository() {
        map = new HashMap<>();
        map.put("a", "b");
        System.out.println("I'm not mock");
    }

    public String findById(String id) {
        return map.get(id);
    }
}
```