from setuptools import setup, find_packages

setup(
    name='jupyterhub-charliecloudspawner',
    version='0.0.1',
    description='Dummy Authenticator for JupyterHub',
    url='https://github.com/yuvipanda/jupyterhub-dummyauthenticator',
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='3 Clause BSD',
    packages=find_packages(),
    entrypoints={
        'console_scripts': [
            'charliecloud-singleuser=charliecloud.singleuser:main'
        ]
    }
)
