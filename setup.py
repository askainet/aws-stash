# coding: utf-8

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-stash",
    setup_requires=['setuptools_scm'],
    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'dirty-tag'
    },
    author="Ivan Lopez",
    author_email="ivan@askai.net",
    description="Manage AWS Parameter Store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askainet/aws-stash",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'aws-stash = aws_stash.__main__:main',
        ],
    },
    install_requires=[
        'boto3>=1.7.38',
        'pyperclip==1.6.4'
    ]
)
