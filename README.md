
# Installation instructions


## Install OpenCV 2.4

### Unbutu > 10.04 :
    sudo apt-get install -y python-opencv libcv2.4

### Ubuntu <= 10.04 :
See [Install-OpenCV](https://github.com/jayrambhia/Install-OpenCV)



## Install MySQL Server

    sudo apt-get install -y mysql-server



## Install Python libraries

    sudo apt-get install -y python-pip python-dev build-essential libblas-dev liblapack-dev gfortran
    pip install numpy
    pip install scipy
    pip install django==1.4
    pip install MySQL-python
    pip install PIL
    pip install scikits.learn
    

## Configure MySQL server

    mysql -u root -p <<EOF
    CREATE DATABASE imageex DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
    CREATE USER 'imageex'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON imageex.* TO 'imageex'@'localhost' WITH GRANT OPTION;
    EOF

    python manage.py syncdb


# Create upload directory

    mkdir -p static/uploads/segmentation


