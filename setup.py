from setuptools import setup



setup(

    name='mitmTool',

    version='1.0',

    py_modules=['mitmTool'],

    install_requires=[],

    entry_points={

        'console_scripts': [

            'mitmTooll=mitmTool:main',

        ],

    },

)

