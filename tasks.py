from invoke import task
import shutil
from pathlib import Path


@task
def clean(c, docs=False, bytecode=False, extra=''):
    patterns = ['build', 'dist', '*.egg-info']
    if docs:
        patterns.append('docs/_build')
    if bytecode:
        patterns.append('**/*.pyc')
    if extra:
        patterns.append(extra)

    for pattern in patterns:
        # Pathオブジェクトを生成
        current_dir = Path("./")
        path_list = list(current_dir.glob(pattern))

        for path in path_list:
            print("remove : " + str(path))
            shutil.rmtree(str(path))


@task
def build(c, docs=False, pypi=False):
    c.run("python setup.py build")
    if pypi:
        c.run("python setup.py sdist")
        c.run("python setup.py bdist_wheel")
    if docs:
        c.run("sphinx-build docs docs/_build")


@task
def release(c):
    clean(c)
    build(c, pypi=True)
    c.run("twine upload dist/*")
