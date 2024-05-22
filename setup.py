from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.1'
DESCRIPTION = 'Python packages for mlab ecosystem'
LONG_DESCRIPTION = 'This package contains supports the core functionalities for the mlab ecosystem'

# Setting up
setup(
    name="mlab.py",
    version=VERSION,
    author="Kelvin Nketia-Achiampong",
    author_email="<disal.bot@gmlcv.onmicrosoft.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'mlab', 'mlab ecosystem', 'mlab python packages'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers", 
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows", 
    ]
)