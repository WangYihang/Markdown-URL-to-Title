import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="u2t",
    version="1.0.2",
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
        "Development Status :: 5 - Production/Stable",
        "Topic :: Text Processing :: Markup :: Markdown",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    python_requires='>=3.6',
    keywords='markdown, url, editor',
    package_data={
        'u2t': [
            'resources/icon/normal.ico',
            'resources/icon/running.ico'
        ]
    },
    install_requires=[
        "system_hotkey",
        "clipboard",
        "requests",
        "bs4",
        "infi.systray",
        "win10toast",
    ],
    entry_points={
        'console_scripts': [
            'u2t=u2t:main',
        ],
    },
)
