from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cottonmouth',
    version='0.2.1',
    description='Pure-Python HTML generation',
    long_description=readme,
    author='Noah Seger',
    author_email='nosamanuel@gmail.com.com',
    url='https://github.com/nosamanuel/cottonmouth',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    test_suite='tests',
)
