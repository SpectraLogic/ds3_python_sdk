#!/bin/bash
cd /opt
git clone https://github.com/SpectraLogic/ds3_c_sdk.git
cd ds3_c_sdk/test
./build_local.sh

cd ../..
git clone https://github.com/SpectraLogic/ds3_python_sdk.git
cd ds3_python_sdk
sudo python setup.py install
LD_LIBRARY_PATH=/opt/ds3_c_sdk/install/lib:$LD_LIBRARY_PATH

cd tests
./clientTests.py
