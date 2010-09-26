from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='aaolm.portlet.coverphoto',
      version=version,
      description="A portlet that displays the cover photo from the current issue.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "INSTALL.txt")).read()  + "\n" +
                       open(os.path.join("docs", "LICENSE.txt")).read()  + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='aaolm cover photo',
      author='Shane Graber',
      author_email='liquid@reefs.org',
      url='http://www.advancedaquarist.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['aaolm', 'aaolm.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.autoinclude',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
