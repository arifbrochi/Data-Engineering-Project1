import pandas as pd
import sys
import os
import json
import re
import glob
# getting column names
def get_column_names(schemas,ds_name):
    column_details=schemas[ds_name]
    return [col['column_name'] for col in column_details]

#reading csv files
def read_csv(file, schemas):
    file_path_list = re.split('[/\\\\]', file)
    ds_name = file_path_list[-2]
    file_name = file_path_list[-1]
    columns = get_column_names(schemas, ds_name)
    df = pd.read_csv(file, names=columns)
    return df

#converting csv into json
def to_json(df, tgt_base_dir, ds_name, file_name):
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    os.makedirs(f'{tgt_base_dir}/{ds_name}', exist_ok=True)
    df.to_json(
        json_file_path,
        orient='records',
        lines=True
    )

    #main file converter logic
def file_converter(src_base_dir, tgt_base_dir, ds_name):
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*')

    for file in files:
        df = read_csv(file, schemas)
        file_name = re.split('[/\\\\]', file)[-1]
        new_file_name=file_name.split('.')[0]
        to_json(df, tgt_base_dir, ds_name, new_file_name)

        #processing files
def process_files(ds_names=None):
    src_base_dir = os.environ.get('src_base_dir')
    tgt_base_dir = os.environ.get('tgt_base_dir')
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        print(f'Processing {ds_name}')
        file_converter(src_base_dir, tgt_base_dir, ds_name)

        #invoking process files function


if __name__=='__main__':
   if len(sys.argv)==2: 
     ds_names=json.loads(sys.argv[1])        
     process_files(ds_names)
   else:
    process_files()
