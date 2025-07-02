FROM ubuntu:latest

WORKDIR /app

RUN apt update && apt upgrade -y && \
    apt install -y nginx python3 python3.12-venv nano
    
COPY . .

RUN chmod +x start.sh

RUN python3 -m venv env && \
    . env/bin/activate && \
    pip install --no-cache-dir -r requirements.txt
    
COPY ./asistencias /etc/nginx/sites-available

RUN ln -s /etc/nginx/sites-available/asistencias /etc/nginx/sites-enabled

RUN rm /etc/nginx/sites-enabled/default

RUN nginx

EXPOSE 80

CMD ["bash", "start.sh"]


