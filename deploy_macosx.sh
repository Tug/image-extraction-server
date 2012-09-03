
curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py imageextraction
cd imageextraction
source bin/activate

ruby <(curl -fsSkL raw.github.com/mxcl/homebrew/go)
brew install gfortran

git clone https://github.com/numpy/numpy.git
cd numpy
python setup.py build
python setup.py install
cd ..

git clone https://github.com/scipy/scipy.git
cd scipy
python setup.py build
python setup.py install
cd ..

pip install django==1.4
pip install gunicorn
# need MySQL installed
## echo "export PATH=/usr/local/mysql/bin:\$PATH" >> ~/.bash_profile
## echo "export LC_ALL=en_US.UTF-8" >> ~/.bash_profile
## echo "export LANG=en_US.UTF-8" >> ~/.bash_profile
## sudo ln -s /usr/local/mysql/lib/libmysqlclient.18.dylib /usr/lib/libmysqlclient.18.dylib
## sudo ln -s /usr/local/mysql/lib /usr/local/mysql/lib/mysql
pip install MySQLdb-python
pip install PIL
pip insall scikits.learn

brew install opencv
export PYTHONPATH="/usr/local/lib/python2.6/site-packages:$PYTHONPATH"
# if seg fault on import need to reinstall opencv after removing /Developer

