# -*- coding: utf-8 -*-
"""Setup module for flask taxonomy."""
import os

from setuptools import setup, find_packages

readme = open('README.md').read()
history = open('CHANGES.md').read()

install_requires = [
    'crossrefapi',
    'langdetect',
    'deepmerge'
]

tests_require = [
    'oarepo-validate',
    'crossrefapi',
    'deepmerge'
]

extras_require = {
    'tests': [
        *tests_require,
        'oarepo[tests]'],
    'build': [
        'oarepo-model-builder'
    ]
}

setup_requires = [
    'pytest-runner>=2.7',
]

g = {}
with open(os.path.join('oarepo_doi_resolver', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name="oarepo_doi_resolver",
    version=version,
    url="https://github.com/oarepo/oarepo-dc",
    license="MIT",
    author="Alzbeta Pokorna",
    author_email="alzbeta.pokorna@cesnet.cz",
    description="DOI resolver for OARepo",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    zip_safe=False,
    packages=['oarepo_doi_resolver'],
    entry_points={
        'invenio_base.apps': [
            'oarepo_doi_resolver = oarepo_doi_resolver:OARepoDOIResolver'
        ],
        'invenio_base.api_apps': [
            'oarepo_doi_resolver = oarepo_doi_resolver:OARepoDOIResolver'
        ]
    },
    include_package_data=True,
    setup_requires=setup_requires,
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
    ],
)
