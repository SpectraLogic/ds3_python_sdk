#!/bin/bash
cd /opt
git clone https://github.com/SpectraLogic/ds3_c_sdk.git
cd ds3_c_sdk
autoreconf --install
./configure
make install
ldconfig

cd ..
git clone https://github.com/SpectraLogic/ds3_python_sdk.git
cd ds3_python_sdk
python setup.py install

cd tests
python -m unittest clientTests
