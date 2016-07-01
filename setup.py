from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pyenguin',
      version='0.1',
      description='Wrapper for pygame to provide a simple drawing and gaming framework in German. '
                  'This project is developed for the use in the CoderDojo Karlsruhe. '
                  'This project uses pygameui by Fictorial to display GUI elements.',
      url='http://github.com/coderdojoka/py2cd',
      author='Mark Weinreuter (CoderDojo Karlsruhe), pygameui (https://github.com/fictorial/pygameui)',
      packages=['pyenguin', 'pyenguin.pygameui', ],
      package_data={'pyenguin': ['resourcen/bilder/*.png',
                              'resourcen/bilder/*/*.png',
                              'resourcen/bilder/*/*/*.png',
                              'resourcen/animationen/*',
                              'resourcen/animationen/*/*',
                              'resourcen/sounds/*',
                              'resourcen/sounds/*/*',
                              'resourcen/musik/*',
                              'resourcen/musik/*/*',
                              'resourcen/schriften/*']},
      install_requires=[
          'pygame'
      ],
      keywords='pygame drawing games framework german',

      classifiers=[
          'Development Status :: 4 - Beta',

          'Intended Audience :: (CoderDojo) Developers',
          'Topic :: Software Development :: Drawing and Gaming Framework',

          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ],

      test_suite="tests",
      zip_safe=False)
