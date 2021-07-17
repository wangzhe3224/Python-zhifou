# list vs tuple

建议：能够使用tuple的时候，有限使用tuple。你想用list的时候，停下来想一下是否可以用tuple？

- tuple less than 20 elements, are cached by runtime (20,000 of them)
- list.append may trigger resize, which leads to slowness and larger memory

```text
>>> %memit [i*i for i in range(100_000)] 
peak memory: 70.50 MiB, increment: 3.02 MiB

>>> %%memit l = []
... for i in range(100_000):
... l.append(i * 2)
...
peak memory: 67.47 MiB, increment: 8.17 MiB

>>> %timeit [i*i for i in range(100_000)]
7.99 ms ± 219 μs per loop (mean ± std. dev. of 7 runs, 100 loops each)

>>> %%timeit l = []
... for i in range(100_000):
... l.append(i * 2)
...
12.2 ms ± 184 μs per loop (mean ± std. dev. of 7 runs, 100 loops each)

>>> %timeit l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
95 ns ± 1.87 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

>>> %timeit t = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
12.5 ns ± 0.199 ns per loop (mean ± std. dev. of 7 runs, 100000000 loops each)
```