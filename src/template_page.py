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

def template_pages(pages):
    print('Templating pages...')
    pages_templates = {}
    
    for _, page in pages.items():
        print(f'- {page['template']}', end=' ')
        tree = None
        
        with open(f'project-output/user/themes/project-theme/templates/{page['template']}', 'r') as file:
            html = file.read()
            tree = etree.fromstring(html, parser)
            twig_fields = template_twig_fields(tree)
            theme_fields = template_theme_fields(tree)
            page_name = page['template'].split('.')[0]
            pages_templates[page_name] = {
                'theme': theme_fields,
                'editable': twig_fields
            }
            file.close()
        
        with open(f'project-output/user/themes/project-theme/templates/{page['template']}', 'w') as file:
            file.write(etree.tostring(tree, pretty_print=True, method="html").decode())
            file.close()
        
        print('OK')        

    return pages_templates 