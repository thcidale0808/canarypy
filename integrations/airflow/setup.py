from os import path

import setuptools

this_directory = path.abspath(path.dirname(__file__))
requirements_path = path.join(this_directory, "requirements.txt")
with open(requirements_path, "r") as f:
    install_requires = f.read().splitlines()

with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


entry_points = {
    "airflow.plugins": "canarypy-airflow-plugin = canarypy_airflow_plugin.canarypy_plugin:CanaryPyPlugin"
}

setuptools.setup(
    name="canarypy-airflow-plugin",
    version="0.0.1",
    author="Thiago Assumpcao",
    author_email="thcidale@gmail.com",
    description="CanaryPy Airflow Plugin - Airflow Integration Plugin for CanaryPy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thcidale0808/canarypy",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    project_urls={
        "Bug Reports": "https://github.com/thcidale0808/canarypy/issues",
        "Source": "https://github.com/thcidale0808/canarypy/",
    },
    entry_points=entry_points,
)
