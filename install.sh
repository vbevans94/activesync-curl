brew install cmake
cd Library
git clone git@github.com:libwbxml/libwbxml.git
cd libwbxml
cmake . -B/tmp/build/libwbxml
cd /tmp/build/libwbxml
make
make test
make install
