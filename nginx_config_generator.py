#!/usr/bin/env python3

import os
import sys
import subprocess
import socket

def check_dns_record_exists(domain):
    try:
        ip_address = socket.gethostbyname(domain)
        if ip_address:
            return True
    except socket.gaierror:
        return False


def generate_nginx_config(domain, nginx_template_path):
    uid = os.getlogin()
    # config_file = f'/home/{uid}/frappe-bench/config/nginx.conf'
    config_file = f'/home/{uid}/Downloads/nginx.conf'
    if domain_exists(domain, config_file):
        print("Server block exists")
        sys.exit(1)

    with open(nginx_template_path, 'r') as template_file:
        nginx_template = template_file.read()
        nginx_config = nginx_template.replace('{{ domain }}', domain)
        nginx_config = nginx_config.replace('{{ host }}', '$host')
        nginx_config = nginx_config.replace('{{ scheme }}', '$scheme')
        nginx_config = nginx_config.replace('{{ http_host }}', '$http_host')
        nginx_config = nginx_config.replace('{{ http_upgrade }}', '$http_upgrade')
        nginx_config = nginx_config.replace('{{ proxy_add_x_forwarded_for }}', '$proxy_add_x_forwarded_for')

    with open(config_file, 'a') as config_file:
        config_file.write(nginx_config)

    print(f"Server block created for {domain}")

def domain_exists(domain, config_file):
    with open(config_file, 'r') as file:
        return domain in file.read()

if _name_ == "_main_":
    if len(sys.argv) < 2:
        print("No domain name argument")
        sys.exit(1)

    domain = sys.argv[1]
    nginx_template_path = 'nginx_template.conf'

    generate_nginx_config(domain, nginx_template_path)

    # The following commands will require appropriate permissions to execute nginx and certbot with sudo.

    # Check nginx configuration
    #subprocess.run(['sudo', 'nginx', '-t'])

    # Restart nginx
    #subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])

    if not check_dns_record_exists(domain):
        print(f"Please add DNS record before obtaining an SSL certificate. \nRun sudo certbot --nginx -d domain_name after adding record.")
        sys.exit(1)


    #Obtain SSL certificate using certbot
    #subprocess.run(['sudo', 'certbot', '--nginx', '-d', domain])