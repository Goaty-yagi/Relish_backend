curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

pip3 install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
