# Getting base image which is alpine3
FROM alpine:3

# Install python3
RUN apk add python3
RUN apk add iputils
RUN apk add py3-pip

#Install pip and upgrade
RUN [ "pip", "install", "--upgrade", "pip" ]
RUN [ "pip", "install", "kubernetes"]

# Create user app_user 
RUN adduser app_user -h /home/app_user;echo 'app_user:myalpine123' | chpasswd

# Select working directory
WORKDIR /home/app_user

# Copy files and folders to container
COPY .. .

# Making app_user as the default user
USER app_user


#Starting the server
#CMD ["python","server.py"]
#CMD ["python","server-gossip3.py"]
CMD ["python","node5050.py"]