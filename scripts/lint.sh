#!/bin/bash

black canarypy tests --check

isort canarypy tests --check --profile black