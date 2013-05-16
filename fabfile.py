from fabric.api import local


def github(branch='master'):
    allowed_branches = (
        'master',
        'develop',
    )
    if branch not in allowed_branches:
        return
    local('git push origin %s' % branch)

def tags():
    local('git push --tags')

def heroku():
    local('git push heroku master')

def _run_manage_command_on_heroku(command):
    local('heroku run python are_there_spiders/manage.py %s' % command)

def syncdb():
    _run_manage_command_on_heroku('syncdb')

def migrate():
    _run_manage_command_on_heroku('migrate')

def static_assets():
    local('django-admin.py collectstatic --settings=are_there_spiders.settings.production --noinput')

def all():
    github('master')
    github('develop')
    tags()
    heroku()
    syncdb()
    migrate()
    static_assets()
