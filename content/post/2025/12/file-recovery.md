---
title: 记一次文件误删
description: 昨天误删了一个源码文件，这并不可怕，可怕的是在这个命令前还有两个命令……
date: 2025-12-21T13:44:07+08:00
lastmod: 2025-12-21T13:44:07+08:00
draft: false
tags:
- file recovery
- winfr
- git
- GitHub
categories:
- engineering
---

昨天误删了一个源码文件，cmd 执行 `del play.py`。
这并不可怕，可怕的是在这个命令前还有两个命令
`gh repo delete --yes composer` 和 `rd /s/q .git`。
这下是完全抹去了。啊啊啊！

<!--more-->

## WinFR

根据掌握的知识和经验，删除文件只是删除了文件控制块（类似进程控制块的一个数据结构，
用于记录元信息），真正的文件本体还是存放在磁盘某个角落，Windows 的 NTFS 是日志文件系统，
应该可以通过某种方法找回文件。

search the web 找到一个推荐 Windows File Recovery 的视频，这是微软推出的文件恢复工具，
只提供命令行界面。

我在几年前用过这个工具，大概是 2021 年 3 月左右，当时还是计算机小白。某次下载一个安装包，
现在回想可能是从 XX 软件园这类地方下载的，安装之后把记事本默认打开程序替换成一个叫做
「小黑记事本」的程序，好像还有其他捆绑操作，但是记不清了。我道坏了，这是中病毒了。
恐慌之余赶紧找解决方法，最终重装系统解决了。顺便提一下，Windows 早已支持「恢复系统」，
保留用户文件，只重装系统，不需要清空磁盘。一直到现在除了安装 Linux 我还没有清空过磁盘，
当然是在其他盘装的 Linux，Windows 所在磁盘至今未曾变动。

说回这个工具，简称 winfr。当时应该是重装系统后不知怎么误删文件了（考虑到是小白，这很正常嘛），
然后应该是找了很多恢复软件，但大多收费很高，或者恢复效果不行，后来就找到了 winfr。
虽然当时我还不习惯使用命令行界面，但它是微软出品，我给予很大的信任，努力学着使用。
结果十分意外，竟然毫无作用。我十分失望，卸载了 winfr，也卸载了大厂滤镜。
我逐渐明白，大厂也是草包，只有掌握在自己手里的数据才是自己的数据。

这次又遇到 winfr，我不禁回想起上次的不愉快情景。几年时间过去，我已经「住在」终端了，
日常使用计算机，视频音乐等娱乐以外，除了浏览器就是终端，我已经熟练使用命令行程序了。
几年前使用 winfr 的细节已经模糊，不知道是不是因为不熟悉导致用错了呢？
几年时间过去，winfr 会不会有了新发展呢？
正好又有恢复文件的需求，不妨试试。从 Microsoft Store 安装 winfr，很小的一个程序，一会就好了。
从微软商店安装的程序，尤其是命令行程序，安装完都不知道在哪里。
所幸有 everything，搜索 `winfr.exe` 找到它的路径，然后还要以管理员身份运行。
「不是内部或外部命令，也不是可运行的程序或批处理文件。」 以及「管理员身份运行」
这个两个问题就足以难倒小白，也不知道当初小白的我是怎么解决的😀。
这次使用 winfr，先查看文档和命令帮助 `path/to/winfr.exe /?`，用法很简单，
主要是 4 个参数：误删文件所在磁盘，想要恢复的位置，恢复模式，过滤规则。
我的文件是刚刚删除的，因此用默认的常规模式即可；据网上说法恢复位置和原盘不能相同；过滤规则支持 glob。
因此我的命令是 `path/to/winfr.exe D: C:\tmp\ /n play.py`。然而这个命令跑了很久，有几十分钟，
然后卡在 `Scanning disk: 99%` 没有任何反应了。查看任务管理器，占用 20% 左右的 CPU，说明它并未停止运行。
再次 search the web 找到很多网页，但是内容一模一样，洋洋洒洒列举好几条解决方法，都是毫无意义的空话，
最后推荐一个软件，毫无疑问就是广告。
我知道文件恢复的大概原理，所以不敢有太多操作，唯恐文件覆盖导致无法找回。
就这样从 19 点到 21 点，在 99% 等了大约两个小时，结果竟然是无法恢复。™的，这样岂不是白等了？
我冷静分析，可能是过滤规则太广泛了，D 盘有 1TB 空间，play.py 文件大约 1.8 KB。
于是我将规则改为 play.py 的绝对路径再试一次，™的又等了两个小时，等到 23 点多，还是无法找回。
我终于确认，winfr 就是废物，微软早已是阿三的形状了。
如果是删除一段时间甚至删除很久，或者是很大的文件，找回概率渺小，这怨不得人。
但是我的文件刚刚删除，而且还不到 2KB，扫描两个小时一无所获，这不是废物是什么！
没办法，数据丢失真的很痛苦。

这是一个按照规则用纯文本编写简谱，然后生成音频的项目，是我之前学习笛箫、
研究乐理时搞的，效果不错。这次是因为整理源码文件，发现这个仓库只有两个文件 composer.py 和 play.py，
有很多这样项目，源码很少、用到的库高度相似，我想把这些项目合并起来。
这没问题，经常翻新是好的。问题在于我的操作，还没有完成迁移合并，就急于删除旧的仓库。
以往的 Python 项目是 package 模式，源码都是存放在 `src` 目录，根目录只有
`pyproject.toml  uv.lock  README.md  .gitignore  .python-version` 这 5 个文件，一般不会误删，
即使误删也影响不大。这个项目图方便，没有用 package 模式，源码直接放在根目录。
以往删除 pyproject.toml 都会输入 p 然后两次 tab，因为 cmd 会先匹配 .python-version，其次才是 pyproject.toml。
巧的是这次有一个叫 play.py 的文件，按字母顺序排在 pyproject.toml 之前，习惯使然，两次 tab 加回车，然后就误删了……

## GitHub

现在怎么办呢？
一个办法是凭着记忆编写，大概功能我是记得的，但是细节可能要花些时间，因为涉及很多数组计算，很繁琐很麻烦。
另一个办法是看看能不能从 GitHub 恢复被删除的仓库。

说起 GitHub，国内网络问题导致 GitHub 连接不稳定（GitHub 是可以直连的，我从没有使用任何工具）。
根据我的经验，网络问题是 https 才有的，也就是 80/443 端口，使用 ssh 协议还没有遇到问题，一直很流畅。
当然浏览器只能用 https，所幸 GitHub 有一个 [cli 客户端（gh）](https://github.com/cli/cli)，在网络正常的时候配置好 ssh 密钥，
然后用 gh 登录，后面很多常规操作都可以用它完成，
例如创建仓库、仓库改名、改可见性、删除仓库、fork 仓库、release、workflow、pr 等等。
网页里删除仓库需要输入完整的仓库名（full_name），gh 也是，不过如果是在本地 git 仓库的根目录加上 `--yes` 执行就可以不输入直接删除。
（某次更新后，还是要求输入仓库名，只加 `--yes` 不行，必须显式 `gh repo delete owner/repo --yes` 才可以）

再说到恢复仓库，我记得几年前有一个叫 faker 的 js 库被删除，因为这个库的影响太大了，GitHub 使用技术手段尝试恢复。
当时的说法是 GitHub 的仓库一旦被删除就无法找回了，只能根据日志定位到服务器机箱，然后从磁盘恢复数据。
就是这个印象，导致我想到了但没有第一时间尝试从 GitHub 恢复仓库。

现在迫不得已，试试总没错。上网搜索一番，还真有方法。
首先找到官方文档
[Restoring a deleted repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/restoring-a-deleted-repository)
映入眼帘是是一个大大的紫色 `Important`

> You can only contact GitHub Support to restore a repository if you are on a paid GitHub plan.
> For more information about the different plans, see GitHub’s plans.

因为不抱希望，看到这么一个提示说只有付费用户才能恢复仓库，我直接关闭了文档。
然后漫无目的地翻看其他网页，某个网页的摘要给出一个路径： `settings -> Repositories -> Deleted repositories`
说是可以从这里恢复被删除的仓库。

哇，居然是真的！这个 URL 是 <https://github.com/settings/deleted_repositories>，页面有一段提示

> It may take up to an hour for repositories to be displayed here.
> You can only restore repositories that are not forks, or have not been forked.

下面就是被删除的仓库以及删除时间，每个条目右边就是恢复按钮。被删除的 composer 仓库就在最顶层，点击 `Restore` 恢复，然后克隆下来，文件终于找回了！

回头细看 GitHub 文档，才发现是我误解了，那个 `Important` 指的是 fork 的仓库。

> A deleted repository can be restored within 90 days, unless the repository was part of a fork network that is not currently empty.

> Who can use this feature?
>
> Anyone can restore deleted repositories that were owned by their own personal account.
> Organization owners can restore deleted repositories that were owned by the organization.

也就是任何被删除的仓库都可以在 90 天内恢复，fork 的仓库除外。文档介绍了 fork 仓库，它是一个网状结构

> A fork network consists of a parent repository, the repository's forks, and forks of the repository's forks.

fork 仓库恢复需要联系 GitHub 支持，这要求是付费用户。

## 总结

至此，我的仓库恢复，文件找回，终于结束了这段痛苦。这段痛苦的经历，值得总结来提高信息安全意识。

很早我就研究过信息安全问题，包括理论方法以及工程手段，当然，都是很浅显的那种。

先来计算一下 1KB 空间可以存储多少不同的信息？这是很简单的组合数学，答案是 `2^8196`，换算成十进制数字，指数部分就是 `8196*log10(2)`，约等于 `2467`。
单单 1KB 空间就存在约 `10^2467` 种不同的信息，这是十分庞大的数字。那么 1MB、1GB 会是多少呢？答案分别是大约 `10^2525222` 和 `10^2585827972`，
这些数字都超乎想象。

我们的数据是从这近乎无穷多可能里面「选取」一种，如果想要依靠枚举法找到它，几乎是不可能的。保证数据安全的**唯一可靠**方法就是**多备份**。

git 是一个伟大的工具，它本质是一个小型文件系统，用 git 备份文本文件如源代码、文档、脚本等是天然合适的，当然二进制文件也是可以的。
本地 git 仓库和远端 git 仓库如 GitHub 结合使用，再加上 work tree，三重冗余，应对大多场景是足够的。
我这次事故就是先删除远端仓库，再删除本地仓库，然后误删 work tree，整好把冗余全部删除了。
另外 git 是分布式系统，多设备可以多仓库，又是一重备份，这样的系统强大到难以消灭。

无论再精妙的方法，再强的检错纠错能力，都不如多重冗余的工程实践。
单一系统的防护能力无论如何也无法达到 100%，如果有人声称他的系统是百分百安全，那么他本人一定不安全。
与其执着提升单一系统的强度，不如增加冗余，冗余增加成本但降低风险，成本风险权衡，冗余是符合实际的。

这在密码安全领域也符合实际，再先进的密钥系统，只要不能从用户根本上做出区分，理论上都是不安全的。
单一系统只认密钥，不认用户。例如真用户忘记密钥，假用户获得密钥，系统是难以辨别的。
工程上的做法是多重认证，这就是冗余，冗余增加用户认证成本，但是降低了整体风险：
一旦假用户通过系统认证，造成的损失是无法估计的。

最后做出总结：信息安全是相对安全，绝对安全是不可能的。
理论给出安全的边界，工程上逼近这个边界。

关于如何解决文件丢失的问题，有三点原则：

1. 多备份
2. 多用回收站，少用 del rm
3. 数据变动完成前不能删除，留个退路

预防丢失，而不是丢失之后痛哭流涕。

EOF