# type: ignore
from invoke import Collection, task


@task
def update(ctx, package=None, force=False):
    print('yeppers')


tasks = Collection(update)
