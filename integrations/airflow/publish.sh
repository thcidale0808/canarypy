#!/bin/bash

pip install twine

export TWINE_USERNAME=$PYPI_USERNAME
export TWINE_PASSWORD=$PYPI_PASSWORD

twine upload dist/*.whl
