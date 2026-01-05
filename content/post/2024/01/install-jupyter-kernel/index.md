---
title: 安装 Jupyter kernel
date: 2024-01-06
lastmod: 2026-01-05T18:13:43+08:00
tags:
 - jupyter
categories: computer
image: Jupyter.svg
---

Jupyter 是一个交互式编程工具。

<!--more-->

Jupyter 是使用 Python 开发的 Web 程序，最初为了支持 Python 在科学计算方面的应用，
之后开发人员为 Jupyter 添加了很多内核，使其可以支持更多编程语言，具体参考
<https://github.com/jupyter/jupyter/wiki/Jupyter-kernels>。

## 安装 Jupyter

~~早期的 Jupyter 环境是 notebook ，现在推荐使用 lab 。~~

~~jupyter 默认环境浏览器体验较差，推荐使用 vscode + jupyter 插件，集成了 jupyter 程序，只需提供 jupyter kernel。~~

更新：当前最佳实践是，使用 uv 管理一个「全局」虚拟环境，将 jupyter 作为 dev 依赖。例如

```bash
uv init pyenv-scic
cd pyenv-scic
uv add --dev jupyter jupyterlab nbformat anywidget
uv add numpy scipy sympy matplotlib plotly pandas
```

> 这里区分一下 jupyter 和 jupyter kernel，二者是不一样的概念：
> jupyter 是一个 web 程序，提供了交互功能，更多的是指前端内容。
> 而 jupyter kernel 是后端服务，任何实现 jupyter kernel 接口的程序都可以作为 jupyter kernel 使用。
> 例如 Python 的 ipykernel，Julia 的 IJulia 等等。

~~首先要有 Python 环境（可以创建一个虚拟环境），使用 pip 安装~~

```bash
pip install jupyterlab
```

~~等待安装完成。~~
~~jupyterlab 自带一个默认的 Python 内核，名为 `ipykernel` 。~~

## 内核操作

### 列出内核

```bash
jupyter kernelspec list
```

### 删除内核

```bash
jupyter kernelspec remove {name}
```

### 安装内核

#### Python

（创建一个虚拟环境）

```bash
pip install ipykernel
python -m ipykernel install --user --name {} --display-name {}
```

这个方法是全局安装 kernel，方便 jupyter 检测。另外可以在当前环境安装，vscode 可以直接使用。
推荐使用 `uv` 作为项目管理工具：

```bash
uv add --dev ipykernel nbformat
```

#### Julia

```julia
using Pkg
Pkg.add("IJulia")
using IJulia
installkernel("Julia")
```

#### R

```r
install.packages('devtools', type='binary')
devtools::install_github('IRkernel/IRkernel')
```
or
```r
install.packages('IRkernel')
IRkernel::installspec()
```
