from setuptools import setup

setup (
    name="django_blog",
    version="0.1.1",
    packages=["djblog", "blog"],
    install_requires=[
        "django",
        "django-markdownify",
    ],
)
