---
title: PNG alpha channel processing
description:
    PNG 图片 alpha 通道处理，即透明度如何影响图片显示，
    也就是之前在「幻影坦克图片原理」里面提到的「PNG 混色原理」。
date: 2025-02-07
lastmod: 2025-02-07
math: true
tags:
 - PNG
 - alpha channel
categories: Image processing
---

<!--more-->

## 背景介绍

常见的图片格式主要是 JPG 和 PNG ，二者除了文件格式、压缩率等区别，
最主要的一点是 PNG 支持 alpha 通道，也就是透明度。

我们知道，显示器只能显示颜色，无法「显示」透明度。透明度在图像渲染之前
已经做过处理，显示器的输入是处理后的颜色，不包含透明度信息。

「PNG 混色原理」给出一个公式，正是用于计算透明度对颜色的影响。
该公式是当时参考了一篇博客，博客也是直接给出了数学公式，没有详细的讲解。
后来了解到「线性插值」算法，形式上与该公式类似，于是补充介绍该公式就是
「线性插值」算法。

前不久学习「贝塞尔曲线」（Bezier curve），深入了解了「线性插值」算法。
研究「局部幻影坦克」时回想起此事，发现对于 PNG 图片的 alpha 通道处理
原理还是不太了解，于是查询相关资料，整理如下。

## PNG alpha 通道处理

权威资料：
[13.16 Alpha channel processing](https://www.w3.org/TR/png-3/#13Alpha-channel-processing)

原文摘录：

> The alpha channel can be used to ***composite*** a foreground image against a background image. The PNG datastream defines the foreground image and the transparency mask, but not the background image. PNG decoders are not required to support this most general case. It is expected that most will be able to support compositing against a single background color.
>
> The equation for computing a composited sample value is:
>
> ```
> output = alpha * foreground + (1-alpha) * background
> ```
> where alpha and the input and output sample values are expressed as fractions in the range 0 to 1. This computation should be performed with intensity samples (not gamma-encoded samples). For color images, the computation is done separately for R, G, and B samples.

其中 `composite` [定义](https://www.w3.org/TR/png-3/#dfn-composited)为：

> composite (verb)
>
> form an image by merging a foreground image and a background image, using transparency information to determine where and to what extent the background should be visible.
>
> > Note
> >
> > The foreground image is said to be composited against the background.

根据以上资料， PNG alpha 通道处理还是使用公式：

$$
l = \alpha \cdot f + (1-\alpha) \cdot b
$$

其中 $l$ 为显示像素，$f$ 为前景像素，$b$ 为后景像素。
「彩色图像」（color image）分别计算 $l_r, l_g, l_b$。

## alpha 的含义以及与线性插值算法的关系

alpha 称为「透明度」，也称为「不透明度」，取值范围为 0~1。
实际上「不透明度」更为合适。

根据公式，显示色是前景色和后景色的加权平均值，
其中前景色的权重为 alpha，后景色的权重为 1-alpha。
也就是说， alpha 越接近 1，显示越接近前景；alpha 越接近 0，
显示越接近后景。

显示器显色原理是发光显色，后景光要透过前景；
alpha 越大，后景权重越小，透明度越低，因此称为「不透明度」。

线性插值算法是在空间中任意两点 $P_0$ 和 $P_1$ 之间插入一个点 $P$，
如果 $P_0$ 到 $P$ 的距离与 $P_0$ 到 $P_1$ 的距离之比为 $t$，
则存在关系： $P = (1-t) \cdot P_0 + t \cdot P_1$。

这里可以将前景色作为 $P_1$ ，后景色作为 $P_0$ ，不透明度作为 $t$ ，
显示色作为 $P$ 。不透明度表示显示色与后景色的距离。

...
