from setuptools import setup, find_packages

setup(
    name="django_dashub",
    version="2.0.2",
    author="Suresh Chand",
    author_email="scthakuri12a@gmail.com",
    description="A modern Django admin dashboard with enhanced customization options, inspired by Jazzmin but featuring a fresh theme and additional functionality.",
    packages=find_packages(),
    license="BSD",
    install_requires=[
        "django",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License"
    ],
    include_package_data=True,
    package_data={
        "django_dashub": [
            "templates/*",
            "static/*",
            "contrib/*",
            "templatetags/*",
            "AUTHORS",
            "LICENSE",
            "README.md"
        ],
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    project_urls={
        "Bug Reports": "https://github.com/scthakuri/django-dashub/issues",
        "Source": "https://github.com/scthakuri/django-dashub",
    },
)
