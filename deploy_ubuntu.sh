
sudo apt-get install -y python-pip python-dev build-essential libblas-dev liblapack-dev gfortran mysql-server python-opencv python-numpy libcv2.4

git clone git://github.com/Tug/image-extraction-server.git
virtualenv image-extraction-server
cd image-extraction-server
source bin/activate

pip install numpy
pip install scipy
pip install django==1.4
pip install gunicorn
pip install MySQL-python
pip install PIL
pip install scikits.learn

mysql -u root -p <<EOF
CREATE DATABASE imageex DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
CREATE USER 'imageex'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON imageex.* TO 'imageex'@'localhost' WITH GRANT OPTION;
EOF

ln -s /usr/lib/pyshared/python2.7/cv2.so lib/python2.7/
#ln -s /usr/local/lib/python2.6/dist-packages/cv2.so lib/python2.6/

cd imageex
mkdir -p static/uploads/segmentation
python manage.py syncdb

