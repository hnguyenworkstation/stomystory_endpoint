#!/usr/bin/env python
import os
from app import create_app, model
from flask_script import Manager, Shell

app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app, model=model)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


if __name__ == '__main__':
    manager.run()
