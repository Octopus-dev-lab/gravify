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

def distribute_files(pages_templates):
    print('Distributing files')
    for template, all_assets in pages_templates.items():
        print(f'  - {template}')
        theme_assets = all_assets['theme']
        twig_assets = all_assets['editable']
        distribute_theme_assets(theme_assets)
        
        

