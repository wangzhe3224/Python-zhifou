# 这样的Python代码很“不入流”

## 1. `from abc import *`

会污染你的命名空间，Bug的温床，不应该出现在正式场合。

## 2. 使用裸 `open` 获得文件句柄

```python
# 【BAD】很不专业，容易忘记关闭造成泄漏
f = open(filename, "w")
f.write("hello!\n")
f.close()

# 【GOOD】使用上下文管理器，自动关闭，即使出现异常也没关系
with open(filename) as f:
    f.write("hello!\n")
```

## 3. `try ... finally` 关闭句柄

```python
# 【BAD】
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    s.sendall(b'Hello, world')
finally:
    s.close()

# 【GOOD】
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'Hello, world')
```

## 4. `try...except` 捕捉一切

```python
# 【BAD】
while True:
    try:
        s = input("输入：")
        x = int(s)
        break
    except:  
        # 这种捕捉一切，会导致 Ctrl-C 都无法终止程序，即一些信号也会被捕捉
        # 即使希望捕捉信号，也应该明确
        print("错了，重试")

#【GOOD】
while True:
    try:
        s = input("输入：")
        x = int(s)
        break
    except Exception:  # 这样还好
        print("错了，重试")
    except (KeyError, ValueError):  # 这样是最好的，明确你要捕捉什么异常
        print("错了，重试")

```

## 5. 单例的等于 `None`

BAD: `x == None`

GOOD: `x is None`

## 6. 用 `+` 连接字符串

```python
# 【BAD】
name = "x"
a = "a" + "b" + "_" + name

# 【GOOD】
a = f"ab_{name}"
```