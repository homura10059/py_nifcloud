from setuptools import setup, find_packages

try:
    with open('README.rst', encoding="utf-8") as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name='py_nifcloud',
    version='1.0.0',
    description='Python wrapper for NifCloud',
    long_description=readme,
    url='https://github.com/o-hayato/py_nifcloud',
    author='o-hayato',
    author_email='preasper0+github@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'PyYAML',
        'botocore',
        'beautifulsoup4',
    ],
    extras_require={
        'dev': [
            'pytest>=3',
            'coverage',
            'tox',
            'sphinx',
            'jupyter',
            'lxml',
            'pallets-sphinx-themes',
            'sphinxcontrib-log-cabinet',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
)
