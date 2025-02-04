from setuptools import find_packages, setup

setup(
    name="emma",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "capybara>=0.1.0",
    ],
    author="Yue Wu",
    author_email="wuyue681@gmail.com",
    description="A short description of your Emma project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mathwuyue/emma",
    include_package_data=True,  # This tells setuptools to look for package data as specified in MANIFEST.in
    package_data={
        "emma": ["emma.db"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
