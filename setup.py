from setuptools import setup, find_packages


setup(
    name='boteweber-backend',
    packages=find_packages(),
    author='Adrian Richter',
    install_requires=[
        'flask',
        'flask-cors',
        'jsonschema',
        'strict-rfc3339',  # date-time format validation
        'python-dateutil',
        'mysql-connector-python'
    ],
    entry_points={
        'console_scripts': [
            'boteweber-backend = src.main:main'
        ]
    }
)
