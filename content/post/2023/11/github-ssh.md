---
title: GitHub 添加 ssh 公钥
description: ssh 密钥
date: 2023-11-22
lastmod: 2026-01-08T17:22:29+08:00
tags:
 - ssh
 - git
 - github
categories: computer
---

托管在 GitHub 上的远程 git 仓库，如果需要敏感操作会要求输入密码，这一不安全，二不方便。
解决方法是使用 ssh 密钥。

一般操作系统都带有 OpenSSH 工具，如果没有先行安装。之后执行以下命令生成 ssh 密钥对

```bash
ssh-keygen -t rsa -C "your_name@example.com"
# 之后有三步输入，第一步可以设置密钥对名字（默认 id_rsa），其余两步可以跳过。

cat ~/.ssh/id_rsa.pub # 带 pub 后缀的才是公钥！
```

进入 <https://github.com/settings/keys> 找到 `SSH keys`，点击 `New SSH key`，
将公钥内容复制粘贴完成。

之后就可以使用 SSH 协议推拉仓库了，例如原先是 `https://github.com/xx/yy`，可以改用
`git@github.com:xx/yy`。

另外，如果需要多平台配置密钥，需要添加对应的配置，例如 gitlab

```text
Host github.com
User git
HostName ssh.github.com
Port 22
IdentityFile ~/.ssh/id_rsa

Host gitlab.com
User git
HostName gitlab.com
Port 22
IdentityFile ~/.ssh/id_rsa_gitlab
```
