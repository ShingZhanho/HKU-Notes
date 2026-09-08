"""Package the pinned project's Ubuntu build; invoked with the source as cwd."""
from pathlib import Path
import shutil
import sys
import zipfile

source = Path.cwd()
document = Path(__file__).resolve().parent
binary = source / 'build/shoot'
resources = source / 'build/res'
if not binary.is_file() or not resources.is_dir():
    sys.exit('Expected build/shoot and build/res after the CMake build')
output = document / 'shoot-v1.0.0-ubuntu_24.04-x86_64.zip'
with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
    archive.write(binary, 'shoot')
    for file in sorted(resources.rglob('*')):
        if file.is_file():
            archive.write(file, str(file.relative_to(resources.parent)))
