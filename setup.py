# based on https://github.com/sodascience/metasynth - MIT License
from pathlib import Path
from setuptools import setup, find_packages


readme_path = Path(__file__).parent.absolute() / "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='autograder',
    version="0.1.0",
    author='Meaghan Fowlie',
    description='Package for creating autograded mini python assignments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['data', 'docs', 'tests', 'examples']),
    python_requires='~=3.8',
    install_requires=[
        "nltk",
        "pandas",
        "importlib-resources;python_version<'3.9'",
    ],
)
