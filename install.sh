echo "Installing Libs for Bluetooth"

sudo apt update
sudo apt install pip
sudo apt install python3-gpiozero -y
sudo apt install bluetooth bluez libbluetooth-dev -y
sudo apt install libglew-dev -y
sudo python3 -m pip install pybluez
sudo pip3 install gpiozero

mv pystart.py ..

sudo pip3 install opencv-contrib-python

sudo echo "python3 ~/pystart.py &" >> ~/.bashrc

sudo systemctl stop serial-getty@ttyS0.service

echo "disable serial0 - 'sudo nano /boot/cmdline.txt' [AND] enable camera and serial communication - 'sudo raspi-config'"
