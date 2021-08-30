from setuptools import setup, find_packages

VERSION = "1.0.0"

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
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    extras_require={
        "dev": [
            "black==21.8b0",
            "coveralls==3.2.0",
            "pylint==2.10.2",
            "pytest==6.2.4",
            "pytest-cov==2.12.1",
        ]
    },
    install_requires=[
        "libarchive-c==3.1",
        "requests>=2.26.0",
        "mwclient>=0.10.1",
    ],
)
