from setuptools import setup, find_packages

__version__ = '0.9.0'

setup(
    name='spoticast',
    version=__version__,
    description='Spotify broadcasting.',
    long_description='https://github.com/jaruserickson/spotiplay',
    url='https://github.com/jaruserickson/spotiplay',
    author='jaruserickson',
    author_email='jarus.erickson@gmail.com',
    license='MIT',
    keywords='spotify spoticast spotiplay broadcast dj room song search',
    packages=find_packages(),
    install_requires=[
        'requests ~= 2.4.3',
        'pycrypto~=2.6.1'
    ],
    entry_points={
        'console_scripts': [
            'spoticast=app.spoticast:main'
        ]
    },
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Terminals',
    ],
)
