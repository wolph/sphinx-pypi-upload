import os
from setuptools import setup


def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='Sphinx-PyPI-upload-2',
    version='0.2.2',
    author='Rick van Hattem',
    author_email='wolph@wol.ph',
    url='https://github.com/WoLpH/sphinx-pypi-upload',
    description='Setuptools command for uploading Sphinx documentation to the '
                'PyPI',
    long_description=read('README'),
    license='BSD',
    classifiers=[
        'Topic :: Documentation',
        'Framework :: Setuptools Plugin',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms='any',
    py_modules=['sphinx_pypi_upload'],
    entry_points={
        'distutils.commands': [
            'upload_sphinx = sphinx_pypi_upload:UploadDoc',
        ],
    },
)
