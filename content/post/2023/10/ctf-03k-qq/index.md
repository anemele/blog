---
title: CTF - 零散坑 QQ 号获取
date: 2023-10-25
lastmod: 2024-12-15
tags:
 - ctf
 - 03k
categories: ctf
---

## 前言

查找 Windows 10 激活教程过程中发现了一个网站：[零散坑](https://www.03k.org)。
访问该网站，发现是大佬建立的博客站，顺便提供了 kms 服务。
博客下方是 QQ 群，但是要通过[谜题](https://blog.03k.org/q.html)才能获得群号。
这算是人机验证的一种方式？实际上也劝退了很多小白。

<!--more-->

## 正文

目前有 4 道题目：

第一题给出了一张“神秘纸条”，内容是：`txt , GetNum.03k.org`

![](q1.jpeg)

第二题给出一张黑白图片，像素分辨率，内容是一个相机，下面是文字 `images.zip`。

![](q2.jpeg)

第三题是无奖竞猜。

![](q3.jpeg)

第四题是方块游戏。

![](qg.jpeg)

第一题完全没有头绪，放弃。

第二题看到文字提示，下意识想到“图种”，于是下载该图片，得到 `what.png`[^what.png]，过程后叙。

第三题有一个 `群号：*********` 的提示，首先想到是前端掩码，但是打开调试器并没有发现有用信息。

第四题是个有趣的游戏，但越玩难度越大，最大尝试玩到 512 就失败了，目标是 4096。提示“欢迎作弊”，猜测是前端破解。

最终是通过第二题获取了群号，思路和过程如下：

根据提示信息 `images.zip`，该图片可能是图种文件，即将图片和压缩包按字节拼接成的文件。一般是方法是改后缀名为 `.zip`，用压缩软件直接打开，但是失败了，提示“无法作为压缩包打开文件”。于是查看字节码，查找 zip 文件头 `PK`，一共找到 4 个。从第一个 PK 到文件尾复制字节码，保存为新文件 `what.zip`[^what.zip] ，再用压缩软件可以正常打开，内部有一个名为 `six digital.txt` 的文件。解压该文件提示需要密码，根据文件名猜测是个 6 位数字密码，猜测 666666、123456、888888、000000 等等，都以失败告终。然后灵机一动，6 位数字密码是可以爆破的，然后用 Python 编写程序尝试。

```python
import zipfile

z = zipfile.ZipFile("what.zip")
for x in range(1000000):
    pwd = bytes(f"{x:06d}", "ascii")
    try:
        z.extractall(pwd=pwd)
        print(x)
    except RuntimeError:
        pass
```

中间遇到一次错误： `zlib.error: Error -3 while decompressing data: invalid stored block lengths`，以为是压缩包有问题。考虑到图种里有 4 个 `PK`，可能存在压缩包混淆，将其余 3 个以同样的方式保存到新的文件，分别命名 `what2.zip`[^what2.zip] `what3.zip`[^what3.zip] `what4.zip`[^what4.zip] ，但是这 3 个文件都不能用压缩软件打开。

回到第一个文件，修改 except 捕获所有异常： `except Exception`
。运行一小会，程序输出了 114514 后继续运行。赶紧 CTRL+C 终止程序，看来密码就是这串数字了。再次用压缩软件打开压缩包，输入密码查看文件，果然成功，顺利获得群号。

文件内容：

```text
Congratulations!
QQ Group: 170776629
```

完善程序

```python
import zipfile

z = zipfile.ZipFile("what.zip")
for x in range(1000000):
    x = f"{x:06d}"
    try:
        z.extractall(pwd=x.encode())
    except Exception:
        continue
    print(x)
    break
else:
    raise RuntimeError
```

## 补充

把群号输入问题三，果然猜测正确。用调试器定位猜测按钮的事件回调函数，发现里面并没有明文给出群号，而是用 `qqgroup` 作为 salt 判断猜测群号的 MD5 与给定的是否一致。从哈希值反推明文可是十分困难的，也许从在线查询 MD5 网站可以获得结果，但尝试了一些，都失败了。

考虑到 QQ 号是 9 位数字，也可以用爆破方法计算，参考程序

```python
# raise DeprecationWarning("计算成功需要耗费几分钟，仅作参考。")
import hashlib

target = "307bff0333b2b42af8620f2295022fe3"


def f(x):
    return hashlib.md5(f"qqgroup{x}".encode()).hexdigest()


for i in range(100000000, 1000000000):
    if f(i) == target:
        print(i)
        break
else:
    raise RuntimeError
```

## 附件

[^what.png]: [附件：what.png](what.png)
[^what.zip]: [附件：what.zip](what.zip)
[^what2.zip]: [附件：what2.zip](what2.zip)
[^what3.zip]: [附件：what3.zip](what3.zip)
[^what4.zip]: [附件：what4.zip](what4.zip)
