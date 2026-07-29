---
title: Fibonacci 数算法
description:
date: 2026-07-22T10:06:40+08:00
lastmod: 2026-07-29T20:54:06+08:00
tags:
- Fibonacci
- dynamic programming
- matrix
categories: algorithm
math: true
---

计算斐波那契数是学习算法的常用案例，本文依此由浅入深介绍几种算法。

## 递归

斐波那契数是递归定义，递归是很直观的算法。

```haskell
fib 0=0
fib 1=1
fib n=fib(n-1)+fib(n-2)
```

```python
def fib(n):
  if n<2:
    return n
  return fib(n-1)+fib(n-2)
```

递归容易理解，但复杂度极高，不适合实际计算。例如 `fib 100` 基本不会停机。

## 记忆化搜索

二叉展开递归，发现存在大量重复计算。例如 $f_n$ 和 $f_{n-1}$ 都依赖 $f_{n-2}$，但是需要分别计算，每次计算的代价很高。因此缓存中间结果，用空间换时间是很好的优化。

Python 可用 `lru_cache`。

```python
from functools import lru_cache

@lru_cache
def fib(n):
  ...
```

## 动态规划

递归是从上到下，遇到边界条件结束；
动态规划是从下到上，从边界条件出发，遇到给定值结束，对于递归分叉的问题十分有效。

```python
def fib(n):
  a,b=0,1
  for _ in range(n):
    a,b=b,a+b
  return a
```

## 矩阵幂

$$
\begin{align*}
f_3 &= f_2+f_1 \\
f_2 &= f_2
\end{align*}
$$

$$
\begin{align*}
\begin{bmatrix}
f_3 \\ f_2
\end{bmatrix}
&=
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix}
\begin{bmatrix}
f_2 \\ f_1
\end{bmatrix}
\\
&=
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix}^2
\begin{bmatrix}
f_1 \\ f_0
\end{bmatrix}
\\
&=
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix}^2
\begin{bmatrix}
1 \\ 0
\end{bmatrix}
\end{align*}
$$

$$
\begin{align*}
\begin{bmatrix}
f_n \\ f_{n-1}
\end{bmatrix}
&=
\begin{bmatrix}
1 & 1 \\ 1 & 0
\end{bmatrix}^{n-1}
\begin{bmatrix}
1 \\ 0
\end{bmatrix}
\end{align*}
$$

Julia 实现

```julia
function fib(n)
  init=big.([1 1;1 0])
  ret=init^(n-1)
  ret[1]
end
```

一行流

```julia
fib(n)=big.([1 1;1 0])^(n-1)|>first
```

Pure Python implementation
(实测速度远低于 Julia，仅作为条件不足的备选。)

```python
type M = tuple[int, int, int, int]
type UInt = int

def matrix_mul(m1: M, m2: M) -> M:
  return (
    m1[0] * m2[0] + m1[1] * m2[2],
    m1[0] * m2[1] + m1[1] * m2[3],
    m1[2] * m2[0] + m1[3] * m2[2],
    m1[2] * m2[1] + m1[3] * m2[3],
  )

def fast_power(m: M, p: UInt) -> M:
  ret = (1, 0, 0, 1)
  while p:
    if p & 1:
      ret = matrix_mul(ret, m)
    m = matrix_mul(m, m)
    p >>= 1
  return ret

def fib(n: UInt) -> UInt:
  if n < 1:
    return 0
  tmp = fast_power((1, 1, 1, 0), n - 1)
  return tmp[0]
```

幂运算一般是快速幂算法实现。

>  **快速幂算法**
>
> ```python
> def fast_power(a, b):
>   # a^b
>   ret = 1 # identity
>   while b:
>     if b & 1:
>       ret *= a
>     a *= a
>     b >>= 1
>
>   return ret
> ```

*特征方程-通项公式*

$$
F_n=\frac{1}{\sqrt 5}[(\frac{1+\sqrt 5}2)^n-(\frac{1-\sqrt 5}2)^n]
$$

涉及浮点运算，不适合计算机精确求值。

## 复杂度

| 算法 | 时间复杂度 | 空间复杂度 |
| -- | -- | -- |
| 递归 | | |
| 记忆化搜索 | O(n) | O(n) |
| 动态规划 | O(n) | O(1) |
| 矩阵幂 | O(log2(n)) | O(1) |
