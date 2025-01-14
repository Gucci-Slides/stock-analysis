# services/data_collector/setup.py
from setuptools import setup, find_packages

setup(
    name="stock-data-collector",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "yfinance",
        "opensearch-py",
        "boto3",
    ],
)