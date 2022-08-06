from setuptools import setup


with open("requirements.txt") as f:
    INSTALL_REQUIRES = f.read().splitlines()


setup(
    name="dolphin",
    version="1.0.0",
    long_description="long",
    author="Hale Terminal, LLC",
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=INSTALL_REQUIRES,
    entry_points={"console_scripts": ["dolphin = dolphin.cli:entrypoint"]},
)
