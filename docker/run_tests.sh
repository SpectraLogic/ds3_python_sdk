
#!/bin/bash
echo Using Git Repo: ${GIT_REPO:="https://github.com/SpectraLogic/ds3_c_sdk.git"}
echo Using Git Branch: ${GIT_BRANCH:="master"}
echo Using Git Sha: ${GIT_SHA:=""}

echo DS3_ENDPOINT ${DS3_ENDPOINT}
echo DS3_SECRET_KEY ${DS3_SECRET_KEY}
echo DS3_ACCESS_KEY ${DS3_ACCESS_KEY}

echo "cd /opt"
cd /opt

if [ ${GIT_BRANCH} != "master" ]; then
  echo git clone ${GIT_REPO} --branch ${GIT_BRANCH} --single-branch
  git clone ${GIT_REPO} --branch ${GIT_BRANCH} --single-branch
else
  echo git clone ${GIT_REPO}
  git clone ${GIT_REPO}
fi

if [${GIT_SHA} != "" ]; then
  echo setting to SHA1 ${GIT_SHA}
  git reset --hard ${GIT_SHA}
fi

cd ds3_c_sdk
autoreconf --install
./configure
make install
ldconfig

cd /opt
git clone https://github.com/SpectraLogic/ds3_python_sdk.git
cd ds3_python_sdk
python setup.py install

cd tests
python -m unittest clientTests
