import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vanillapay",  # This is the name of the package
    version="1.0.0",  # The initial release version
    author="Vanilla Pay Team",  # Full name of the author
    description="This module offers a streamlined solution for seamlessly integrating the Vanilla Pay payment system into Python applications.",
    long_description=long_description,  # Long description read from the readme
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/Rohan29-AN/vanilla_pay_python",
    },
    packages=["vanillapay"],  # List of all modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    python_requires=">=3.12",
    py_modules=["vanillapay"],  # Name of the python package
    install_requires=["requests"],  # depandance
    include_package_data=True,  # Include all data file with the package
)