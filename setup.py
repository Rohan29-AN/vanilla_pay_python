import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vanillapay", 
    version="1.0.1", 
    author="Vanilla Pay Team",  
    description="This module offers a streamlined solution for seamlessly integrating the Vanilla Pay payment system into Python applications.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/Rohan29-AN/vanilla_pay_python",
    },
    packages=["vanillapay"],
    keywords=['vanilla pay','fintech','online_payment'],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    python_requires=">=3.12",
    py_modules=["vanillapay"],  
    install_requires=["requests","python-dotenv"], 
    include_package_data=True,
)