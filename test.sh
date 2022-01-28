git clone https://github.com/lightyagami/realnibbasgame mirror-bot/
cd mirror-bot
cp config_sample.env config.env
pip3 install -r requirements.txt
pip3 install -r requirements-cli.txt
sudo dockerd
sudo docker build . -t mirror-bot
sudo docker run -p 80:80 mirror-bot
