import setuptools

setuptools.setup(
    name="canarypy",
    version="0.0.11",
    author="Thiago Assumpcoa",
    description="CanaryPy python package.",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests",
    ],
    entry_points="""
        [console_scripts]
        canarypy=canarypy.cli.main:cli
    """,
)
