import setuptools

setuptools.setup(
    name="canarypy",
    version="0.0.1",
    author="Thiago",
    description="CanaryPy python package.",
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests",
    ],
    entry_points='''
        [console_scripts]
        canarypy=canarypy.cli.main:cli
    ''',
)
