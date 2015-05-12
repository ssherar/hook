from setuptools import setup, find_packages

setup(
    name = "hook",
    version = "0.0.1",

    author = "Sam Sherar",
    author_email = "sbsherar@gmail.com",
    license = "MIT license",
    url = "https://github.com/ssherar/hook",
    packages = find_packages(),

    description = "A config based hook framework for github and others",
    long_description = open("README.md").read(),

    install_requires = [
        "pyyaml==3.11",
        "flask==0.10.1"
    ],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],
    
    data_files = {
        'config': '*.yml'
    }
)
