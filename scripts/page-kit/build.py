#!/usr/bin/env python3
"""Generate concept pages from a category's page modules.

    python3 scripts/page-kit/build.py azure storage:storage blob:blob_storage

Each argument is  <module>:<function-suffix>  →  imports <category>/p_<module>.py, calls
build_<function-suffix>() and writes  <repo>/<category>/concepts/<function-suffix with - >.html .
Nothing is overwritten unless you name it. Output is plain static HTML: review it, lint it
(scripts/diagram-lint.js, scripts/check-site.js) and commit it. See README.md.
"""
import importlib, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    category, specs = argv[0], argv[1:]
    sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / category))
    cfg = importlib.import_module('config')
    import kit
    kit.configure(cfg.NAME, cfg.DIR, cfg.ICON)
    out = REPO / cfg.DIR / 'concepts'
    out.mkdir(parents=True, exist_ok=True)
    for spec in specs:
        mod_name, fn = spec.split(':')
        mod = importlib.import_module('p_' + mod_name)
        text = getattr(mod, 'build_' + fn)()
        target = out / (fn.replace('_', '-') + '.html')
        target.write_text(text)
        print('wrote', target.relative_to(REPO), len(text))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
