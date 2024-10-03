import os
import shutil

def distribute_by_file_type(assets, file_type):    
    for asset in assets[file_type]:
        asset_name = asset.split("/")[-1]
        print(f'   * project/public/{asset} -> project-output/user/themes/project-theme/{file_type}/{asset_name}')
        shutil.copy2(f'project/public/{asset}', f'project-output/user/themes/project-theme/{file_type}/{asset_name}')
    
def distribute_files(pages_templates):
    print('Distributing files')
    for template, assets in pages_templates.items():
        print(f'  - {template}')

        distribute_by_file_type(assets, 'css')
        distribute_by_file_type(assets, 'js')
        os.mkdir(f'project-output/user/themes/project-theme/assets')
        distribute_by_file_type(assets, 'assets')