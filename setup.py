from setuptools import setup, find_packages

setup(
    name="tsclient",
    version="0.1.3",
    author="Talkscriber",
    author_email="info@talkscriber.com",
    description="Talkscriber Python Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Talkscriber/ts-client",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "ffmpeg-python==0.2.0",
        "numpy>=1.22.3,<1.23.0",
        "PyAudio==0.2.11",
        "scipy>=1.8.0,<1.11.0",
        "websocket-client==1.6.0",
    ],
)
