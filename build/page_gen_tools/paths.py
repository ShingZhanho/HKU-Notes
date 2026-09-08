from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SitePaths:
    repository: Path
    docs: Path
    artifacts: Path

    def metadata(self, target):
        return self.repository / 'src' / target / 'metadata.json'

    @property
    def authors(self):
        return self.repository / 'site/docs/statics/authors/authors.json'
