sudo apt update
sudo apt-get install wget -y
wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tgz
sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
sudo apt-get install zlib1g-dev -y
tar -xzvf Python-3.6.8.tgz
cd Python-3.6.8
./configure --enable-optimizations
sudo make altinstall
sudo apt-get install libmysqlclient-dev -y
sudo apt-get install libldap2-dev -y
sudo apt-get install libsasl2-dev -y
sudo apt-get install gcc libpq-dev -y
sudo apt-get install python3-dev python3-pip python3-venv python3-wheel -y
sudo apt-get install -y locales locales-all
cd
# mkdir venv
pwd
python3.6 -m venv venv/venv-medplus
#source venv/venv-medplus/bin/activate
venv/venv-medplus/bin/pip install wheel
pwd
venv/venv-medplus/bin/pip install -r /var/lib/jenkins/venv/venv-medplus/bin/requirements.txt
