from setuptools import setup

setup(name='django-chunks-jinja2',
      version='0.1',
      description='Keyed blocks of content for use in your Django templates',
      author='Clint Ecker, Andrey Nelyubin',
      author_email='andry.kreeg@gmail.com',
      url='https://github.com/Kreeg/django-chunks-jinja2',
      packages=['chunks', 'chunks.templatetags', 'chunks.contrib'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )
