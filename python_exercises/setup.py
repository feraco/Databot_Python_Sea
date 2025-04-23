from setuptools import setup, find_packages

setup(
    name="databot_exercises",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "bleak>=0.14.0",
        "bottle>=0.12.19",
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
    ],
    description="Python exercises for Databot underwater ROV",
    author="Databot Team",
    author_email="info@databot.us.com",
    url="https://github.com/feraco/Databot_Python_Sea",
)