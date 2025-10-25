import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbot-command",
    version="1.1.2",
    author="Gregory Raiz",
    author_email="",
    py_modules=['cbot'],
    install_requires=['openai>=2.0.0', 'pyperclip'],
    description="Cbot is a command line assistant powered by GPT-5-mini with interactive shell mode.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/graiz/cbot/",
    project_urls={
        "GitHub": "https://github.com/graiz/cbot/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
    keywords='terminal cbot openai gpt5-mini chatgpt interactive-shell command-line-assistant',
    entry_points={
                        'console_scripts': [
                                'cbot=cbot:main',
                        ]
                }
)