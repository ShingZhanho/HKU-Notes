"""Compatibility view for page generators; the input format is exclusively v3."""
from pathlib import Path
from hkbuild.metadata import load
from ..metadata import Metadata, ButtonKeyNode


class Reader:
    def __init__(self, metadata_file, build_target=None):
        self.path = Path(metadata_file)
        self.build_target = build_target or self.path.parent.name

    def parse(self) -> Metadata:
        data = load(self.path)
        result = Metadata(self.build_target)
        build = data['build']
        result.root_file.set(build.get('root_file', ''))
        result.output_file.set(build.get('output_file', ''))
        result.build.spec = build
        site = data.get('static_site', {})
        defaults = dict(description='-', custom_md_file='', document_status='unk', pdf_viewer='at_head')
        for key in ('description', 'meta_description', 'custom_md_file', 'document_status', 'pdf_viewer'):
            getattr(result.static_site, key).set(site.get(key, defaults.get(key)))
        result.static_site.alias_to.set(build.get('target') if build['type'] == 'alias' else None)
        result.authors.set(data.get('authors', ['jacob_shing']))
        buttons = site.get('buttons')
        if buttons is None:
            buttons = []
            if build['type'] in ('latex', 'custom'):
                buttons.append(dict(text='Download', is_primary=True, icon='material-download',
                                    href=f'../../files/{self.build_target}/{build["output_file"]}'))
            buttons.append(dict(text='View source', icon='material-github',
                                href=f'https://github.com/ShingZhanho/HKU-Notes/tree/master/src/{self.build_target}'))
        nodes = []
        for button in buttons:
            node = ButtonKeyNode(result.static_site)
            for key in ('index', 'is_primary', 'text', 'icon', 'href', 'message'):
                getattr(node, key).set(button.get(key, {'index': 0, 'is_primary': False}.get(key)))
            nodes.append(node)
        result.static_site.buttons.set(sorted(nodes, key=lambda node: node.index.get()))
        return result
