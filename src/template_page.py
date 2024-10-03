from lxml import etree

parser = etree.HTMLParser()

def template_css_fields(tree):
    css_fields = []
    css_tags = tree.xpath('//link[@rel="stylesheet"]')

    for tag in css_tags:
        if 'http' not in tag.get('href'):
            href = tag.get('href')
            css_fields.append(href)
            file_name = href.split('/')[-1]
            tag.attrib['href'] = f'{{{{url("theme://css/{file_name}")}}}}'
    return css_fields

def template_js_fields(tree):
    js_fields = []
    js_tags = tree.xpath('//script')

    for tag in js_tags:
        if 'http' not in tag.get('src'):
            src = tag.get('src')
            js_fields.append(src)
            file_name = src.split('/')[-1]
            tag.attrib['src'] = f'{{{{url("theme://js/{file_name}")}}}}'
    
    return js_fields

def template_assets_fields(tree):
    assets_fields = []
    assets_tags = tree.xpath('//img | //video')

    for tag in assets_tags:
        if 'http' not in tag.get('src'):
            src = tag.get('src')
            assets_fields.append(src)
            file_name = src.split('/')[-1]
            tag.attrib['src'] = f'{{{{url("theme://assets/{file_name}")}}}}'
    
    return assets_fields

def template_theme_fields(tree):
    theme_fields = {}
    
    theme_fields['css'] = template_css_fields(tree)
    theme_fields['js'] = template_js_fields(tree)
    theme_fields['assets'] = template_assets_fields(tree)
    
    return theme_fields

def template_pages(pages):
    print('Templating pages...')
    pages_templates = {}
    
    for _, page in pages.items():
        print(f'- {page['template']}', end=' ')
        tree = None
        
        with open(f'project-output/user/themes/project-theme/templates/{page['template']}', 'r') as file:
            html = file.read()
            tree = etree.fromstring(html, parser)
            theme_fields = template_theme_fields(tree)
            pages_templates[page["template"]] = theme_fields
            file.close()
        
        with open(f'project-output/user/themes/project-theme/templates/{page['template']}', 'w') as file:
            file.write(etree.tostring(tree, pretty_print=True, method="html").decode())
            file.close()
        
        print('OK')        

    return pages_templates 