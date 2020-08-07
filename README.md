# Markdown-URL-to-Title

本工具的功能为：自动提取剪贴板中的 URL ，然后使用 requests 获取目标 URL 的标题，根据标题生成可直接粘贴的 Markdown 内容。

## 背景

在使用 Hexo 写博客的时候，想给博文里插入一些参考文献，但是如果直接粘贴 URL 的话，
有的参考链接的 URL 非常长，而且会被 URL 编码，不太容易阅读，如下：
```
## 参考文献
* https://vi.stackexchange.com/questions/14114/paste-link-to-image-in-clipboard-when-editing-markdown
* https://c.m.163.com/news/a/FJ8PBOJ000097U7R.html?spss=adap_pc&referFrom=&spssid=592b2c22f7c667bdd783e7ef59625b86&spsw=1&isFromH5Share=article
```
所以就想着能不能为 Hexo 实现一个自动将 URL 转为 Markdown 带有标题文本的格式，也就是如下：
```
## 参考文献
* [Paste link to image in clipboard when editing Markdown - Vi and Vim Stack Exchange](https://vi.stackexchange.com/questions/14114/paste-link-to-image-in-clipboard-when-editing-markdown)
* [继微信封禁WeTool后 腾讯或大规模封禁第三方QQ机器人](https://c.m.163.com/news/a/FJ8PBOJ000097U7R.html?spss=adap_pc&referFrom=&spssid=592b2c22f7c667bdd783e7ef59625b86&spsw=1&isFromH5Share=article)
```
经过一番搜索暂时没有找到解决方案，没有办法，只好出此下策，使用 Python 来对剪切板进行操作，提取剪切板中的 URL 并转换为 Markdown 的格式。


## 环境需求
* Windows 10
* Python 3

## 例子

### 剪切板输入

```markdown
...
https://baidu.com/
...
```

### 剪切板输出

```markdown
...
[百度一下，你就知道](https://www.baidu.com/)
...
```

## 安装

```bash
git clone https://github.com/WangYihang/Markdown-URL-to-Title
```

## 使用方式
0. 运行：`cd Markdown-URL-to-Title; python u2t.py`，此时系统托盘出现图标
1. 复制待处理文本，不用特别精确地只复制 URL，本程序使用正则提取剪切板内容中的所有 URL 并进行批量处理
2. 按快捷键 Ctrl + Shift + Q
3. 等待数秒，待 Windows 弹出 Toast 提示框，即可直接进行粘贴
