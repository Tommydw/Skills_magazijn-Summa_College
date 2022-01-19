#Create a ubuntu base image with python 3 installed.
FROM python:3.8

#Set the working directory
WORKDIR /data

#copy all the files
COPY * /data/

#Install the dependencies
RUN apt-get -y update
RUN pip3 install -r requirements.txt

#Expose the required port
# EXPOSE 5000

#Run the command
# CMD ["python3", "Start.py"]
# CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "start:app", "-b", "0.0.0.0:80"]