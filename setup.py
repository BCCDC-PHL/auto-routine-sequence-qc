from setuptools import setup, find_namespace_packages

setup(
    name='auto-routine-sequence-qc',
    version='0.1.0-alpha',
    packages=find_namespace_packages(),
    entry_points={
        "console_scripts": [
            "auto-routine-sequence-qc = auto_routine_sequence_qc.__main__:main",
        ]
    },
    scripts=[],
    package_data={
    },
    install_requires=[
    ],
    description=' Automated routine quality control analysis of arbitrary microbial sequence data',
    url='https://github.com/BCCDC-PHL/auto-routine-sequence-qc',
    author='Dan Fornika',
    author_email='dan.fornika@bccdc.ca',
    include_package_data=True,
    keywords=[],
    zip_safe=False
)
