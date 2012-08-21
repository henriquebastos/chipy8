from setuptools import setup, find_packages
import os

setup(name = 'chipy8',
      version = '0.1',
      description = 'A Chip8 tool in Python',
      #long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
      author = "Henrique Bastos", author_email = "henrique@bastos.net",
      license = "BSD",
      packages = find_packages(exclude=["*.tests", "*.tests.*", "examples"]),
      scripts = ['bin/chipy8'],
      classifiers = [
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Programming Language :: Assembly',
          'Topic :: Games/Entertainment',
          'Topic :: Software Development :: Assemblers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Compilers',
          'Topic :: Software Development :: Embedded Systems',
        ],
      url = 'http://github.com/henriquebastos/chipy8/',
)
