import os
import shutil

def distribute_by_file_type(assets, file_type):    
    for asset in assets:
        asset_name = asset.split("/")[-1]
        print(f'   * project/public/{asset} -> project-output/user/themes/project-theme/{file_type}/{asset_name}')
        shutil.copy2(f'project/public/{asset}', f'project-output/user/themes/project-theme/{file_type}/{asset_name}')

def distribute_theme_assets(theme_assets):
    distribute_by_file_type(theme_assets['css'], 'css')
    distribute_by_file_type(theme_assets['js'], 'js')
    os.mkdir(f'project-output/user/themes/project-theme/assets')
    distribute_by_file_type(theme_assets['assets'], 'assets')

def distribute_twig_assets(page_dir, twig_assets):
    for _, asset in twig_assets.items():
        attrib_name = ''
        if asset['type'] == 'img' or asset['type'] == 'video' or asset['type'] == 'audio':
            attrib_name = 'src'
        if asset['type'] == 'head_icon':
            attrib_name = 'href'

        if attrib_name != '' and 'http' not in asset[attrib_name]:
                asset_name = asset[attrib_name].split("/")[-1]
                print(f'   * project/public/{asset[attrib_name]} -> project-output/user/pages/{page_dir}/{asset_name}')
                shutil.copy2(f'project/public/{asset[attrib_name]}', f'project-output/user/pages/{page_dir}/{asset_name}')
        

def distribute_files(pages, pages_templates):
    print('Distributing files')
    for index, pages in pages.items():
        page_name = pages['template'].split('.')[0]
        page_dir = pages['dir']
        print(f'  - {page_name}')
        theme_assets = pages_templates[page_name]['theme']
        twig_assets = pages_templates[page_name]['editable']
        distribute_theme_assets(theme_assets)
        distribute_twig_assets(page_dir, twig_assets)
        
        

