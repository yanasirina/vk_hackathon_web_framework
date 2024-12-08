from setuptools import setup, find_packages


def main() -> None:
    setup(
        name='web',
        version='0.0.1',
        packages=find_packages(include=['web', 'web.*']),
        install_requires=[
            'gunicorn',
            'webob',
            'jinja2',
            'python-dotenv',
            'locust'
        ],
    )


if __name__ == '__main__':
    main()
