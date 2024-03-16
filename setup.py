from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]


setup(
    name='my_code_base',
    version='0.1.0',
    author='Markus Ritschel',
    author_email='git@markusritschel.de',
    description="This is a collection of routines that I've developed over time and that I use in my daily work.",
    long_description=readme,
    license="MIT license",
    keywords=(
        "Python, my-code-base"
    ),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    url='https://github.com/markusritschel/my-code-base',
    package_dir={"": str("src")},
    packages=find_packages(where="./src/", include=['my_code_base', 'my_code_base.*']),
    root="./src",
    install_requires=setup_requirements,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
