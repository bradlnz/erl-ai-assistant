from setuptools import setup, find_packages

setup(
    name="erl_code_generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "gitpython",
        "openai",
        "flask",
        "rich",
        "colorama",
        "flasgger"
    ],
    entry_points={
        "console_scripts": [
            "erl_code_generator=src.main:main",
        ],
    },
    author="Bradley Lietz",
    description="A tool for automating code generation and GitHub management.",
)
