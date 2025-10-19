#!/usr/bin/env python3
"""
Setup script for Talkscriber Python Client Package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from pyproject.toml
def read_requirements():
    """Read requirements from pyproject.toml dependencies"""
    return [
        "numpy>=1.21.0",
        "scipy>=1.7.0", 
        "ffmpeg-python>=0.2.0",
        "PyAudio>=0.2.11",
        "websocket-client>=1.6.0",
        "websockets>=11.0.0",
        "loguru>=0.7.0",
    ]

setup(
    name="tsclient",
    version="1.0.0",
    author="Talkscriber",
    author_email="support@talkscriber.com",
    description="Python client library for Talkscriber Live Transcription and Text-to-Speech services",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Talkscriber/ts-client",
    project_urls={
        "Documentation": "https://docs.talkscriber.com",
        "Dashboard": "https://app.talkscriber.com",
        "Website": "https://talkscriber.com",
        "Bug Reports": "https://github.com/Talkscriber/ts-client/issues",
        "Source": "https://github.com/Talkscriber/ts-client",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    entry_points={
        "console_scripts": [
            "talkscriber-stt=talkscriber.stt.cli:main",
            "talkscriber-tts=talkscriber.tts.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="talkscriber, speech-to-text, text-to-speech, transcription, tts, stt, websocket, real-time",
)
