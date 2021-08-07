from distutils.core import setup
setup(
  name = 'sparkreader_lib',         # package folder (MyLib)
  packages = ['sparkreader_lib'],   #  same as "name"
  version = '0.1',      # 
  license='MIT',        # license  here: https://help.github.com/articles/licensing-a-repository
  description = 'reads json and csv files, performs data quality checks',   
  author = 'Adam Suhajda',                   
  author_email = 'adamsuhajdafx@gmail.com',      
  url = 'https://github.com/Suhaada/python_spark_reader_library',   
  download_url = 'https://github.com/Suhaada/python_spark_reader_library/archive/refs/tags/v_01.tar.gz',    
  keywords = ['SPARK', 'DATA QUALITY', 'READ DATA'],   
  install_requires=[            
          'pyspark'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
