from pathlib import Path
import shutil,json
from setuptools import setup
from setuptools.command.build_py import build_py

class BuildWithTemplates(build_py):
    def run(self):
        super().run()
        source=Path(__file__).parent/'assets/templates'
        target=Path(self.build_lib)/'resume_craft/assets/templates'
        for meta in source.glob('*/template.json'):
            data=json.loads(meta.read_text(encoding='utf-8'))
            if data.get('distribution')=='local-only':
                stale=target/meta.parent.name
                if stale.exists():
                    assert stale.resolve().is_relative_to(target.resolve()) and stale.resolve()!=target.resolve()
                    shutil.rmtree(stale)
                continue
            shutil.copytree(meta.parent,target/meta.parent.name,dirs_exist_ok=True)

setup(cmdclass={'build_py':BuildWithTemplates})
