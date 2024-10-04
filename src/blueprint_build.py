import os
import yaml

def to_local_path(path):
    if 'http' in path:
        return path
    return path.split('/')[-1]

def to_head_icon_field(data):
    return {
        'type': 'pagemediaselect',
        'label': data['label'],
        'default': to_local_path(data['href'])
    }

def to_text_field(data):
    return {
        'type': 'text',
        'label': data['label'],
        'default': data['content']
    }

def to_image_fields(variable_name, data):
    return {
        variable_name: {
            'type': 'section',
            'title': data['label']
        },
        f'{variable_name}_src' : {
            'type': 'pagemediaselect',
            'label': data['label'],
            'default': to_local_path(data['src'])
        },
        f'{variable_name}_alt' :{
            'type': 'text',
            'label': 'Alt Text',
            'default': data['alt']
        },
    }

def to_audio_field(variable_name, data):
    return {
        variable_name: {
            'type': 'section',
            'title': data['label']
        },
        f'{variable_name}_src': {
            'type': 'pagemediaselect',
            'label': data['label'],
            'default': to_local_path(data['src'])
        },
        f'{variable_name}_autoplay': {
            'type': 'toggle',
            'label': 'Autoplay',
            'default': data['autoplay']
        },
        f'{variable_name}_controls': {
            'type': 'toggle',
            'label': 'Controls',
            'default': data['controls']
        },
        f'{variable_name}_loop': {
            'type': 'toggle',
            'label': 'Loop',
            'default': data['loop']
        },
        f'{variable_name}_muted': {
            'type': 'toggle',
            'label': 'Muted',
            'default': data['muted']
        }
    }

def to_video_fields(variable_name, data):
    return {
        variable_name: {
            'type': 'section',
            'title': data['label']
        },
        f'{variable_name}_src': {
            'type': 'pagemediaselect',
            'label': variable_name['label'],
            'default': to_local_path(data['src'])
        },
        f'{variable_name}_autoplay': {
            'type': 'toggle',
            'label': 'Autoplay',
            'default': data['autoplay']
        },
        f'{variable_name}_controls': {
            'type': 'toggle',
            'label': 'Controls',
            'default': data['controls']
        },
        f'{variable_name}_disablepictureinpicture': {
            'type': 'toggle',
            'label': 'Disable Picture in Picture',
            'default': data['disablepictureinpicture']
        },
        f'{variable_name}_loop': {
            'type': 'toggle',
            'label': 'Loop',
            'default': data['loop']
        },
        f'{variable_name}_muted': {
            'type': 'toggle',
            'label': 'Muted',
            'default': data['muted']
        },
        f'{variable_name}_playsinline': {
            'type': 'toggle',
            'label': 'Plays Inline',
            'default': data['playsinline']
        },
        f'{variable_name}_poster': {
            'type': 'pagemediaselect',
            'label': 'Poster Image',
            'default': data['poster']
        }
    }

def to_button_fields(variable_name, data):
    return {
        variable_name: {
            'type': 'section',
            'title': data['label']
        },
        f'{variable_name}_content': {
            'type': 'text',
            'label': 'Content'
        },
        f'{variable_name}_disabled': {
            'type': 'toggle',
            'label': 'Disabled'
        }
    }

def to_a_fields(variable_name, data):
    return {
        variable_name: {
            'type': 'section',
            'title': data['label']
        },
        f'{variable_name}_href': {
            'type': 'text',
            'label': 'Link',
            'default': data['href']
        },
        f'{variable_name}_content': {
            'type': 'text',
            'label': 'Content'
        }
    }

def build_blueprint(page, twig_fields):
    blueprint = {
        'title': page,
        'form': {
            'fields': {
                'page_media': {
                'label': 'Page Media',
                'help': 'Add here all the media files for this page. Images will be available in fields with the same name as the file.',
                'type': 'pagemedia'
                }
            }
        }
    }

    header_fields = {
        'page_data': {
                    'type': 'section',
                    'title': 'Page Metadata',
                },
        'header.page_title': {
                    'type': 'text',
                    'label': 'Page Title',
        },
    }
    body_fields = {
        'page_content': {
            'type': 'section',
            'title': 'Page Content',
        }
    }

    for field, data in twig_fields.items():
        variable_name = f'header.{field}'
        field_type = data['type']

        if field_type == 'head_icon':
            header_fields['head_icon'] = to_head_icon_field(data)
        elif field_type == 'text':
            body_fields[variable_name] = to_text_field(data)
        elif field_type == 'img':
            body_fields = body_fields | to_image_fields(variable_name, data)
        elif field_type == 'audio':
            body_fields = body_fields | to_audio_field(variable_name, data)
        elif field_type == 'video':
            body_fields = body_fields | to_video_fields(variable_name, data)
        elif field_type == 'button':
            body_fields = body_fields | to_button_fields(variable_name, data)
        elif field_type == 'a':
            body_fields = body_fields | to_a_fields(variable_name, data)
    
    blueprint['form']['fields'].update({**header_fields, **body_fields})
    return blueprint

def create_blueprint(page, blueprint):
    with open(f'project-output/user/themes/project-theme/blueprints/{page}.yaml', 'w') as file:
        yaml.dump(blueprint, file, sort_keys=False)

def build_blueprints(template_pages):
    print('Creating blueprints')
    os.mkdir('project-output/user/themes/project-theme/blueprints')

    for page, data in template_pages.items():
        print(f'- {page}.yaml')
        twig_fields = data['editable']
        blueprint = build_blueprint(page, twig_fields)
        create_blueprint(page, blueprint)