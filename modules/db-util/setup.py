import setuptools

setuptools.setup(
    name='db-util',
    version='0.1.0',
    description='A simple package for DB connection.',
    author='venub',
    license='Apache License 2.0',
    author_email='venub755@gmail.com',
    py_modules=[
        'dbConnect', 
        'DbContextManager'
    ],
    install_requires=[
        'mysql-connector-python',
    ],
    classifiers=[
        'Development Status <IP_ADDRESS> 3 - Alpha',
        'Intended Audience <IP_ADDRESS> Developers',
        'License <IP_ADDRESS> OSI Approved <IP_ADDRESS> Apache Software License',
        'Programming Language <IP_ADDRESS> Python <IP_ADDRESS> 3',
    ]
)