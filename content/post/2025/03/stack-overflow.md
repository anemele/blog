---
title: Stack Overflow
description: 本博客记录一次编写 Rust 程序时遇到的堆栈溢出错误。
date: 2025-03-17
lastmod: 2025-03-17
tags:
 - stack
 - os
 - rust
 - c
categories: os
---

## 背景介绍

堆栈溢出是一个常见的内存错误。

程序加载到内存后以进程的形式存在，每个进程由操作系统分配内存，
通过虚拟地址技术，进程认为自己拥有一段连续的内存空间。
这段内存通常包括 text data heap stack 等部分，
text 和 data 是从硬盘加载到内存的，
heap 和 stack 是程序运行时动态分配的。
其中的 stack 根据机器和操作系统有一定限制，例如 2MB 或者 8MB 等。
对于有 gc 的编程语言而言，无需关注内存分配与释放。
我的第一门语言是 Python ，再加上非计算机专业，没有系统学习过操作系统-内存管理相关知识，
因此对堆栈溢出问题的认识也仅停留在「知道它存在」的层面。

## 本次错误

一个项目中有一个检查文件 SHA256 哈希值的函数，我采用了分块读取文件，
这在 Python 中经过验证，也是推荐的做法。

但是运行程序时报错了：

```text
thread 'main' has overflowed its stack
```

因为函数里存在一个循环，退出条件是读取字节数小于块数。
我本能地以为是循环导致的栈溢出，网上搜索一番，没有解决。

突然想到，之前看过一个介绍 Rust 数据结构内存布局的视频
（[B站搬运](https://www.bilibili.com/video/BV1KT4y167f1) /
[油管原视频](https://www.youtube.com/watch?v=rDoqT-a6UFg)）
，介绍过 Rust 的栈空间是有限的。于是思考，是否因为分配的
buf 空间太大导致栈溢出？

```rust
let mut buf = [0u8; 1024 * 1024];
```

buf 分配了 `1024 * 1024` 字节，即 1MB 空间，我试着将其改为
`1024 * 4` 字节，即 4KB 空间，程序果然正常运行。

## 总结与后记

本次错误是分配了过大的 buf 导致栈空间不足溢出，得益于 Rust
友好的错误提示，很快定位错误并解决。

后面又尝试了用 C 语言分配大的 buf ，同样导致了栈溢出，
但是没有任何错误提示。

```c
#include<stdio.h>

void f() { char a[1024*1024*2]; }
int main() {
    printf("calling f ...\n");
    f();
    printf("ok\n");
}
```

Rust 是一门现代语言，是进步的语言，值得学习。
