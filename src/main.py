import os
from grav_setup import setup_grav
from page_extraction import create_pages

if __name__ == '__main__':
    os.chdir('data')
    setup_grav()
    pages = create_pages()

