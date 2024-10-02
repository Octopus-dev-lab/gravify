import os
import shutil

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
    for _, page in pages.items():
        dir_name = page['dir']
        page_name = page['page']
        grav_page_content = get_grav_md_page_content(page_name)
        
        os.mkdir(f'project-output/user/pages/{dir_name}')
        with open(f'project-output/user/pages/{dir_name}/{page_name}', 'w') as file:
            file.write(grav_page_content)
            file.close()
        

def create_grav_template_pages(pages):
    for _, page in pages.items():
        template_name = page['template']
        page_name = page['src_name']
        
        shutil.copy(f'project/public/{page_name}', f'project-output/user/themes/project-theme/templates/{template_name}')
    
def create_grav_pages(pages):
    create_grav_md_pages(pages)
    create_grav_template_pages(pages)

def build_pages_dict(pages_names):
    pages = {}
    for page_name in pages_names:
        grav_page_index = int(page_name.split('-')[0])
        grav_page_dir = to_grav_dir_name(page_name)
        grav_page_name = to_grav_page_name(page_name)
        grav_template_name = to_grav_template_name(page_name)

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
    return pages

def create_pages():
    pages_names = find_pages()
    pages = build_pages_dict(pages_names)
    create_grav_pages(pages)
    return pages