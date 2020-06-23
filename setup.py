# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ""
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, "README.rst")
if os.path.exists(readme_path):
    with open(readme_path, "rb") as stream:
        readme = stream.read().decode("utf8")


setup(
    long_description=readme,
    name="displayarray",
    version="1.2.0",
    description="Tool for displaying numpy arrays.",
    python_requires="==3.*,>=3.6.0",
    project_urls={"repository": "https://github.com/simleek/displayarray"},
    author="SimLeek",
    author_email="simulator.leek@gmail.com",
    license="MIT",
    entry_points={"console_scripts": ["displayarray = displayarray.__main__:main"]},
    packages=[
        "displayarray",
        "displayarray.effects",
        "displayarray.frame",
        "displayarray.window",
    ],
    package_dir={"": "."},
    package_data={},
    install_requires=[
        "docopt==0.6.2",
        "localpubsub==0.0.4",
        "numpy==1.16.1",
        "opencv-python==4.*,>=4.0.0",
        "pyzmq==18.1.0",
    ],
    extras_require={
        # pypi doesn't allow direct dependencies for security reasons,
        # even though I could install a lot of viruses just from this setup.py
        # "linux": ["PyV4L2Cam @ git+https://github.com/SimLeek/PyV4L2Cam"],
        "dev": [
            "black==18.*,>=18.3.0.a0",
            "coverage==4.*,>=4.5.0",
            "mock==3.*,>=3.0.0",
            "mypy==0.*,>=0.740.0",
            "pydocstyle==4.*,>=4.0.0",
            "pytest==5.2.1",
            "sphinx==2.*,>=2.2.0",
            "tox==3.*,>=3.14.0",
            "tox-gh-actions==0.*,>=0.3.0",
            "typing==3.7.4.1",
            "wheel==0.*,>=0.30.0"
        ],
    },
)
