from setuptools import setup, find_packages

setup(
    name='scrape_latest_user_agent',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'httpx',
        'typed_argument_parser @ git+https://github.com/vphpersson/typed_argument_parser.git#egg=typed_argument_parser'
    ]
)
