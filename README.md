Are there spiders?
==================

Well, are there?

Requirements
------------
 - [git](http://git-scm.com/), well, obviously.
 - [Python](http://www.python.org) 2.7.x
 - [pip](https://pypi.python.org/pypi/pip)
 - [virtualenv](https://pypi.python.org/pypi/virtualenv) (ideally with [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/))
 - [yuglify](https://github.com/yui/yuglify/)
 - [PostgreSQL](http://www.postgresql.org/)
 - [Mercurial](http://mercurial.selenic.com/) to install one dependency from Bitbucket.
 
If you're on OS X, use [homebrew](http://mxcl.github.io/homebrew/) to install the relevant things. Life is better that way.

Setup
-----

	# Let's start in the right place.
    cd $PROJECT_HOME  # ~/code or whatever
    # We need to get the repo cloned locally.
    git clone git@github.com:wlonk/are_there_spiders.git
    # We need to set up an associated virtualenv
    mkvirtualenv -a are_there_spiders are_there_spiders
    # Now let's get in the project
    cd are_there_spiders
    # Tell the project to include the inner folder in the PYTHONPATH
    add2virtualenv $PWD/are_there_spiders
    # Set some environment variables.
    # You'll need to actually specify some of these, of course, and
    # make sure that they're in your env when you're working on this
    # project.
    cat << EOF > .env
    PORT=8000
	DJANGO_SETTINGS_MODULE=are_there_spiders.settings.local
	DJANGO_SECRET_KEY=...
	AWS_ACCESS_KEY_ID=...
	AWS_SECRET_ACCESS_KEY=...
	AWS_STORAGE_BUCKET_NAME=...
	EMAIL_HOST=...
	EMAIL_HOST_PASSWORD=...
	EMAIL_HOST_USER=...
	EMAIL_PORT=...
	EOF
	# Now, let's install the requirements:
	pip install -r requirements/local.py
	# And create and set up the database
	createdb are_there_spiders
	django-admin.py syncdb
	django-admin.py migrate

	