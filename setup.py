from setuptools import find_packages, setup

setup(
    name='pyghelpers',
    version='1.0.1',
    author='Irv Kalb',
    author_email='Irv@furrypants.com',
    description='Classes and functions for use with Pygame',
    long_description='A collection of classes and functions for building programs using Pygame',
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    url='https://github.com/IrvKalb/pyghelpers',
    install_requires=[
        'pygame>=1.9',
        'pygwidgets>=0.9',        
        ],
    keywords="Timer classes, Scene and SceneMgr classes, Dialogs, file IO functions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
      ]
    )
