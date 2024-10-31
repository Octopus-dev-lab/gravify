import os
import json
from grav_setup import setup_grav
from page_extraction import create_pages
from template_page import template_pages
from res_distribution import distribute_files
from blueprint_build import build_blueprints

def read_config():
    print('Reading config file...', end=' ')
    config = {}
    
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
        print('OK')
    except FileNotFoundError:
        with open('../default-config.json', 'r') as file:
            config = json.load(file)
        print('OK (default-config.json)')
    
    return config

if __name__ == '__main__':
    os.chdir('data')
    config = read_config()
    setup_grav()
    pages = create_pages()
    pages_templates = template_pages(pages)
    build_blueprints(pages_templates)
    distribute_files(pages, pages_templates)