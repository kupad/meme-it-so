from setuptools import find_packages, setup

setup(
    name='meme-it-so',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'wheel',
        'flask',
        'moviepy',
        'srt'
    ],
)
