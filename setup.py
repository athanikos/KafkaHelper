import setuptools
from distutils.core import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='KafkaHelper-athanikos',
    version="0.1.2",
    license='MIT License',
    author='Nikos Athanasakis',
    packages=setuptools.find_packages(),
    author_email='athanikos@gmail.com',
    description='A set of helper to produce / consume from / to kafka (uses kafka-python)',
    tests_require=['pytest'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
