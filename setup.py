from setuptools import setup, find_packages

try:
    with open('README.md') as f:
        readme = f.read()
except IOError:
    readme = ''

setup(
    name='py_nifcloud',
    version='0.0.1',
    description='Python wrapper for NifCloud',
    long_description=readme,
    url='https://github.com/o-hayato/py_nifcloud',
    author='** yourname **',
    author_email='** your@address.com **',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'requests',
        'PyYAML',
        'botocore',
    ],
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