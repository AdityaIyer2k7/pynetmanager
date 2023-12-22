import setuptools

with open("README.md") as fl: ldesc = fl.read()

setuptools.setup(
    name="pynetmanager",
    version="1.0.0",
    author="AdityaIyer2k7",
    author_email="adityaiyer2007@gmail.com",
    description="A FOSS library to simplify writing and handling sockets in Python. Includes INET and INET6 support, `bind`, `listen`, `accept`, `connect` API.",
    long_description=ldesc,
    long_description_content_type="text/markdown",
    url="https://github.com/AdityaIyer2k7/pynetmanager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
    keywords=[
        "python",
        "python 3",
        "socket",
        "sockets",
        "network",
        "networks",
        "networking",
    ],
    python_requires='>=3.6'
)