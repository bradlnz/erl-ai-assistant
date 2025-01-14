from setuptools import setup, find_packages

setup(
    name="autocodegeneraterl",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "gitpython",
        "openai",
        "flask",
        "rich",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "ai_creator=src.main:main",
        ],
    },
    author="Bradley Lietz",
    description="A tool for automating code generation and GitHub management.",
)
