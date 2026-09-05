import json
import shutil
import tempfile
from pathlib import Path

from cskills.handlers import HANDLERS
from cskills.runtime import run
from cskills.validation import ROOT, read_json


def fixture(name):
    identifier = next(key for key, item in HANDLERS.items() if item[1] == name)
    category = HANDLERS[identifier][0]
    folder = ROOT / 'skills' / category / name
    return identifier, read_json(folder, 'examples/input.json'), read_json(folder, 'examples/expected.json')


class RepositoryCopy:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'repository'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', 'dist', '.venv', '.pytest_cache'))
        return self

    def __exit__(self, *args):
        self.temp.cleanup()

    def mutate(self, relative, change):
        path = self.root / relative
        value = json.loads(path.read_text(encoding='utf-8'))
        change(value)
        path.write_text(json.dumps(value), encoding='utf-8')


MANIFEST_PATH = 'skills/research/summarize-evidence/skill.json'
