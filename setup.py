from setuptools import setup, find_packages
from distutils.core import setup

setup(
    name='ubm',
    packages=find_packages(),
    version='v1.0.0',
    description='Library for UniBo Motorsport data analysis',
    author='Aaron Russo',
    author_email='axolo6@gmail.com',
    url='https://github.com/Ax6/ubm-python-libraries',  # use the URL to the github repo
    download_url='https://github.com/Ax6/ubm-python-libraries/archive/v1.0.0.tar.gz',
    classifiers=[],
    install_requires=[
        'numpy',
        'scipy',
        'pandas'
    ],
)
