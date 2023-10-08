from setuptools import setup
import io


setup(name='LORIS',
      version='1.0',
      description='LORIS: A cancer immunotherapy response scoring system'
                  ' based on patient clinical features',
      long_description=io.open('README.md', encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      author='Tiangen Chang',
      author_email='changtiangen@gmail.com',
      packages=['LORIS'],
      license='GPLv3',
      install_requires=['numpy>=1.14.0',
                        'pandas>=0.24.2'],
      package_data={'LORIS': ['model_Params/LLR6_panCancer_Param.txt',
                              'model_Params/LLR6_panCancer_ORR_Table.txt',
                              'model_Params/LLR6_panCancer_PFS_Table.txt',
                              'model_Params/LLR6_panCancer_OS_Table.txt',
                              'model_Params/LLR5_panCancer_Param.txt',
                              'model_Params/LLR5_panCancer_ORR_Table.txt',
                              'model_Params/LLR5_panCancer_PFS_Table.txt',
                              'model_Params/LLR5_panCancer_OS_Table.txt',
                              'model_Params/LLR6_NSCLC_Param.txt',
                              'model_Params/LLR6_NSCLC_ORR_Table.txt',
                              'model_Params/LLR6_NSCLC_PFS_Table.txt',
                              'model_Params/LLR6_NSCLC_OS_Table.txt',
                              'model_Params/LLR5_NSCLC_Param.txt',
                              'model_Params/LLR5_NSCLC_ORR_Table.txt',
                              'model_Params/LLR5_NSCLC_PFS_Table.txt',
                              'model_Params/LLR5_NSCLC_OS_Table.txt'
                              ]},
      entry_points={'console_scripts': ['LORIS=LORIS.__main__:main']})