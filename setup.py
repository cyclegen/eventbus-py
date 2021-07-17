import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eventbus-py",
    version="0.0.3",
    author="CycleGen",
    author_email="pypi@cyclegen.cloud",
    description="An eventbus that used for FinanGen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclegen/eventbus-py",
    project_urls={
        "Bug Tracker": "https://github.com/cyclegen/eventbus-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)