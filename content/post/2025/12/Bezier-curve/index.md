---
title: 贝塞尔曲线 Bézier/Bezier curve
description: 整理对「贝塞尔曲线」的研究
date: 2025-12-20T02:56:29+0800
lastmod: 2025-12-20T02:56:29+0800
draft: false
tags:
 - Bezier curve
categories:
 - math
math: true
---

「贝塞尔曲线」是计算机绘制曲线图的方法，之前偶然看到一个游戏开发者
介绍贝塞尔曲线，内容很好：[B站搬运](https://www.bilibili.com/video/BV1zgztY7EJF)/[油管](https://www.youtube.com/watch?v=aVwxzDHniEw)。于是稍微研究一番，做个记录。

> 实际上这个研究是很早之前在 jupyter 上面完成的，现在只是整理成文。

对于平面上两点 $P_0$ 和 $P_1$，在其连线上有一个点 $P$，根据线性插值
（linear interpolation, lerp）算法有：$P=lerp(P_0,P_1,t)$，其中
$t=\frac{P_0P}{P_0P_1}$。该式子展开为 $P=(1-t)P_0+tP_1$。

对于三个点的情况，$P_0$ 和 $P_1$ 之间有一个点，$P_1$ 和 $P_2$ 之间也有
一个点，这两个点之间又有一个点 $P$，根据 $t\in[0,1]$，$P$ 的轨迹
就是贝塞尔曲线，具体来说，三个点控制的称为「二阶贝塞尔曲线」。

贝塞尔曲线完全由离散的点控制，只要改变控制点就可以得到不同的曲线，
这对计算机绘图十分方便，曲线上的点坐标都是可以准确计算出来的。

以二阶曲线为例，根据线性插值有

$$
\begin{align*}
P'&=(1-t)P_0+tP_1\\
P''&=(1-t)P_1+tP_2\\
P&=(1-t)P'+tP''\\
&=(t^2-2t+1)P_0+(2t-2t^2)P_1+t^2P_2
\end{align*}
$$

$P$ 是关于 $t$ 变化的量，记为函数

$$
B(t)=\sum_{i=0}^{n}P_{i}B_{i,n}(t)
$$

其中 $B_{i,n}(t)=\binom{n}{i}t^{i}(1-t)^{n-i}$, $t\in[0,1]$，
称为「伯恩斯坦多项式」。

这个式子可以再进一步变换成矩阵乘法形式

$$
\begin{align*}
P&=(t^2-2t+1)P_0+(2t-2t^2)P_1+t^2P_2\\
&=\begin{bmatrix}
t^2 & t & 1
\end{bmatrix}
\begin{bmatrix}
1 & -2 & 1 \\
-2 & 2 & 0 \\
1 & 0 & 0
\end{bmatrix}
\begin{bmatrix}
P_0 \\ P_1 \\ P_2
\end{bmatrix}
\end{align*}
$$

这样将变量和常量分离开来，方便研究。
注意到乘式中间是一个**对称方阵**，称为「伯恩斯坦矩阵」。

对于固定控制点数，伯恩斯坦矩阵是不变的。
例如二阶曲线有三个控制点，该矩阵就是如上的三阶方阵。
这样曲线上的点只与变量 $t$ 有关，方便计算。

现在的任务是计算伯恩斯坦矩阵和贝塞尔曲线，
下面使用 Julia 完成：

```julia
function gen_i(n, i)
    a = binomial(n, i)
    s = 0:n-i
    b = binomial.(n-i, s)
    c = (-1) .^ s
    @. a * b * c
end

function gen_bernstein_matrix(n)
    res = zeros((n+1, n+1))
    for i = 1:n+1
        res[i, i:n+1] = gen_i(n, i-1)
    end
    res
end

function calcute_bezier_curve(points, num=100)
    n, _ = size(points)
    bernstein_matrix = gen_bernstein_matrix(n-1)
    t = LinRange(0, 1, num)
    ts = t .^ reshape(0:n-1, (1, n))
    res = ts * transpose(bernstein_matrix) * points
end

using Plots

function calc_and_plot_bezier_curve(points)
    cps = calcute_bezier_curve(points)
    scatter(points[:,1], points[:,2], label="Control points")
    plot!(points[:,1], points[:,2], label="Control curve")
    plot!(cps[:,1], cps[:,2], label="Bezier curve")
end

points = [
    0 0
    1 3
    2 -1
    5 6
    2 10
    0.5 4
    2 7
    4 2
]

calc_and_plot_bezier_curve(points)

savefig("demo.svg")
```

得到如下曲线图：

![贝塞尔曲线](demo.svg)

EOF
