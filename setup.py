"""
Setup configuration for DashboardAGTorroni package.

This setup file allows for proper installation and distribution of the dashboard application
for agricultural data visualization and analysis.
"""

from setuptools import setup, find_packages

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="DashboardAGTorroni",
    version="1.0.0",
    author="GIACOMO CROCIANI",
    author_email="",
    description="Interactive dashboard for agricultural production and sales analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/giacomocrociani/DashboardAGTorroni",
    project_urls={
        "Bug Tracker": "https://github.com/giacomocrociani/DashboardAGTorroni/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "dash>=2.0.0",
        "plotly>=5.0.0",
        "dash-bootstrap-components>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "torroni-dashboard=__init__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.csv", "data/MeteoCetona2024/*.csv"],
    },
    zip_safe=False,
)