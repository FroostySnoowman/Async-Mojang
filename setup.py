from setuptools import setup, find_packages

setup(
    name="async-mojang",
    version="1.0.3",
    author="FroostySnoowman",
    description="An async Python wrapper for the Mojang API.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FroostySnoowman/Async-Mojang",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    license="MIT",
    python_requires=">=3.7",
    install_requires=[
        "aiohttp",
    ],
    keywords=["mojang", "minecraft", "api", "mojang api", "minecraft api", "async mojang", "async minecraft"],
)