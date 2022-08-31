#DOCKER-SPEECH-API:
Docker con restapi de speech recognition. Probamos Google, Assemply-AI y DeepSpeech.

#Venv:
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt

#Cliente:
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/muke/python/mongoex/temp/NS6.wav" -F "channels=1" http://localhost:5000/calls/deep-speech

#Production:
flask run --host=0.0.0.0

#Docker:
##Build:
docker build --tag eugenio74/socker-speech-api:v1 .

##Run:
docker run -i -t -p 5000:5000 eugenio74/docker-speech-api:v1
-p PORT_API:PORT_DOCKER

##Login:
docker login -u "USERNAME" docker.io

##Push:
docker push tag/docker:version

##Pull:
docker pull eugenio74/docker-speech-api:latest

##Other Commands:
###docker images: lista imagenes
###docker image rm IMAGE_ID: borra imagen con id IMAGE_ID

Done: 
. Conexion AssemblyAI
. Conexion Google Speech
. Conexion a DeepSpeech de Mozilla

Roadmap:
. Coqui