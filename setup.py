from setuptools import setup, find_packages
import sys, os

from txantiloilak import __version__

setup(name='txantiloilak',
      version=__version__,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Unai Zalakain (GISA)',
      author_email='unai@gisa-elkartea.org',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={
          'txantiloilak': ['documents/*/*'],
          },
      zip_safe=False,
      install_requires=[
          'rst2pdf',
          'Jinja2',
          'PyYAML',
          'argparse',
      ],
      entry_points={
          'console_scripts': [
              'txantiloilak = txantiloilak.txantiloilak:main',
              ],
          },
      )
