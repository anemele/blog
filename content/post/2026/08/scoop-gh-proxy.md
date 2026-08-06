---
title: Scoop GitHub Proxy
description:
date: 2026-08-06T23:53:28+08:00
lastmod: 2026-08-06T23:53:28+08:00
# image:
tags:
- scoop
- GitHub
- PowerShell
- git
categories: Computer
math:
hidden: false
draft: false
---

Scoop 安装某些 GitHub release 包很慢，好在它用 PowerShell 编写，可以修改源码，添加镜像源。

编辑 `~\scoop\current\lib\download.ps1`，在 `function Invoke-Download` 里面添加以下代码

```pwsh
$github_mirror = "https://edgeone.gh-proxy.org/"
$github_prefixes = @("https://github.com/", "https://raw.githubusercontent.com/")
if ($github_prefixes | Where-Object { $url.StartsWith($_) }) {
	$url = $github_mirror + $url
}
Write-Host "[DEBUG] url=$url"
```

因为 scoop 经常更新，最好设置 git rebase

```bash
git config --add user.name a
git config --add user.email a
git config --add pull.rebase true
```

然后提交一次

```bash
git add .
git commit -m "add github mirror"
```
