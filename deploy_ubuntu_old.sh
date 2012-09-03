apt-get install python-scipy python-opencv apache2 libapache2-mod-python python-django php5 mysql-server
apt-get install php5-mysql python-mysqldb
apt-get install python-nose
apt-get install python-memcache
apt-get install liblapack-dev

# compile opencv 2.2.0:
apt-get install build-essential
apt-get install cmake
apt-get install pkg-config
apt-get install libpng12-0 libpng12-dev libpng3 libpng++-dev
apt-get install libpnglite-dev libpngwriter0-dev libpngwriter0c2
apt-get install zlib1g-dbg zlib1g zlib1g-dev
apt-get install libjasper-dev libjasper-runtime libjasper1
apt-get install pngtools libtiff4-dev libtiff4 libtiffxx0c2 libtiff-tools
apt-get install libjpeg8 libjpeg8-dev libjpeg8-dbg libjpeg-progs
apt-get install ffmpeg libavcodec-dev libavcodec52 libavformat52 libavformat-dev
apt-get install libgstreamer0.10-0-dbg libgstreamer0.10-0  libgstreamer0.10-dev
apt-get install libxine1-ffmpeg  libxine-dev libxine1-bin
apt-get install libunicap2 libunicap2-dev
apt-get install libdc1394-22-dev libdc1394-22 libdc1394-utils
apt-get install swig
apt-get install libv4l-0 libv4l-dev
apt-get install python-numpy
apt-get install libpython2.6 python-dev python2.6-dev
apt-get install doxygen
#set mysql root password

#too old : apt-get install python-scikits-learn
easy_install -U scikits.learn

cd ~/
mkdir django_projects
cd django_projects
django-admin startprojet imageex
sudo ln -s /home/cplab/django_projects/imageex /var/www/imageex
sudo nano /etc/apache2/sites-available/imageex

<Location "/imageex/">
    SetHandler python-program
    PythonHandler django.core.handlers.modpython
    PythonDebug On
    PythonPath "['/var/www'] + sys.path"
    SetEnv DJANGO_SETTINGS_MODULE examples.settings
</Location>

sudo a2ensite imageex
sudo /etc/init.d/apache2 reload

sudo apt-get install phpmyadmin
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf.d/phpmyadmin.conf
sudo /etc/init.d/apache2 reload

CREATE DATABASE `imageex` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

cd ~/django_projects/imageex
nano settings.py

DATABASES = {
    'default': {
'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
'NAME': 'imageex',      # Or path to database file if using sqlite3.
'USER': 'root',      # Not used with sqlite3.
'PASSWORD': '',  # Not used with sqlite3.
'HOST': '',      # Set to empty string for localhost. Not used with sqlite3.
'PORT': '',      # Set to empty string for default. Not used with sqlite3.
    }
}

python manage.py syncdb

