from setuptools import setup, find_packages


setup(
    name='boteweber-backend',
    packages=find_packages(),
    author='Adrian Richter',
    install_requires=[
        'flask',
        'flask-cors',
        'mysql-connector-python'
    ]
)