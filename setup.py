from setuptools import setup, find_packages

setup(
    name="mmHomonymDisambiguator",
    version="0.1.0",
    author="Zar Zar Hlaing",
    author_email="zarzarhlaing.it@gmail.com",
    description="Myanmar Homonym Disambiguation system using n-gram probability model",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zar-zar-hlaing/mmHomonymDisambiguator",
    license="MIT",
    packages=find_packages(),
    py_modules=["mmHomonymDisambiguator"],
    python_requires=">=3.8",
    install_requires=[
        "regex>=2023.6.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Natural Language :: Burmese",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    include_package_data=True,
    package_data={
        "mmHomonymDisambiguator": [
            "myanmar_text_data/*.txt",
            "reference/*.pdf",
        ],
    },
    entry_points={
        "console_scripts": [
            "mmhomo=mmHomonymDisambiguator:main",
        ],
    },
)
