from raven.contrib.flask import Sentry


def setup(app):
    if app.config['SENTRY_CONFIG']['environment'] in ['production', 'staging']:
        Sentry(app)
        print('Sentry started with environment "{}"'.format(app.config['SENTRY_CONFIG']['environment']))
    else:
        print('Sentry not started due to environment "{}"'.format(app.config['SENTRY_CONFIG']['environment']))
