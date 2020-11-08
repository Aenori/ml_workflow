import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from version import VERSION

setuptools.setup(
    name="ml_workflow", # Replace with your own username
    version=VERSION,
    author="Nicolas Rousset",
    author_email="nicolas.rousset@aenori.com",
    description="Machine Learning Workflow : helping make machine learning packages understable",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Aenori/ml_workflow",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)