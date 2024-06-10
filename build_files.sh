# Ensure the script exits on error
set -e

# Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# Install virtualenv
pip3 install virtualenv
virtualenv venv
pip3 install -r requirements.txt 
python3.9 src/manage.py collectstatic