import os
import shutil
from utils import progressbar

def get_grav_md_page_content(page_name):
    return f'---\ntitle: {page_name}\n---\n'

def to_grav_page_name(page_name):
    grav_page_name = page_name.split('-')[1]
    grav_page_name = grav_page_name.replace('.html', '.md')
    return grav_page_name

def to_grav_dir_name(name):
    name = name.replace('.html', '')
    name = name.replace('-', '.')
    return name

def to_grav_template_name(page_name):
    template_name = page_name.split('-')[1]
    return f'{template_name}.twig'

def find_pages():
    all_files = os.listdir('project/public')
    pages = []

    for file in all_files:
        if file.endswith('.html'):
            pages.append(file)

    return pages

def create_grav_md_pages(pages):
    print('Creating markdown pages...')
    index = 0

    for _, page in pages.items():
        dir_name = page['dir']
        page_name = page['page']
        grav_page_content = get_grav_md_page_content(page_name)
        
        progressbar(index, len(pages), '')
        print()

        os.mkdir(f'project-output/user/pages/{dir_name}')
        with open(f'project-output/user/pages/{dir_name}/{page_name}', 'w') as file:
            file.write(grav_page_content)
            file.close()
    
    print('OK')

def create_grav_template_pages(pages):
    print('Creating template pages...')
    index = 0

    for _, page in pages.items():
        template_name = page['template']
        page_name = page['src_name']
        
        progressbar(index, len(pages), '')
        print()

        shutil.copy(f'project/public/{page_name}', f'project-output/user/themes/project-theme/templates/{template_name}')
    
    print('OK')

def create_grav_pages(pages):
    create_grav_md_pages(pages)
    create_grav_template_pages(pages)

def build_pages_dict(pages_names):
    pages = {}

    print('Building pages dictionary...')

    for index, page_name in enumerate(pages_names):
        grav_page_index = int(page_name.split('-')[0])
        grav_page_dir = to_grav_dir_name(page_name)
        grav_page_name = to_grav_page_name(page_name)
        grav_template_name = to_grav_template_name(page_name)

        progressbar(index, len(pages_names), '')
        print()

        if grav_page_index in pages:
            shutil.rmtree(f'project-output')
            raise Exception(f'Duplicate index {grav_page_index} in html files')
        else:
            pages[grav_page_index] = {
                'src_name' : page_name,
                'dir': grav_page_dir,
                'page': grav_page_name,
                'template': grav_template_name
            }

    print('OK')

    return pages

def update_root_page(root_page):
    system_file = ''
    with open(f'project-output/user/config/system.yaml', 'r') as file:
        system_file = file.read()
        file.close()
    
    system_file = system_file.replace('/home', f'/{root_page}')
    
    with open(f'project-output/user/config/system.yaml', 'w') as file:
        file.write(system_file)
        file.close()

def log_pages(pages):
    print('Pages:')
    for _, page in pages.items():
        print(f'{page['src_name']} -> {page['dir']}/{page['page']} -> {page['template']}')

    print('Total pages:', len(pages))

def create_pages():
    pages_names = find_pages()
    pages = build_pages_dict(pages_names)
    root_page = pages[1]['page'].split('.')[0]
    update_root_page(root_page)
    create_grav_pages(pages)
    log_pages(pages)
    return pages