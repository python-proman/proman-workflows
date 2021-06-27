# type: ignore
from invoke import Collection, task


@task
def update(ctx, package=None, force=False):
    if not package:
        package = ctx.package
    return f"update {package}"


tasks = Collection(update)
