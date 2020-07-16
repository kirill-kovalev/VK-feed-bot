#git stash
#git pull
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install vk pytelegrambotapi
cd bot
python3 ./__init__.py $*

