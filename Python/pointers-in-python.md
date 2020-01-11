## 왜?
- C 공부하다가 pointer를 처음 봤는데 C 기반으로 돼있는 python에서는 이걸 어떻게 처리하는지 궁금해서 찾아봄.

## Why Doesn’t Python Have Pointers?
- Probably, but pointers seem to go against the Zen of Python. Pointers encourage implicit changes rather than explicit. Often, they are complex instead of simple, especially for beginners.
- Python often focuses on usability instead of speed. As a result, pointers in Python doesn’t really make sense.

## Objects in Python
- In Python, everything is an object. 

## Understanding Variables
- Python variables are fundamentally different than variables in C or C++. In fact, Python doesn’t even have variables. Python has names, not variables.
- C에서 새로운 value를 assign하면 주소가 바뀌는 게 아니라 주소는 그대로이고 value가 바뀜. thereby overwriting the previous value. It means that x is the memory location, not just a name for it. 아래처럼해도 x는 바뀌지 않음.
    ```
    int x = 2338;
    int y = x;
    y = 2337;
    ```

## Names in Python
- It is important to know that there is a difference between variables and names.
- The Python name x doesn’t directly own any memory address in the way the C variable x owned a static slot in memory.
```
# 1. Create a PyObject
# 2. Set the typecode to integer for the PyObject
# 3. Set the value to 2337 for the PyObject
# 4. Create a name called x
# 5. Point x to the new PyObject
# 6. Increase the refcount of the PyObject by 1

x = 2337
```
```
# 1. Creates a new PyObject
# 2. Sets the typecode to integer for the PyObject
# 3. Sets the value to 2338 for the PyObject
# 4. Points x to the new PyObject
# 5. Increases the refcount of the new PyObject by 1
# 6. Decreases the refcount of the old PyObject by 1

x = 2338
```
- In addition, the previous object (which held the 2337 value) is now sitting in memory with a ref count of 0 and will get cleaned up by the garbage collector.

## A Note on Intern Objects in Python
- Python pre-creates a certain subset of objects in memory and keeps them in the global namespace for everyday use.
- Which objects depend on the implementation of Python. CPython 3.7 interns the following:
    1. Integer numbers between -5 and 256
    2. Strings that contain ASCII letters, digits, or underscores only
- Strings that are less than 20 characters and contain ASCII letters, digits, or underscores will be interned.
- Bonus: If you really want these objects to reference the same internal object, then you may want to check out sys.intern(). One of the use cases for this function is outlined in the documentation.
    ```
    from sys import intern  # Python 3
 
    c = intern("Alex Lee")
    d = "Alex Lee"
    print(id(c), id(d), c is d) # 2987210077360 2987210078704 False
    
    e = intern("Alex Lee")
    print(id(c), id(e), c is e) # 2987210077360 2987210077360 True
    ```

## Simulating Pointers in Python
### Using Mutable Types as Pointers
- Using a `list` means that the end result appears to have modified the value.
- Another common approach to mimicking pointers in Python is to use a `dict`.
- Let’s say you had an application where you wanted to keep track of every time an interesting event happened. One way to achieve this would be to create a `dict` and use one of the items as a counter.
### Using Python Objects
- The `dict` option is a great way to emulate pointers in Python, but sometimes it gets tedious to remember the key name you used.
- This is where a custom Python class can really help.
```
class Metrics(object):
    def __init__(self):
        self._metrics = {
            "func_calls": 0,
            "cat_pictures_served": 0,
        }

    @property
    def func_calls(self):
        return self._metrics["func_calls"]

    @property
    def cat_pictures_served(self):
        return self._metrics["cat_pictures_served"]

    def inc_func_calls(self):
        self._metrics["func_calls"] += 1

    def inc_cat_pics(self):
        self._metrics["cat_pictures_served"] += 1
```

## Real Pointers With ctypes
- maybe there are pointers in Python, specifically CPython. Using the builtin `ctypes` module, you can create real C-style pointers in Python.
- 자세한 거는 reference에서 보기

## reference
- https://realpython.com/pointers-in-python/
- http://pythonstudy.xyz/python/article/512-%ED%8C%8C%EC%9D%B4%EC%8D%AC-Object-Interning