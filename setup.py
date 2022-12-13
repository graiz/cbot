import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cbot-command",
    version="1.0.3",
    author="Gregory Raiz",
    author_email="",
    requirements=['openai', 'pyperclip'],
    install_requires=['openai', 'pyperclip'],
    description="Cbot is a simple python command line bot based on GPT3.",
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
    keywords ='terminal cbot openai gpt3 chatgpt',
    entry_points={
                        'console_scripts': [
                                'cbot=cbot:main',
                        ]
                }
)