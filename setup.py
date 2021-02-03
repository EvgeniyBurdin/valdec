from os.path import dirname, join

from setuptools import setup

setup(
    name='valdec',
    version='1.1.0',
    license='MIT',
    author='Evgeniy Burdin',
    author_email='e.s.burdin@mail.ru',
    packages=['valdec'],
    description='Decorator for validating function arguments and result.',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/EvgeniyBurdin/valdec',
    keywords='validation function',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    python_requires='>=3.7',
)
