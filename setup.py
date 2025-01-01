from setuptools import setup, find_packages

setup(
    name='fastmobile',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['python-fasthtml'],
    author='Umer Adil and contributors',
    author_email='umer.hayat.adil@gmail.com',
    description='FastHTML, but for mobile',
    url='https://github.com/umerha/fastmobile',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
