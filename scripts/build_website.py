"""Build the static Pages site from the canonical resource catalog."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / '_site'
output.mkdir(exist_ok=True)
for path in (ROOT / 'website').iterdir():
    if path.is_file():
        shutil.copy2(path, output / path.name)
(output / 'data').mkdir(exist_ok=True)
for name in ('resources.json', 'categories.json'):
    shutil.copy2(ROOT / 'data' / name, output / 'data' / name)
(output / '.nojekyll').touch()
print(f'Built static website in {output}')
