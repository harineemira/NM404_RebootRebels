from zipfile import ZipFile 
import os
import sys
from pathlib import Path

# specifying the zip file name 
path1=r"C:\Users\pahar\SAR"
path2=sys.argv[1]
file_name=path1+"\\"+path2

# opening the zip file in READ mode 
with ZipFile(file_name, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir() 
    # extracting all the files 
    print('Extracting all the files now...') 
    zip.extractall() 
    print('Done!')
extract = Path(file_name).stem
add_string=".SAFE"
extract += add_string
print(extract+"\preview\quick-look.png")  
# Output img with window name as 'image'