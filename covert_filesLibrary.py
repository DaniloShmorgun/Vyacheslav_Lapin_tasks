import os 
import pandas as pd

output_folder = 'domestic'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

input_folder = 'domestic_zones'
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

file_names = os.listdir(input_folder)
sorted_file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0]))

# Define the input XLS file path
input_file_path = 'path/to/input_file.xls'

# Define the output XLSX file path
output_file_path = 'path/to/output_file.xlsx'

for filename in sorted_file_names[:50]:
    df = pd.read_excel(os.path.join(input_folder, filename), engine='openpyxl')
    df.to_excel(os.path.join(output_folder, filename +'x'), index=False)