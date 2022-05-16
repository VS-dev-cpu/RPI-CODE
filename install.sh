echo "Installing Libs for Bluetooth"

sudo apt install pip
sudo apt-get install bluetooth bluez libbluetooth-dev -y
sudo python3 -m pip install pybluez
sudo apt install libglew-dev -y

mv pystart.py ..

sudo pip3 install opencv-contrib-py

sudo echo "python3 ~/pystart.py &" >> ~/.bashrc

sudo systemctl stop serial-getty@ttyS0.service

echo "Edit '/boot/cmdline.txt' AND Enable Camera and Serial"
