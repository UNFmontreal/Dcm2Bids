from distutils.core import setup

setup(
    name='Dcm2Bids',
    version='0.1.0',
    author='Christophe Bedetti',
    author_email='christophe.bedetti@criugm.qc.ca',
    packages=['dcm2bids', 'dcm2bids.test'],
    scripts=['bin/dcm2bids.py'],
    url='', #TODO
    license='LICENSE.txt',
    description='Convert your DICOM nicely.',
    long_description=open('README.txt').read(),
    install_requires=[
        "nibabel",
    ],
)
