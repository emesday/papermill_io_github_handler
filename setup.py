from setuptools import setup

setup(
    name="papermill_io_github_handler",
    version="0.0.1",
    url="https://github.com/mskimm/papermill_io_github_handler.git",
    author="Min Seok Kim",
    author_email="mskim.org@gmail.com",
    description="A Papermill IO for Github API v3.",
    packages=['papermill_io_github_handler'],
    install_requires=['requests'],
    entry_points={"papermill.io": ["github+https://=papermill_io_github_handler:GitHubHandler"]},
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
