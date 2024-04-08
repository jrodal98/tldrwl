import setuptools

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setuptools.setup(
    name="tldrwl",
    version="2.0.0",
    author="Jacob Rodal",
    author_email="dev@jrodal.com",
    description="Too long, didn't read/watch/listen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jrodal98/tldrwl",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=install_requires,
)
