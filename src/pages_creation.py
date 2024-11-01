import os
import shutil

def find_html_files():
    print('Searching for html files...', end=' ')
    html_files = []
    for root, dirs, files in os.walk('project'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    print('OK\nFiles found:', end='\n  ')
    print("\n  ".join(f"- {path}" for path in html_files))
    return html_files

def create_md_files(html_file_paths, root_page):
    print('Creating markdown files:')
    
    page_index = 2
    
    for path in html_file_paths:
        dir_name = ''
        file_name =  path.split('/')[-1].replace('.html', '')

        if file_name == root_page.replace('.html', ''):
            dir_name = '01.' + file_name
        else:
            if page_index < 10:
                str_index = f'0{page_index}' 
            dir_name = f'{str_index}.{file_name}'
            page_index += 1

        os.mkdir(f'project-output/user/pages/{dir_name}')

        with open(f'project-output/user/pages/{dir_name}/{file_name}.md', 'w') as md_file:
            md_file.write(f'---\ntitle: {file_name}\n---\n')
            md_file.close()

        print(f'  - {path} -> {dir_name}/{file_name}.md')
    
def create_twig_files(html_file_paths):
    print('Creating twig files:')

    for path in html_file_paths:
        twig_name = path.split('/')[-1] + '.twig'
        shutil.copy(path, f'project-output/user/themes/project-theme/templates/{twig_name}')

        print(f'  - {path} -> {twig_name}')
       
        
def create_pages(root_page):
    html_file_paths = find_html_files()
    create_md_files(html_file_paths, root_page)
    create_twig_files(html_file_paths)

    return html_file_paths