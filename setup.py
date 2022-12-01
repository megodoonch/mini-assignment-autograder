# based on https://github.com/sodascience/metasynth - MIT License
from pathlib import Path
from setuptools import setup, find_packages

# import versioneer


readme_path = Path(__file__).parent.absolute() / "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='autograder',
    version="0.1.0",   #versioneer.get_version(),
    # cmdclass=versioneer.get_cmdclass(),
    author='Meaghan Fowlie',
    description='Package for creating autograded mini python assignments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['data', 'docs', 'tests', 'examples']),
    # package_data={"metasynth": ["py.typed"]},
    # include_package_data=True,
    python_requires='~=3.8',
    install_requires=[
        "nltk",
        "pandas",
        "polars>=0.14.17",
        "pyarrow",  # Dependency of polars since we're converting from pandas.
        "scipy",
        "numpy>=1.20",
        "faker",
        "scikit-learn",
        "xmltodict",
        "jsonschema",
        "importlib-resources;python_version<'3.9'",
        "wget",
    ],
    entry_points={
        'metasynth.disttree': [
            "builtin = metasynth.disttree:BuiltinDistributionTree",
        ]
    }
)
