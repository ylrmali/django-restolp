from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name='django-restolp',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    author='Ali Yıldırım',
    author_email='ylrmali1289@gmail.com',
    description='Django Rest Framework Object Level Permissions',
    url='https://github.com/ylrmali/django-restolp.git',
    install_requires=[
        'djangorestframework>=3.14.0',
        'django-guardian>=2.4.0',
    ]
)