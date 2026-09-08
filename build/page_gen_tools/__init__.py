"""Generate website pages from explicit source and artifact paths."""
import shutil
from .utils import get_targets_dict
from .gen_details_page import gen_details_page
from .gen_catalogue_page import gen_catalogue_page
from mttools import Reader


def start(targets, paths):
    targets_dict = get_targets_dict(targets)
    (paths.docs / 'downloads/details').mkdir(parents=True, exist_ok=True)
    for target in targets:
        metadata = Reader(paths.metadata(target), target).parse()
        gen_details_page(target, metadata, targets_dict, paths)
        extra = paths.repository / 'src' / target / '.COPY'
        if extra.is_dir():
            shutil.copytree(extra, paths.docs / 'downloads/details' / target, dirs_exist_ok=True)
    gen_catalogue_page(targets_dict, paths)
