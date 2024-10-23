from setuptools import setup, find_packages

def read_readme() -> str:
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

setup(
    name="InternetSpeedTest",
    version="1.0",
    author="Jin-Mach",
    author_email="Ji82Ma@seznam.cz",
    description="A simple text editor designed for productive work with basic formatting options.",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jin-Mach/TextEditor",
    packages=find_packages(),
    install_requires=[
        "PyQt6>=6.7.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "text_editor=text_editor:main",
            ],
        },
    keywords="text_editor, pyqt6",
)