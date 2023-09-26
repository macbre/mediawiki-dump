from setuptools import setup, find_packages

VERSION = "1.2.0"

# @see https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
with open("README.md", "r") as fh:
    long_description = fh.read()

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name="mediawiki_dump",
    version=VERSION,
    author="Maciej Brencz",
    author_email="maciej.brencz@gmail.com",
    license="MIT",
    description="Python package for working with MediaWiki XML content dumps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="dump fandom mediawiki wikipedia wikia",
    url="https://github.com/macbre/mediawiki-dump",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Markup :: XML",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    extras_require={
        "dev": [
            "black==23.9.1",
            "coveralls==3.3.1",
            "pylint==2.17.6",
            "pytest==7.4.2",
            "pytest-cov==4.1.0",
            "responses==0.23.3",
        ]
    },
    install_requires=[
        "libarchive-c==5.0",
        "requests>=2.26.0",
        "mwclient>=0.10.1",
    ],
)
