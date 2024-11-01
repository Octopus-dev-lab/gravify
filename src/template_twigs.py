import os
from lxml import etree
from twig_field_template import template_twig_field, template_theme_fields

parser = etree.HTMLParser()

def template_twig_fields(tree):
    twig_fields = {}
    twig_tags = tree.xpath('//*[@twig]')

    for tag in twig_tags:
       templated_tag = template_twig_field(tag)
       if templated_tag:
           twig_fields[tag.get('twig')] = templated_tag
    
    return twig_fields

def template_twig_files(html_file_paths):
    print('Templating twig files:')

    pages_templates = {}
    children = os.listdir('project-output/user/themes/project-theme/templates')
    children.remove('partials')
    children.remove('default.html.twig')
    children.remove('error.html.twig')

    for twig_file in children:
        print(f'  - {twig_file}', end=' ')
        tree = None
        src_file_path = ''

        for path in html_file_paths:
            if path.endswith(twig_file.replace('.twig', '')):
                src_file_path = os.path.dirname(path)
                break

        with open(f'project-output/user/themes/project-theme/templates/{twig_file}', 'r') as file:
            html = file.read()

            if html != '':
                tree = etree.fromstring(html, parser)
                twig_fields = template_twig_fields(tree)
                theme_fields = template_theme_fields(tree)
                page_name = twig_file.replace('.html.twig', '')
                pages_templates[page_name] = {
                    'src_file_path': src_file_path,
                    'theme': theme_fields,
                    'editable': twig_fields
                }

            file.close()

        if tree is not None:
            with open(f'project-output/user/themes/project-theme/templates/{twig_file}', 'w') as file:
                file.write(etree.tostring(tree, pretty_print=True, method="html").decode())
                file.close()
        
        print('OK')
    
    return pages_templates