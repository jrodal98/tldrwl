#!/usr/bin/env python3
# www.jrodal.com

from tldrwl.summarize_text import TextSummarizer
import logging

logging.basicConfig(level=logging.DEBUG)

text = """How to Deploy a Rocket Rust Web Application on VPS
August 15, 2020
 2 mins to read 
comment
 post
This tutorial provides a step-by-step guide on how to deploy a Rocket Rust web application on a VPS. The tutorial covers all the necessary steps, including acquiring a VPS and domain, setting up domain settings, downloading and installing necessary software on the VPS, and compiling the application. The tutorial also includes helpful tips and troubleshooting advice, making it a useful resource for anyone looking to deploy a Rocket Rust web application on a VPS.

Table Of Contents
Step 1: Acquire a VPS and a Domain
Step 2: Domain Settings
Step 3: Download Software on VPS
Step 4: Compile your Application and Create a Systemd Service
Step 5: Setup Nginx Webserver
Step 6: CI/CD with Github actions
rust.yml
deploy.yml
Optional: Safer and Easier SSHing into your VPS
Step 1: Acquire a VPS and a Domain
First, you need to figure out where you want to deploy your application. I chose virmach because they offer a dirt cheap $1 linux vps. It gives you 256 MB of memory, 10 GB of disk space, and 500 GB monthly bandwidth, which is more than enough for my needs. I’ve been running my application on the $1 vps for over a year now and have had no issues.

I bought my domain from namecheap because I was able to get an xyz domain name for $1, but it doesn’t matter where you get yours. You can get a free .tk domain name at dot.tk, if you don’t care about the unorthodox extension.

Step 2: Domain Settings
Next, you’ll need to point your domain to your server. You do this by creating an A record that points to the ip address allocated to your VPS. You should also create a CNAME record if you want to be able to prepend www to your domain name.

This will probably appear in the DNS settings for your domain at your domain registrar. For me, I went to namecheap and then went to “advanced dns” for my domain. I added the records like so:


where IP Address is the static IP address of your VPS and Target is your domain name.

It might take awhile for your changes to propagate across the internet, so be patient.

Step 3: Download Software on VPS
I’m going to assume that you’re running something based on debian for simplicity. Downloading and updating packages with other distros will be left as an exercise to the reader.

First, update the list of available packages and then upgrade to the latest versions:

bash

CLICK TO COPY
 
apt update && apt upgrade
Next, install some necessary packages:

bash

CLICK TO COPY
 
apt install curl git gcc nginx python3 python3-venv
Next, install certbot:

python3 -m venv /opt/certbot/
/opt/certbot/bin/pip install certbot certbot-nginx
ln -s /opt/certbot/bin/certbot /usr/bin/certbot
Lastly, install rust with the following command:

bash

CLICK TO COPY
 
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
You should run source $HOME/.cargo/env to prepare the rocket rust environment.

If you run into a “RUSTUP_UNPACK_RAM must be larger than X” error, try running export RUSTUP_UNPACK_RAM=X and trying the rust install again.

Step 4: Compile your Application and Create a Systemd Service
Get your source code onto your machine. I’m assuming you know how to do this if you’re using rust. If git isn’t an option, research rsync to copy files from your host machine to your vps. Soon, we’ll be using Github actions to automate this entire process. But for now, let’s make sure we can deploy manually.

cd into your project directory (created with cargo) and compile your project

bash

CLICK TO COPY
 
cd YOUR_PROJECT_DIR
cargo build --release
Next, create a systemd file named /etc/systemd/system/YOUR_DOMAIN.service:

/etc/systemd/system/YOUR_DOMAIN.service

CLICK TO COPY
 
[Unit]
Description=Put a description here

[Service]
User=root
Group=root
WorkingDirectory=/path/to/project/dir
Environment="ROCKET_ENV=prod"
Environment="ROCKET_ADDRESS=127.0.0.1"
Environment="ROCKET_PORT=8000"
Environment="ROCKET_LOG=critical"
ExecStart=/path/to/project/dir/target/release/YOUR_APPLICATION_NAME

[Install]
WantedBy=multi-user.target
You might not want to use root as the user, depending on your vps. Research systemd and modify it as desired.

Start your service with systemctl start YOUR_DOMAIN.service and enable it to run on system startup with systemctl enable YOUR_DOMAIN.service. Your application should now be running - check with systemctl status YOUR_DOMAIN.service

Step 5: Setup Nginx Webserver
Generate some self-signed SSL certificates:

bash

CLICK TO COPY
 
mkdir /etc/ssl/private
chmod 700 /etc/ssl/private
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
Put something like this in /etc/nginx/sites-available/YOUR_DOMAIN:

nginx

CLICK TO COPY
 
server {
    listen 80;
    listen [::]:80;

    server_name YOUR_DOMAIN_NAME www.YOUR_DOMAIN_NAME;

    location / {
        # Forward requests to rocket
        proxy_pass http://127.0.0.1:8000;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name YOUR_DOMAIN_NAME www.YOUR_DOMAIN_NAME;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    location / {
        # Forward requests to rocket
        proxy_pass http://127.0.0.1:8000;
    }
}
Then, run this command to create a symbolic link:

bash

CLICK TO COPY
 
ln -s /etc/nginx/sites-available/YOUR_DOMAIN /etc/nginx/sites-enabled/
Check your syntax with nginx -t.

Make sure to delete the default nginx file with rm /etc/nginx/sites-available/default && rm /etc/nginx/sites-enabled/default.

Reload nginx with systemctl reload nginx. Navigate to your domain on your browser with http://YOUR_DOMAIN_NAME. Verify that it’s working.

If everything is working, then go ahead and setup https with certbot --nginx and follow the instructions. If it asks you if you want to redirect http to https, you absolutely should.

Reload nginx with systemctl reload nginx. Navigate to your domain on your browser with https://YOUR_DOMAIN_NAME. Verify that it’s working.

I recommend setting up a cron job to auto renew your https certificates. Run crontab -e and insert this to run the certbot renew script at the first of each month:

plain

CLICK TO COPY
 
1 1 1 * * certbot renew
Step 6: CI/CD with Github actions
You don’t want to have to manually log into your server, pull your latest changes, build your new binary, and restart your application whenever you push code. We can use Github Actions to automate this.

Each Github actions file is a workflow. Workflows are stored in the .github/workflows directory of your repository.

You will create two workflows:

rust.yml (build and test)
deploy.yml (deploy)
You can name them whatever you want.

rust.yml
rust.yml

CLICK TO COPY
 
name: Rust

on:
  push:
    # change this to main if you use that
    branches: [ master ]
  pull_request:
    # change this to main if you use that
    branches: [ master ]

env:
  CARGO_TERM_COLOR: always

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Build
      run: cargo build --verbose
    - name: Run tests
      run: cargo test --verbose
deploy.yml
deploy.yml

CLICK TO COPY
 
name: Deploy

on:
  workflow_run:
    # Run after workflow with name "Rust" finishes
    workflows: [Rust]
    types:
      - completed

jobs:
  build:

    runs-on: ubuntu-latest
    # only run if the build and test workflow succeeded
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
    - uses: actions/checkout@v1

    - name: Copy repository contents via scp
      uses: appleboy/scp-action@master
      env:
        # see github documentation on adding secrets
        # https://docs.github.com/en/actions/security-guides/encrypted-secrets
        HOST: ${{ secrets.HOST }}
        USERNAME: ${{ secrets.USERNAME }}
        PORT: ${{ secrets.PORT }}
        # See optional section at bottom of post to learn how to get the SSHKey
        KEY: ${{ secrets.SSHKEY }}
      with:
        source: "."
        target: "/path/to/your/project"

    - name: Executing remote command
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.HOST }}
        USERNAME: ${{ secrets.USERNAME }}
        PORT: ${{ secrets.PORT }}
        KEY: ${{ secrets.SSHKEY }}
        command_timeout: 30m
        script_stop: true
        script: |
             cd /path/to/your/project
             /root/.cargo/bin/cargo build --release
             systemctl restart YOUR_DOMAIN.service             
Optional: Safer and Easier SSHing into your VPS
I like sshing with RSA keys because you don’t have to enter a password. If you don’t already have a keypair, run the following commands on your host machine (the machine you ssh from)

bash

CLICK TO COPY
 
ssh-keygen
ssh-copy-id USER@VPS_IP_ADDR
Use all of the defaults and don’t add a password to your key, unless you want to have to type your password to use it. I’m not super concerned about putting a password on my key because I’ll have bigger things to worry about if someone ever got my key to begin with.

Verify that you can ssh into your machine without a password by running ssh USER@VPS_IP_ADDR.

You can create an ssh profile by editing ~/.ssh/config on your host machine like so:

plain

CLICK TO COPY
 
Host PROFILE_NAME
    HostName VPS_IP_ADDR
    User USER
    IdentityFile ~/.ssh/id_rsa
which will allow you to ssh into your VPS by running ssh PROFILE_NAME.

I also like to disable text passwords to my remote machines so that only I can access them (or anyone with a key). If you also want to do this, set the following options in etc/ssh/sshd_config:

plain

CLICK TO COPY
 
/etc/ssh/sshd_config
PassWordAuthentication no
UsePam no
ChallengeResponseAuthentication no"""

summary = TextSummarizer().summarize_text(text)

print(summary)
print(summary.estimated_cost_usd)
