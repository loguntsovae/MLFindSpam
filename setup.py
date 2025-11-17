"""
SMS Spam Classifier - Setup Configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="sms-spam-classifier",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A machine learning project for SMS spam classification",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/spam_classifier",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "spam-classifier=src.predict:main",
        ],
    },
    include_package_data=True,
    keywords="spam classification machine-learning nlp sms text-classification",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/spam_classifier/issues",
        "Source": "https://github.com/yourusername/spam_classifier",
        "Documentation": "https://github.com/yourusername/spam_classifier/blob/main/README.md",
    },
)
