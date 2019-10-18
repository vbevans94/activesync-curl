brew install cmake
cd ~/Library
git clone https://github.com/libwbxml/libwbxml.git
cd libwbxml
cmake . -B/tmp/build/libwbxml
cd /tmp/build/libwbxml
make
make test
make install

echo "Project uses python3, to install please refer to https://www.python.org/"
echo "Please install python dependencies:"
echo "To install pip if you don't have yet, run:"
echo "curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py"
echo "python get-pip.py"
echo "pip install defusedxml"
echo "pip install configparser"
