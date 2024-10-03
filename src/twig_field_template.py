text_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'textarea', 'li', 'span']

def template_css_fields(tree):
    css_fields = []
    css_tags = tree.xpath('//link[@rel="stylesheet"]')

    for tag in css_tags:
        if tag.get('twig') is None and 'http' not in tag.get('href'):
            href = tag.get('href')
            css_fields.append(href)
            file_name = href.split('/')[-1]
            tag.attrib['href'] = f'{{{{url("theme://css/{file_name}")}}}}'
    return css_fields

def template_js_fields(tree):
    js_fields = []
    js_tags = tree.xpath('//script')

    for tag in js_tags:
        if tag.get('twig') is None and 'http' not in tag.get('src'):
            src = tag.get('src')
            js_fields.append(src)
            file_name = src.split('/')[-1]
            tag.attrib['src'] = f'{{{{url("theme://js/{file_name}")}}}}'
    
    return js_fields

def template_assets_fields(tree):
    assets_fields = []
    assets_tags = tree.xpath('//img | //video')

    for tag in assets_tags:
        if tag.get('twig') is None and 'http' not in tag.get('src'):
            src = tag.get('src')
            assets_fields.append(src)
            file_name = src.split('/')[-1]
            tag.attrib['src'] = f'{{{{url("theme://assets/{file_name}")}}}}'
    
    return assets_fields

def to_twig_media_ref(var_name):
    return f"{{{{url((media[(page.header.{var_name}|first).name]).url)}}}}"

def to_twig_variable_ref(var_name):
    return f'{{{{page.header.{var_name}}}}}'

def to_twig_boolean_ref(var_name, tag_name):
    return f'{{%if page.header.{var_name} %}}tag_name{{% endif %}}'

def template_title_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'title',
        'label': field_name.replace('_', ' ').capitalize(),
        'content': '' if tag.text is None else tag.text
    }
    tag.text = f'{{{{page.header.{field_name}}}}}'

    return field

def template_link_field(tag):
    rel = tag.get('rel')
    if rel != 'icon':
        raise Exception(f'Link tag with rel {rel} not supported, only icon links are supported')
    field_name = tag.get('twig')
    field = {
        'type': 'head_icon',
        'href': '' if tag.get('href') is None else tag.get('href'),
        'label': field_name.replace('_', ' ').capitalize(),
    }
    tag.attrib['href'] = to_twig_media_ref(field_name)

    return field

def template_img_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'img',
        'src': '' if tag.get('src') is None else tag.get('src'),
        'label': field_name.replace('_', ' ').capitalize(),
        'alt': '' if tag.get('alt') is None else tag.get('alt')
    }
    tag.attrib['src'] = to_twig_media_ref(field_name + '_src')
    tag.attrib['alt'] = to_twig_variable_ref(field_name + '_alt')

    return field
    
def template_audio_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'audio',
        'src': '' if tag.get('src') is None else tag.get('src'),
        'label': field_name.replace('_', ' ').capitalize(),
        'autoplay': tag.get('autoplay'),
        'controls': tag.get('controls'),
        'loop': tag.get('loop'),
        'muted': tag.get('muted')
    }
    tag.attrib['src'] = to_twig_media_ref(field_name + '_src')
    tag.attrib['autoplay'] = to_twig_boolean_ref(field_name + '_autoplay')
    tag.attrib['controls'] = to_twig_boolean_ref(field_name + '_controls')
    tag.attrib['loop'] = to_twig_boolean_ref(field_name + '_loop')
    tag.attrib['muted'] = to_twig_boolean_ref(field_name + '_muted')

    return field

def template_video_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'video',
        'src': '' if tag.get('src') is None else tag.get('src'),
        'label': field_name.replace('_', ' ').capitalize(),
        'autoplay': tag.get('autoplay'),
        'controls': tag.get('controls'),
        'disablepictureinpicture': tag.get('disablepictureinpicture'),
        'loop': tag.get('loop'),
        'muted': tag.get('muted'),
        'playsinline': tag.get('playsinline'),
        'poster': '' if tag.get('poster') is None else tag.get('poster')
    }
    tag.attrib['src'] = to_twig_media_ref(field_name + '_src')
    tag.attrib['autoplay'] = to_twig_boolean_ref(field_name + '_autoplay')
    tag.attrib['controls'] = to_twig_boolean_ref(field_name + '_controls')
    tag.attrib['disablepictureinpicture'] = to_twig_boolean_ref(field_name + '_disablepictureinpicture')
    tag.attrib['loop'] = to_twig_boolean_ref(field_name + '_loop')
    tag.attrib['muted'] = to_twig_boolean_ref(field_name + '_muted')
    tag.attrib['playsinline'] = to_twig_boolean_ref(field_name + '_playsinline')
    tag.attrib['poster'] = to_twig_media_ref(field_name + '_poster')

    return field

def template_button_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'button',
        'label': field_name.replace('_', ' ').capitalize(),
        'content': '' if tag.text is None else tag.text,
        'disabled': tag.get('disabled')
    }    
    tag.text = f'{{{{page.header.{field_name}}}}}' 
    tag.attrib['disabled'] = to_twig_boolean_ref(field_name + '_disabled')  

    return field

def template_a_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'link',
        'href': '' if tag.get('href') is None else tag.get('href'),
        'label': field_name.replace('_', ' ').capitalize(),
        'content': '' if tag.text is None else tag.text
    }
    tag.attrib['href'] = to_twig_variable_ref(field_name + '_href')
        

def template_text_field(tag):
    field_name = tag.get('twig')
    field = {
        'type': 'text',
        'label': field_name.replace('_', ' ').capitalize(),
        'content': '' if tag.text is None else tag.text
    }    
    tag.text = f'{{{{page.header.{field_name}}}}}'

    return field

def template_twig_field(tag):
    tag_type = tag.tag

    if('img' in tag_type):
        templated_field = template_img_field(tag)
        return templated_field
    elif('audio' in tag_type):
        return template_audio_field(tag)
        
    elif('video' in tag_type):
        return template_video_field(tag)
    elif('button' in tag_type):
        return template_button_field(tag)
    elif('a' in tag_type):
        return template_button_field(tag)
    elif('link' in tag_type):
        return template_link_field(tag)
    elif('title' in tag_type):
        return template_title_field(tag)
    elif(tag_type in text_tags):
        return template_text_field(tag)
    else:
        print(f'No template for {tag_type}')
        return None

def template_theme_fields(tree):
    theme_fields = {}
    
    theme_fields['css'] = template_css_fields(tree)
    theme_fields['js'] = template_js_fields(tree)
    theme_fields['assets'] = template_assets_fields(tree)
    
    return theme_fields