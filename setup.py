"""
Setup script para o Sistema de Controle de Perdas
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sistema-controle-perdas",
    version="1.0.0",
    author="Seu Nome",
    author_email="seu.email@empresa.com",
    description="Sistema completo para controle de perdas de gadgets e monitoramento",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/sistema-controle-perdas",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950"
        ]
    },
    entry_points={
        "console_scripts": [
            "sistema-controle=app:main",
        ],
    },
)
