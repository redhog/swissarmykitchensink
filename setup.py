#! /usr/bin/python

from setuptools.command import easy_install
from setuptools import setup, find_packages
import shutil
import os.path
import sys
import hashlib

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_NAME = os.path.basename(PKG_DIR)

# Make it possible to overide script wrapping
old_is_python_script = easy_install.is_python_script
def is_python_script(script_text, filename):
    if 'SETUPTOOLS_DO_NOT_WRAP' in script_text:
        return False
    return old_is_python_script(script_text, filename)
easy_install.is_python_script = is_python_script

setup(
    name = "swissarmykitchensink",
    description = "Swiss army kitchen sink for all things to do with database queries and data conversion / editing from the command line.",
    keywords = "sql export csv kml csv json geojson",
    install_requires = ["Shapely>=1.2.18", "fastkml>=0.3dev", "geojson>=1.0.1", "jsonpath>=0.54"],
    version = "0.0.3",
    author = "Egil Moeller",
    author_email = "egil.moller@piratpartiet.se",
    license = "GPL",
    url = "https://github.com/redhog/swissarmykitchensink",
    scripts = ["db_export", "skyconvert", "jsonedit"]
)
