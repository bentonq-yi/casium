from setuptools import setup

setup(
    name='casium',
    version='1.0.0',
    author='bentonq',
    author_email='bentonq@163.com',
    url='https://github.com/bentonq-yi/casium',
    description='A simple python module for auto ui-test using appium and uiautomator2.',
    packages=['casium'],
    install_requires=[
        'Appium-Python-Client',
        'pytest',
        'openpyxl',
        'cached-property',
        'pyinstaller',
        'numpy'
    ]
)
