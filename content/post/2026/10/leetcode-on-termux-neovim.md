---
title: Leetcode on Termux Neovim
description:
date: 2026-10-16T06:35:55Z
lastmod: 2026-10-16T06:35:55Z
# image:
tags:
- Leetcode
- termux
- Neovim
- cookie
- GitHub
categories: Termux
math:
hidden: false
draft: false
---

在室外偶然想要写点算法题玩玩，只带了手机，Leetcode 确实有移动端 App，但是编辑体验不好，于是思考 termux 解决方案：我已经熟练使用 termux 一年多了。

vscode 有一个 Leetcode 插件，neovim 呢？搜索一下，果然有一个 <https://github.com/kawre/leetcode.nvim>，同时找到一篇经验分享 <https://leetcode.cn/discuss/post/3675554/>，恰好是同样的思路。我根据自己情况做出调整，补充遇到的问题以及解决方法。

`kawre/leetcode.nvim` README 提供十分详细的安装配置教程，跟着一步一步来很快安装成功。

登录 Leetcode 需要提供 cookie，安卓浏览器不提供 devtools，只能另寻他法。那篇分享使用一个第三方浏览器的扩展程序获取 cookie，我使用的 edge 浏览器同样支持扩展程序，搜索添加插件 `Cookie-Editor` 解决。

**坑一**：插件显示几十条 cookie，不知道使用哪个，leetcode.nvim 没有提示输入格式，只是一味地报错：
`bad csrf token format`，搜索 issue 解决：[#160](https://github.com/kawre/leetcode.nvim/issues/160#issuecomment-3214503406)，
格式为 `csrftoken=***;LEETCODE_SESSION=***`

**坑二**：登录成功后一直「加载中」，报错 `curl: (23) Failed writing received data to disk/application`，搜索 issue 解决：[#88](https://github.com/kawre/leetcode.nvim/issues/88#issuecomment-2051042669)，设置环境变量 `export XDG_RUNTIME_DIR=$TERMUX__PREFIX/tmp`

---

可以愉快地写算法题啦！
