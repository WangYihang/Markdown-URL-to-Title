import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="u2t",
    version="0.0.1",
    author="Wang Yihang",
    author_email="wangyihanger@gmail.com",
    description="A tool helps to convert url to markdown style url format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WangYihang/Markdown-URL-to-Title",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Markup :: Markdown",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    python_requires='>=3.6',
)