---
title: SHA1 碰撞
description: 2017 年谷歌发布一篇文章公布了首个 SHA1 碰撞案例……
date: 2023-05-20T05:56:49+08:00
tags:
 - SHA1
 - Hashsum
 - shattered
categories: cryptography
---

2017 年，谷歌发布一篇[文章](https://shattered.io/static/shattered.pdf)，
公布了首个 SHA1 碰撞案例，即两个不同的文件拥有相同的 SHA1 值。

文章只有二十多页，但我不了解密码学，没有阅读和研究，只是关心文末提供的碰撞样本，
它是一段 base64 编码，按照文章提示保存为文件，然后执行两条命令就可以得到样本 PDF 文件

```bash
base64 --decode coll.tar.bz2.b64 > coll.tar.bz2
tar -xvf coll.tar.bz2
```

为了方便写了一段 Python 程序

```python
import base64
import hashlib
import io
import tarfile

data = """QlpoOTFBWSZTWbL5V5MABl///////9Pv///v////+/////HDdK739/677r+W3/75rUNr4Aa/AAAAAAA
CgEVTRtQDQAaA0AAyGmjTQGmgAAANGgAaMIAYgGgAABo0AAAAAADQAIAGQ0MgDIGmjQA0DRk0AaMQ0D
QAGIANGgAAGRoNGQMRpo0GIGgBoGQAAIAGQ0MgDIGmjQA0DRk0AaMQ0DQAGIANGgAAGRoNGQMRpo0GI
GgBoGQAAIAGQ0MgDIGmjQA0DRk0AaMQ0DQAGIANGgAAGRoNGQMRpo0GIGgBoGQAAIAGQ0MgDIGmjQA0
DRk0AaMQ0DQAGIANGgAAGRoNGQMRpo0GIGgBoGQAABVTUExEZATTICnkxNR+p6E09JppoyamjGhkm0a
mmIyaekbUejU9JiGnqZqaaDxJ6m0JkZMQ2oaYmJ6gxqMyE2TUzJqfItligtJQJfYbl9Zy9QjQuB5mHQ
RdSSXCCTHMgmSDYmdOoOmLTBJWiCpOhMQYpQlOYpJjn+wQUJSTCEpOMekaFaaNB6glCC0hKEJdHr6Bm
UIHeph7YxS8WJYyGwgWnMTFJBDFSxSCCYljiEk7HZgJzJVDHJxMgY6tCEIIWgsKSlSZ0S8GckoIIF+5
51Ro4RCw260VCEpWJSlpWx/PMrLyVoyhWMAneDilBcUIeZ1j6NCkus0qUCWnahhk5KT4GpWMh3vm2nJ
WjTL9Qg+84iExBJhNKpbV9tvEN265t3fu/TKkt4rXFTsV+NcupJXhOhOhJMQQktrqt4K8mSh9M2DAO2
X7uXGVL9YQxUtzQmS7uBndL7M6R7vX869VxqPurenSuHYNq1yTXOfNWLwgvKlRlFYqLCs6OChDp0HuT
zCWscmGudLyqUuwVGG75nmyZhKpJyOE/pOZyHyrZxGM51DYIN+Jc8yVJgAykxKCEtW55MlfudLg3KG6
TtozalunXrroSxUpVLStWrWLFihMnVpkyZOrQnUrE6xq1CGtJlbAb5ShMbV1CZgqlKC0wCFCpMmUKSE
kvFLaZC8wHOCVAlvzaJQ/T+XLb5Dh5TNM67p6KZ4e4ZSGyVENx2O27LzrTIteAreTkMZpW95GS0CEJY
hMc4nToTJ0wQhKEyddaLb/rTqmgJSlkpnALxMhlNmuKEpkEkqhKUoEq3SoKUpIQcDgWlC0rYahMmLuP
Q0fHqZaF4v2W8IoJ2EhMhYmSw7qql27WJS+G4rUplToFi2rSv0NSrVvDUpltQ8Lv6F8pXyxmFBSxiLS
xglNC4uvXVKmAtusXy4YXGX1ixedEvXF1aX6t8adYnYCpC6rW1ZzdZYlCCxKEv8vpbqdSsXl8v1jCQv
0KEPxPTa/5rtWSF1dSgg4z4KjfIMNtgwWoWLEsRhKxsSA9ji7V5LRPwtumeQ8V57UtFSPIUmtQdOQfs
eI2Ly1DMtk4Jl8n927w34zrWG6Pi4jzC82js/46Rt2IZoadWxOtMInS2xYmcu8mOw9PLYxQ4bdfFw3Z
Pf/g2pzSwZDhGrZAl9lqky0W+yeanadC037xk496t0Dq3ctfmqmjgie8ln9k6Q0K1krb3dK9el4Xsu4
4LpGcenr2eQZ1s1IhOhnE56WnXf0BLWn9Xz15fMkzi4kpVxiTKGEpffErEEMvEeMZhUl6yD1SdeJYbx
zGNM3ak2TAaglLZlDCVnoM6wV5DRrycwF8Zh/fRsdmhkMfAO1duwknrsFwrzePWeMwl107DWzymxdQw
iSXx/lncnn75jL9mUzw2bUDqj20LTgtawxK2SlQg1CCZDQMgSpEqLjRMsykM9zbSIUqil0zNk7Nu+b5
J0DKZlhl9CtpGKgX5uyp0idoJ3we9bSrY7PupnUL5eWiDpV5mmnNUhOnYi8xyClkLbNmAXyoWk7GaVr
M2umkbpqHDzDymiKjetgzTocWNsJ2E0zPcfht46J4ipaXGCfF7fuO0a70c82bvqo3HceIcRlshgu73s
eO8BqlLIap2z5jTOY+T2ucCnBtAtva3aHdchJg9AJ5YdKHz7LoA3VKmeqxAlFyEnQLBxB2PAhAZ8Kvm
uR6ELXws1Qr13Nd1i4nsp189jqvaNzt+0nEnIaniuP1+/UOZdyfoZh57ku8sYHKdvfW/jYSUks+0rK+
qtte+py8jWL9cOJ0fV8rrH/t+85/p1z2N67p/ZsZ3JmdyliL7lrNxZUlx0MVIl6PxXOUuGOeArW3vuE
vJ2beoh7SGyZKHKbR2bBWO1d49JDIcVM6lQtu9UO8ec8pOnXmkcponBPLNM2CwZ9kNC/4ct6rQkPkQH
McV/8XckU4UJCy+VeTA=="""

tar_obj = io.BytesIO(base64.b64decode(data))
name_bytes = []
with tarfile.open(fileobj=tar_obj) as tar:
    for member in tar.getmembers():
        tf = tar.extractfile(member)
        if tf is None:
            continue
        name_bytes.append((member.name, tf.read()))

hashsum = [hashlib.sha1, hashlib.sha256]

for h in hashsum:
    for name, b in name_bytes:
        print(h(b).hexdigest(), name)
```

得到如下结果

```text
d00bbe65d80f6d53d5c15da7c6b4f0a655c5a86a good.pdf
d00bbe65d80f6d53d5c15da7c6b4f0a655c5a86a bad.pdf
298847a40440d3f9076c1c1cb4381a57c937cf8fc4de92815982a02c05b27e73 good.pdf
20055e76deb6f328e0d81020ee818eb5bcf3a6126b276c820338b4dce5407370 bad.pdf
```

EOF