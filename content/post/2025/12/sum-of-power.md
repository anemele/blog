---
title: 幂和问题
description: $S_k(n)=1^k+2^k+...+n^k$
date: 2025-12-20T01:15:43+0800
lastmod: 2025-12-20T01:15:43+0800
draft: false
tags:
 - power
 - sum
categories:
 - math
math: true
---

对于通项为 $a_k(n)=n^k$ 的序列，其前 n 项和为 $S_k(n)=1^k+2^k+...+n^k$，其中 $n=1,2,3,...;k=0,1,2,...$。


研究幂和计算问题的核心公式是「相邻数高一次幂差」与「二项式定理」：

$$
(i+1)^{k+1}-i^{k+1}=
\tbinom{k+1}{1}i^k+\tbinom{k+1}{2}i^{k-1}+...+\tbinom{k+1}{k}i+1=
\sum_{j=1}^{k+1}\tbinom{k+1}{j}i^{k+1-j}
$$

该式左右两边对 $i$ 从 $1$ 到 $n$ 求和，左边消去得到简单多项式，右边聚合得到幂和组合：

$$
(n+1)^{k+1}-1=
\tbinom{k+1}{1}S_k+\tbinom{k+1}{2}S_{k-1}+...+\tbinom{k+1}{k}S_1+S_0=
\sum_{j=1}^{k+1}\tbinom{k+1}{j}S_{k+1-j}
$$

依次代入 $k=0,1,2,3,...$ 可以得到：

$$
\begin{align*}
(n+1)^1-1&=S_0\\
(n+1)^2-1&=2S_1+S_0\\
(n+1)^3-1&=3S_2+3S_1+S_0\\
(n+1)^4-1&=4S_3+6S_2+4S_1+S_0\\
&...
\end{align*}
$$

进而得到常用的幂和通式：

$$
\begin{align*}
S_0&=n\\
S_1&=\frac{n(n+1)}{2}\\
S_2&=\frac{n(n+1)(2n+1)}{6}\\
S_3&=\frac{n^2(n+1)^2}{4}\\
&...
\end{align*}
$$

对于 $k\ge4$ 的情况，如果常用，则可以迭代**符号计算**得到关于 $n$ 的式子，否则可以**数值计算**得到数值结果。

对于其他由（非负）幂运算组合的序列，可以化为幂序列的线性组合，其幂和也是线性组合。
负数幂不适用。

使用 sympy 做符号计算：

```python
from sympy import *

n = symbols('n')

_Sk_cache = [n]

def get_Sk(k: int):
    # k >= 0
    # 该算法性能一般，k 不要取得过大，否则耗时很高。建议小于 10。
    length = len(_Sk_cache)
    if length > k:
        return _Sk_cache[k]
    for idx in range(length, k+1):
        tmp = n
        for i in range(2, k+1):
            tmp += binomial(k+1, i) * _Sk_cache[idx+1-i]
        S = ((n+1)**(k+1)-1-tmp) / (k+1)
        S = factor(S)
        _Sk_cache.append(S)
    return S

def test_get_Sk():
    samples = [n, n*(n+1)/2, n*(n+1)*(2*n+1)/6, n**2*(n+1)**2/4]
    for k, S in enumerate(samples):
        assert get_Sk(k) == S

test_get_Sk()

# 代入求值
S3 = get_Sk(3).subs(n, 100)
print(S3)
# 25502500
```

使用 Julia 做数值计算，因为可能遇到大整数，numpy 不太好用。
数值计算就用最朴素的方法，而非符号计算的推导，后者做数值运算太复杂。

```julia
f(k, n) = sum((1:big(n)).^k)
print(f(5, 10000))
# 166716670833333325000000
```

最后再强调一遍，如果是单次计算，直接用朴素方法；
如果需要多次甚至大量计算，先用符号计算得到关于 n 的表达式是更好的做法，
这样可以将复杂运算提前完成，后续都是 $O(1)$ 运算。
