import setuptools


setuptools.setup(
    name='Mink',
    version='0.0.1',
    author='Elliot Wadge',
    author_email='ewadge@sfu.ca',
    description='Package containing useful functions for scientific analysis',
    url='https://github.com/Elliot-Wadge/Mink',
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=['numpy', 'plotly', 'scipy'],
)
