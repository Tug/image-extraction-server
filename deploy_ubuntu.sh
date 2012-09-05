
sudo apt-get install -y python-pip python-dev build-essential liblapack-dev gfortran mysql-server python-opencv python-numpy libcv2.4
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv

git clone git://github.com/Tug/image-extraction-server.git
virtualenv image-extraction-server
cd image-extraction-server
source bin/activate

sudo easy_install pip
pip install numpy
pip install scipy
pip install django==1.4
pip install gunicorn
pip install MySQL-python

sudo apt-get install -y libjpeg62-dev libfreetype6 libfreetype6-dev
sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/
pip install PIL

pip install scikits.learn

pip install --no-install PIL
cd build/PIL

mysql -u root -p <<EOF
CREATE DATABASE imageex DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'imageex'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON imageex.* TO 'imageex'@'localhost' WITH GRANT OPTION;
EOF

cd ../..
ln -s /usr/lib/pyshared/python2.7/cv2.so lib/python2.7/

cd imageex
mkdir -p static/uploads/segmentation
python manage.py syncdb
