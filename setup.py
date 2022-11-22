from pathlib import Path
from setuptools import setup


readme_file = Path(__file__).parent.resolve() / 'README.md'
readme_contents = readme_file.read_text()

setup(
    name='my-py-opt',
    version="0.2",
    description='Lightweight optimization library',
    url='https://github.com/Myoldmopar/MyPyOpt',
    license='UnlicensedForNow',
    packages=[
        'mypyopt', 'mypyopt.demos.plot_example', 'mypyopt.demos.pretend_energyplus', 'mypyopt.demos.wall_temperature'
    ],
    package_data={
        'mypyopt.demos.pretend_energyplus': ['in_template.json'],
    },
    include_package_data=True,
    long_description=readme_contents,
    long_description_content_type='text/markdown',
    author="Edwin Lee",
    install_requires=[],
)
