from distutils.core import setup

setup(
    name='Dcm2Bids',
    version='0.1.0',
    author='Christophe Bedetti',
    author_email='christophe.bedetti@criugm.qc.ca',
    packages=['dcm2bids'],
    scripts=['bin/dcm2bids'],
    url='https://github.com/cbedetti/Dcm2Bids',
    license='LICENSE.txt',
    description='Convert your DICOM nicely.',
    long_description=open('README.md').read(),
    install_requires=[
        "dcm2niix",
    ],
)
