from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='gemini_pro_rpg',
    version='1.6',
    packages=find_packages(),
    url='https://github.com/GlobalCreativeApkDev/gemini-pro-rpg',
    license='MIT',
    author='GlobalCreativeApkDev',
    author_email='globalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the role-playing game (RPG) '
                'with Gemini Pro integrated into it.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={
        "console_scripts": [
            "gemini_pro_rpg=gemini_pro_rpg.main:main",
        ]
    }
)