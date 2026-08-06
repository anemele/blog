---
title: Julia 编程语言安装教程
date: 2023-12-26
lastmod: 2026-08-06T23:00:28+08:00
tags:
 - Julia
 - installation
categories: computer
---

## Linux/Windows

[Julia](https://julialang.org/) 是一门新生的科学计算编程语言，拥有动态语言的方便与静态语言的性能。

安装 Julia 推荐使用包管理器 [juliaup](https://github.com/JuliaLang/juliaup/releases/latest) ，
并按照以下几个步骤配置镜像。

1. 下载 juliaup 程序，解压并将路径放置在 PATH
2. 设置 mirror ，即设置环境变量 `JULIAUP_SERVER` [^juliaup-mirror]
3. 使用 juliaup 安装 Julia
4. 配置 Julia 镜像

juliaup mirror 可以参考 [jill](https://github.com/johnnychen94/jill.py/blob/master/jill/config/sources.json)，
可以设置永久变量，也可以设置临时变量，例如

```bash
# linux
export JULIAUP_SERVER=https://mirrors.nju.edu.cn/julia-releases
```

```batch
@REM Windows
set JULIAUP_SERVER=https://mirrors.nju.edu.cn/julia-releases
```

Julia 包镜像

```julia
# ~/.julia/config/startup.jl
ENV["JULIA_PKG_SERVER"] = "https://mirrors.nju.edu.cn/julia"
```

## Termux

Termux 官方仓库没有提供 Julia，但是提供了 glibc，可以通过补丁使用 Julia for Linux[^参考文章]。

> proot 也是一种方法，但是性能较差，不推荐使用。

首先安装 glibc

```bash
pkg update && pkg upgrade
pkg install glibc-repo
pkg install glibc glibc-runner
```

然后下载并解压 Julia 包，注意按实际情况修改版本、CPU arch 等

```bash
set -ue

ver='1.12.6'
# wget "https://julialang-s3.julialang.org/bin/linux/aarch64/${ver%.*}/julia-$ver-linux-aarch64.tar.gz"
wget "https://mirror.tuna.tsinghua.edu.cn/julia-releases/bin/linux/aarch64/${ver%.*}/julia-$ver-linux-aarch64.tar.gz"
tar -xzf "julia-$ver-linux-aarch64.tar.gz"
```

接着是关键：**打补丁**

```bash
set -ue

JULIA_DIR='./julia-1.12.6'
JULIA_LIBEXEC="$JULIA_DIR/libexec/julia"

GLIBC_LIB="/data/data/com.termux/files/usr/glibc/lib"
GLIBC_LD="$GLIBC_LIB/ld-linux-aarch64.so.1"

patchelf --set-interpreter "$GLIBC_LD" \
         --set-rpath '$ORIGIN/../lib:$ORIGIN/../lib/julia:'"$GLIBC_LIB" \
         "$JULIA_DIR/bin/julia"

for tool in zstd 7z dsymutil lld; do
    if [ -f "$JULIA_LIBEXEC/$tool" ]; then
        patchelf --set-interpreter "$GLIBC_LD" \
                 --set-rpath '$ORIGIN/../../lib/julia:'"$GLIBC_LIB" \
                 "$JULIA_LIBEXEC/$tool"
    fi
done
```

最后是设置启动器，创建一个 `julia` 文件，添加 x 权限，写入以下内容，注意修改路径。

```bash
#!/usr/bin/bash
unset LD_PRELOAD
exec "path/to/julia-1.12.6/bin/julia" "$@"
```

[^juliaup-mirror]: https://github.com/JuliaLang/juliaup?tab=readme-ov-file#juliaup-server
[^参考文章]: https://zhuanlan.zhihu.com/p/2037295509367411091
