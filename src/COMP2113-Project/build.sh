#!/bin/bash
# This script builds the shoot binary for Ubuntu 24.04 x86_64 and packages it into a zip file.

git clone https://github.com/ShingZhanho/ENGG1340-Project-25Spring.git repo
cd repo         # now in /src/COMP2113-Project/repo
mkdir build
cd build        # now in /src/COMP2113-Project/repo/build
cmake ..
make
mkdir bin
mv shoot ./bin/
mv res ./bin/
cd bin          # now in /src/COMP2113-Project/repo/build/bin
zip -r ../shoot-v1.0.0-ubuntu_24.04-x86_64.zip .
cd ..           # now in /src/COMP2113-Project/repo/build
mv ./shoot-v1.0.0-ubuntu_24.04-x86_64.zip ../../  # move the zip to /src/COMP2113-Project
cd ../..        # now in /src/COMP2113-Project
rm -rf repo     # clean up