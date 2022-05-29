from core import diff, load, load_config, load_rules, render, scan
from models import (
    Config,
    Exclude,
    Format,
    Issue,
    Severity,
    Results
)
from tempfile import TemporaryDirectory
import git
from urllib.parse import urlparse
import jsonpickle
import argparse, json
import attr
from typing import Iterable


c = Config(
    exclude=None,
    severity=Severity.LOW
)

t=[
    "https://github.com/Shmood00/BadRepo.git",
    "https://github.com/trufflesecurity/trufflehog"
]

tmp_url = ''
results = []
for item in range(len(t)):
    tmp_url = t[item]
    
    remote = urlparse(t[item]).scheme in ("http", "https")
    if remote:  # pragma: no cover
        tmp = TemporaryDirectory(prefix="repo-")
        git.Repo.clone_from(t[item], tmp.name)
        t[item] = tmp.name

    s = scan(
        target=t[item],
        config=c,
        rules=load_rules('new_rules.yml'),
        processes=2
    )
    
    if s:
        results.append(Results(tmp_url, s))
        
        #render([u], format=Format.JSON)
    
    if remote:  # pragma: no cover
        tmp.cleanup()

render(results, format=Format.HTML, file='index.html')