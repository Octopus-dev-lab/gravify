import os
import json
from grav_setup import setup_grav
from pages_creation import create_pages
from template_twigs import template_twig_files
from res_distribution import distribute_files
from blueprints_creation import create_blueprints

def read_config():
    print('Reading config file...', end=' ')
    config = {}
    
    try:
        with open('project/config.json', 'r') as file:
            config = json.load(file)
        print('OK')
    except FileNotFoundError:
        with open('default-config.json', 'r') as file:
            config = json.load(file)
        print('OK (default-config.json)')
    
    return config

if __name__ == '__main__':
    config = read_config()

    os.chdir('data')

    setup_grav()
    html_files_paths = create_pages(config['root_page'])
    twig_files_fields = template_twig_files(html_files_paths)
    create_blueprints(twig_files_fields)
    distribute_files(twig_files_fields)