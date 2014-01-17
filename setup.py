

from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py
    
setup(
    name = 'bottle-mongoengine',
    version = '0.0.1',
    description = 'MongoEngine integration for Bottle.',
    author = 'Juan Madurga',
    author_email = 'jlmadurga@gmail.com',
    url = 'http://www.github.com/jlmadurga/bottle-mongoengine',
    license = 'MIT',
    platforms = 'any',
    py_modules = [
        'bottle_mongoengine'
    ],
    requires = [
        'bottle(>=0.9)',
        'mongoengine',        
    ],
    tests_require = [
        'webtest'
    ],    
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
