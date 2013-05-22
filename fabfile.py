from fabric.api import local, task


@task
def github(branch='master'):
    """
    Push to GitHub.

    Arguments:
        branch='master'
    """
    allowed_branches = (
        'master',
        'develop',
    )
    if branch not in allowed_branches:
        return
    local('git push origin %s' % branch)

@task
def tags():
    """
    Push tags to GitHub.
    """
    local('git push --tags')

@task
def heroku():
    """
    Push to production on Heroku.
    """
    local('git push heroku master')

def _run_manage_command_on_heroku(command):
    local('heroku run python are_there_spiders/manage.py %s' % command)

@task
def syncdb():
    """
    Add new app tables on Heroku.
    """
    _run_manage_command_on_heroku('syncdb')

@task
def migrate():
    """
    Apply database migrations on Heroku.
    """
    _run_manage_command_on_heroku('migrate')

@task
def static_assets():
    """
    Pipeline static assets to Amazon S3.
    """
    _run_manage_command_on_heroku('collectstatic --settings=are_there_spiders.settings.production --noinput')

@task(default=True)
def all():
    """
    Full deploy. (Default task.)
    """
    github('master')
    github('develop')
    tags()
    heroku()
    # syncdb()
    migrate()
    static_assets()
