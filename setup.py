from distutils.core import setup

setup(
    name='Dcm2Bids',
    version='0.3.3dev',
    author='Christophe Bedetti',
    author_email='christophe.bedetti@criugm.qc.ca',
    packages=['dcm2bids'],
    scripts=['bin/dcm2bids'],
    url='https://github.com/cbedetti/Dcm2Bids',
    license='LICENSE.txt',
    description='Convert DICOM images to Brain Imaging Data Structure',
    long_description=open('README.md').read(),
    install_requires=[
        'dcmstack >= 0.7.0',
        'nibabel >= 2.0.0',
        'pydicom >= 0.9.7',
        'dcm2niibatch',
    ],
)
