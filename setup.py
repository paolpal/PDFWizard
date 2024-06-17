from setuptools import setup, find_packages

setup(
    name="pdfwizard",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "PyMuPDF",
        "PyMuPDFb",
        "pypdf",
        "tqdm",
    ],
    entry_points={
        'console_scripts': [
            'pdfwizard = pdfwizard.__main__:main',
        ],
    },
    author="Paolo Palumbo",
    author_email="paol.palumbo@gmail.com",
    description="A Python package for manipulating PDF files",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/paolpal/PDFWizard", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
