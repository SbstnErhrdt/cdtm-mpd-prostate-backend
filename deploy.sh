cd cdtm-mpd-prostate-backend
docker-compose down
cd ..
docker rmi prostate-backend:latest
rm -rf cdtm-mpd-prostate-backend
git clone https://github.com/SbstnErhrdt/cdtm-mpd-prostate-backend
cp docker-compose.yml ./cdtm-mpd-prostate-backend/docker-compose.yml
cd cdtm-mpd-prostate-backend
docker build -t prostate-backend ./
docker-compose up -d