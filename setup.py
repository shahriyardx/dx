from pathlib import Path

from setuptools import find_packages, setup

current_directory = Path(__file__).parent.resolve()


def _get_requirements() -> list:
    with open(current_directory / "requirements.txt") as f:
        return f.read().splitlines()


def _get_long_desc() -> str:
    return (current_directory / "README.md").read_text(encoding="utf-8")


setup(
    name="dx",
    version="0.0.1",
    description="utility tools",  # Optional
    long_description=_get_long_desc(),
    long_description_content_type="text/markdown",
    url="https://github.com/shahriyardx/dx",
    author="Md Shahriyar Alam",
    author_email="contact@shahriyar.dev",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=_get_requirements(),
    extras_require={
        "dev": ["black", "isort", "click", "twine"],
    },
    project_urls={
        "Bug Reports": "https://github.com/shahriyardx/dx/issues",
        "Source": "https://github.com/shahriyardx/dx/",
    },
    entry_points={"console_scripts": ["dx = src:dx"]},
)
