from setuptools import find_packages, setup

setup(
    name="emma",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "capybara>=0.1.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your capybara project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/capybara",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
