import os
from grav_setup import setup_grav
from page_extraction import create_pages
from template_page import template_pages
from res_distribution import distribute_files

if __name__ == '__main__':
    os.chdir('data')
    setup_grav()
    pages = create_pages()
    pages_templates = template_pages(pages)
