# 迭代器有意思的例子

```python
@staticmethod
def _get_tasks(func, it, size):
    it = iter(it)
    while 1:
        x = tuple(itertools.islice(it, size))
        if not x:
            return
        yield (func, x)
```

