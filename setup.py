import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="Sphinx-PyPI-upload",
    version='0.2.1',
    author="Jannis Leidel",
    author_email="jannis@leidel.info",
    url="http://bitbucket.org/jezdez/sphinx-pypi-upload/",
    download_url="http://bitbucket.org/jezdez/sphinx-pypi-upload/downloads/",
    description="setuptools command for uploading Sphinx documentation to PyPI",
    long_description=read('README'),
    license="BSD",
    classifiers=[
        "Topic :: Documentation",
        "Framework :: Setuptools Plugin",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: BSD License',
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    platforms='any',
    py_modules=["sphinx_pypi_upload"],
    entry_points = {
        "distutils.commands": [
            "upload_sphinx = sphinx_pypi_upload:UploadDoc",
        ]
    }
)
