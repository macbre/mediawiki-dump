from setuptools import setup, find_packages

VERSION = '0.6.3'

# @see https://packaging.python.org/tutorials/packaging-projects/#creating-setup-py
with open("README.md", "r") as fh:
    long_description = fh.read()

# @see https://github.com/pypa/sampleproject/blob/master/setup.py
setup(
    name='mediawiki_dump',
    version=VERSION,
    author='Maciej Brencz',
    author_email='maciej.brencz@gmail.com',
    license='MIT',
    description='Python package for working with MediaWiki XML content dumps',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='dump fandom mediawiki wikipedia wikia',
    url='https://github.com/macbre/mediawiki_dump',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Text Processing :: Markup :: XML',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    extras_require={
        'dev': [
            'coverage==4.5.3',
            'pylint==2.3.1',
            'pytest==4.3.1',
        ]
    },
    install_requires=[
        'libarchive-c==2.8',
        'requests==2.20.0',
    ]
)
