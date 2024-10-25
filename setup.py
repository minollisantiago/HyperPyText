from setuptools import setup

setup(
    name='hyperpytext',
    version='1.0',
    description = "A tool to create HyperPy applications",
    packages=['hyperpytext'],
    include_package_data=True,
    package_data={
        'hyperpytext': ['templates/**/*.yaml'],
    },
    install_requires=[
        'Click',
        'PyYAML',
        'fastapi',
        'uvicorn',
    ],
    entry_points={
        'console_scripts': [
            'create-hyperpy-app=hyperpytext.__main__:create_app',
        ],
    },

)
