import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-simple-api-proxy',
    fullname='django-simple-api-proxy',
    author='Nat Lee',
    author_email='natlee.work@gmail.com',
    description='Easy to proxy any APIs you want.',
    keywords='django, api, proxy, proxy pass',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/natlee/Django-Simple-API-Proxy',
    project_urls={
        'Documentation': 'https://github.com/natlee/Django-Simple-API-Proxy',
        'Bug Reports': 'https://github.com/natlee/Django-Simple-API-Proxy/issues',
        'Source Code': 'https://github.com/natlee/Django-Simple-API-Proxy',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=['django>=4.0.0', 'requests', 'loguru', 'djangorestframework'],
    extras_require={
        'dev': ['check-manifest'],
        # 'test': ['coverage'],
    },
)
