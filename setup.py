from setuptools import setup, find_packages

setup(
    name="llmint",
    version="0.0.4",
    description="Llmint python library",
    author="Llmint Team",
    author_email="silveryfu@gmail.com",
    license="Apache License, Version 2.0",
    packages=find_packages(exclude=("tests",)),
    python_requires='>=3.10',
    include_package_data=True,
    install_requires = open('requirements.txt').readlines(),
)
