from setuptools import setup
import importlib

prereqs = ['clippyr']

if importlib.util.find_spec('PySide2') == None:
    prereqs.append('PySide2')

setup(
    name='qlippyr',
    version='0.1',
    py_modules=['qlippyr'],
    install_requires=prereqs,
    entry_points='''
        [console_scripts]
        qlippyr=qlippyr:main
    ''',
)
