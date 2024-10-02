import os
import shutil
import zipfile
import pexpect
from utils import progressbar

def download_grav():
    print('Checking for Grav...', end=' ')
    if not os.path.exists('grav.zip'):
        print('\nGrav not found. Downloading...', end=' ')
        os.system('wget https://getgrav.org/download/core/grav-admin/1.7.46 -O grav.zip')
        
    print('OK')

def extract_grav():
    with zipfile.ZipFile('grav.zip', 'r') as zipf:
        file_list = zipf.namelist()
        total_files = len(file_list)
        print('Extracting Grav...')
        print()

        for idx, file in enumerate(file_list):
            zipf.extract(file, 'grav-extracted')
            progressbar(idx, total_files, '')
    print()
    

def get_grav():
    download_grav()
    extract_grav()
    shutil.move('grav-extracted/grav-admin', 'project-output')
    os.rmdir('grav-extracted')

def install_grav_devtools():
    print('Installing Grav devtools...')
    os.chdir('project-output')
    os.system('php bin/gpm install devtools')

def create_new_theme():
    print('Creating new theme...', end=' ')
    child_process = pexpect.spawn('php bin/plugin devtools new-theme')
    child_process.expect(r'Enter.*Theme.*Name')
    child_process.sendline('project-theme')
    child_process.expect(r'Enter.*Theme.*Description')
    child_process.sendline('A Grav theme for Project')
    child_process.expect(r'Enter.*Developer.*Name')
    child_process.sendline('Name')
    child_process.expect(r'Enter.*GitHub.*ID')
    child_process.sendline('')
    child_process.expect(r'Enter.*Developer.*Email')
    child_process.sendline('email@gmail.com')
    child_process.expect(r'Please.*choose.*an.*option')
    child_process.sendline('pure-blank')
    child_process.expect(pexpect.EOF)
    print('OK')

def set_theme_as_default():
    print('Setting project-theme as default theme')
    print('Updating project-output/user/config/system.yaml...', end=' ')
    yaml = ""
    with open('user/config/system.yaml', 'r') as f:
        yaml = f.read()
        f.close()

    yaml = yaml.replace('quark', 'project-theme')
    yaml = yaml.replace('markdown: true', 'markdown: false')
    yaml = yaml.replace('twig: false', 'twig: true')

    with open('user/config/system.yaml', 'w') as f:
        f.write(yaml)
        f.close()

    os.chdir('..')
    print('OK')


def setup_theme():
    install_grav_devtools()
    create_new_theme()
    set_theme_as_default()
    

def remove_default_files():
    print('Cleaning up default files')
    print('Removing project-output/user/pages/01.home...', end=' ')
    shutil.rmtree('project-output/user/pages/01.home')
    print('OK')
    print('Removing project-output/user/pages/02.typography...', end=' ')
    shutil.rmtree('project-output/user/pages/02.typography')
    print('OK')
    print('Removing project-output/user/themes/quark...', end=' ')
    shutil.rmtree('project-output/user/themes/quark')
    print('OK')
    print('Removing project-output/user/themes/project-theme/css/custom.css...', end=' ')
    os.remove('project-output/user/themes/project-theme/css/custom.css')
    print('OK')
    print('Removing project-output/user/themes/project-theme/images/logo.png...', end=' ')
    os.remove('project-output/user/themes/project-theme/images/logo.png')
    print('OK')


def setup_grav():
    get_grav()
    setup_theme()
    remove_default_files()