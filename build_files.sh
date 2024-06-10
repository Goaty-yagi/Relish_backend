export PYTHONPATH=$(pwd)/src:$PYTHONPATH
echo "PYTHONPATH is set to: $PYTHONPATH"
pip3 install -r requirements.txt 
python3.9 src/manage.py collectstatic