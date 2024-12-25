from setuptools import setup

setup(
    name="ts_live",
    version="0.1.0",
    packages=["ts_live"],
    install_requires=[
        "websocket-client>=1.6.0",
        "numpy>=1.22.3,<1.23.0",
        "PyAudio==0.2.11",
        "pydantic>=2.0.0",
        "scipy>=1.8.0",
        "ffmpeg-python>=0.2.0",
    ],
)