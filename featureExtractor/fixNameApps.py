import os
from pathlib import Path

# specify the directory containing the benignApps and drebinApps folders
apkFolder = 'data/apks'

dir_path = os.path.dirname(os.path.realpath(__file__))
parent = Path(dir_path).parent
path = f'{parent}/{apkFolder}'
print('path', path)
bTrain = 1
bTest = 1
m = 1
name = 'app'
# loop through the benignApps and drebinApps folders
for dir_name, subdir_list, file_list in os.walk(path):
    for file_name in file_list:

        if file_name.endswith('.apk'):
            file_path = os.path.join(dir_name, file_name)
            if 'benignApps' in file_path:
                if 'train' in file_path:
                    new_file_name = f'{name}{bTrain}_B.apk'
                    bTrain += 1
                else:
                    new_file_name = f'{name}{bTest}_B.apk'
                    bTest += 1
            else:
                new_file_name = f'{name}{m}_M.apk'
                m += 1

            new_file_path = os.path.join(dir_name, new_file_name)
            print('new_file_name', new_file_name)
            os.rename(file_path, new_file_path)
