from setuptools import setup, find_packages

setup(
    name='hyperpytext',
    version='1.0',
    description = "A tool to create HyperPy applications",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'HyperPyText': ['templates/*.yaml'],
    },
    install_requires=[
        'Click',
        'PyYAML',
        'fastapi',
        'uvicorn',
    ],
    entry_points='''
        [console_scripts]
        hyperpytext=create-HyperPy-app:create_app
    ''',
)