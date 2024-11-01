import os
import shutil

def distribute_by_file_type(assets, file_type, src_file_path):    
    for asset in assets:
        asset_name = asset.split("/")[-1]
        print(f'  - {src_file_path}/{asset} -> project-output/user/themes/project-theme/{file_type}/{asset_name}')
        shutil.copy2(f'{src_file_path}/{asset}', f'project-output/user/themes/project-theme/{file_type}/{asset_name}')

def distribute_theme_assets(theme_assets, src_file_path):
    distribute_by_file_type(theme_assets['css'], 'css', src_file_path)
    distribute_by_file_type(theme_assets['js'], 'js', src_file_path)
    os.mkdir(f'project-output/user/themes/project-theme/assets')
    distribute_by_file_type(theme_assets['assets'], 'assets', src_file_path)

def distribute_twig_assets(page_name, twig_assets, src_file_path):
    page_dirs = os.listdir(f'project-output/user/pages')
    for _, asset in twig_assets.items():
        attrib_name = ''
        if asset['type'] == 'img' or asset['type'] == 'video' or asset['type'] == 'audio':
            attrib_name = 'src'
        if asset['type'] == 'head_icon':
            attrib_name = 'href'

        if attrib_name != '' and 'http' not in asset[attrib_name]:
                asset_name = asset[attrib_name].split("/")[-1]
                page_dir = ''

                for dir_name in page_dirs:
                    page = os.listdir(f'project-output/user/pages/{dir_name}')[0].replace('.md', '')
                    if page == page_name:
                        page_dir = dir_name
                        break

                print(f'  - {src_file_path}/{asset[attrib_name]} -> project-output/user/pages/{page_dir}/{asset_name}')
                shutil.copy2(f'{src_file_path}/{asset[attrib_name]}', f'project-output/user/pages/{page_dir}/{asset_name}')
        
def distribute_files(twig_files_fields):
    print('Distributing files:')

    for key, fields in twig_files_fields.items():
        src_file_path = fields['src_file_path']
        theme_assets = fields['theme']
        twig_assets = fields['editable']
        distribute_theme_assets(theme_assets, src_file_path)
        distribute_twig_assets(key, twig_assets, src_file_path)
    
            

