"""Generate navigation into a destination config, leaving the template intact."""
import json
from pathlib import Path
from hkbuild.metadata import resolve_alias

PLACEHOLDER = '# == RES_LIST_PLACEHOLDER == #'


def generate(targets, repository, template, destination, site_url):
    courses = {}
    for target in targets:
        course = target[:8] if len(target) > 8 and target[:4].isalpha() and target[4:8].isdigit() else 'Miscellaneous'
        link = resolve_alias(repository / 'src' / target).name
        courses.setdefault(course, []).append((target, link))
    lines = []
    for course, entries in sorted(courses.items()):
        lines.append(f'      - {json.dumps(course)}:')
        for target, link in sorted(entries):
            lines.append(f'        - {json.dumps(target)}: downloads/details/{link}.md')
    text = template.read_text(encoding='utf-8')
    if PLACEHOLDER not in text:
        raise ValueError(f'Navigation placeholder missing from {template}')
    text = text.replace(PLACEHOLDER, '\n'.join(lines))
    # Preserve custom YAML tags used by the site's Markdown extensions.
    text = '\n'.join('site_url: ' + json.dumps(site_url) if line.startswith('site_url:') else line for line in text.splitlines())
    destination.write_text(text + '\n', encoding='utf-8')
