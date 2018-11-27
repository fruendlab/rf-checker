from setuptools import setup


def parse_requirements():
    with open('requirements.txt') as f:
        return f.readlines()


setup(
    name='check_rf',
    version='1.0',
    author='Ingo Fruend',
    install_requires=parse_requirements(),
)
