from setuptools import setup

setup(
    name="tcmg476",
    version='0.1',
    py_modules=['groupcli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tcmg476=groupcli:cli
    ''',
)
