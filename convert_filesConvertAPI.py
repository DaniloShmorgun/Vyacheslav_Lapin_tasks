# import requests
import os
import cloudconvert

api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiM2M5ZDQyMjIyNWIwOTE3OWVlZTdmZDY1M2U5MmZkMTM4MzYxYmE3N2QxMTdlOWQ5MmJmMDliYjQ2Yzk4ZTNlOTI5ODQyYWNjNTE2ZWI3ZDAiLCJpYXQiOjE2NzcwNjQ4MzkuMzY0OTM3LCJuYmYiOjE2NzcwNjQ4MzkuMzY0OTM4LCJleHAiOjQ4MzI3Mzg0MzkuMzU3ODk0LCJzdWIiOiI2MjI1MjUyMSIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.j1xgi_EUErxV0ClHqD1QKeCVATsmwuP-ENOtRGzCEBgSel4FBeuDBw5sbwGOvaa-Xi_IhMIuCofthCo_SY-U86pZuLMtXZhKkhBkC2hdPQ15wNwcq_CD0hPAfWBUHX6DQE_qA3tkY9-9siZ0Ckfh1-OjkaIqs7CSFAtV3FYd2FWeB8ulq_actHsNGAEXKyUxGcqlj5xCqrTYwAoJWCThB2AhjTiifz9cl4XKMbgjwZxGl6dkmJn5Cs2N3f5oPUrUVj3ubEEMzdIrNNr9pXXeHYnQhxF0emrV-UvXeGz5D-whHw1XQ0shcwuTFsSOg9nTqL489nLuQcMUiawcppBiR0Ri7zaEcJGV4P0YVCboKCgOlizKgTvRZBJtsyI4u1GE96PKxA9eKG1XD7C_SfOmAjHK3jUnNH9B946_80GcuxGlS2U9FTyz6IlmHMn71TCSbD1PVjW1I1Hk0u97GhpWeYf3s_tKaW34O3DXomZBG0yaR6eysBbOcDeZLO9-M3NXK9-BQlFhA1CwjN3qHUrsp6x2SCWrOklz372VUWPCk0nKNGpChg3BAHs-CmSq7grzq1tYtTYu3MILAfkIy5j40-qJG3Mi59DPlLeY5OEdH3wuBVpUAye37p7YJxWwWTM2bbF9zj7t0CBOLG-q0BgshD73gjav9Vv8yBgRSxVNtYk'

cloudconvert.configure(api_key=api_key, sandbox=False)

input_format = 'xls'
output_format = 'xlsx'

job = cloudconvert.Job.create(payload={
    'tasks': {
        "upload": {
            "operation": "import/upload"
        },
        'convert-my-file': {
            'operation': "convert",
            'input': "upload",
            "input_format": "xls",
            'output_format': 'xlsx'
        },
        "export": {
            "operation": "export/url",
            "input": "convert-my-file",
            "inline": False,
            "archive_multiple_files": True
        }

    }
})

# t = cloudconvert.Job.all()
# for job in t:
#     print('\n', job)

input_folder = 'domestic_zones'
if not os.path.exists(input_folder):
    os.makedirs(input_folder)

file_names = os.listdir(input_folder)
sorted_file_names = sorted(file_names, key=lambda x: int(os.path.splitext(x)[0]))

for i in range(1, 20):
    job = cloudconvert.Job.create(payload={
    'tasks': {
        "upload": {
            "operation": "import/upload"
        },
        'convert-my-file': {
            'operation': "convert",
            'input': "upload",
            "input_format": "xls",
            'output_format': 'xlsx'
        },
        "export": {
            "operation": "export/url",
            "input": "convert-my-file",
            "inline": False,
            "archive_multiple_files": True
        }

        }
    })
    #### Upload

    upload_task_id = job['tasks'][0]['id']
    upload_task = cloudconvert.Task.find(id=upload_task_id)

    for filename in sorted_file_names[i]:
        if filename.endswith(f'.{input_format}'):
            print(os.path.join(input_folder,filename))
            res = cloudconvert.Task.upload(os.path.join(input_folder,filename), task=upload_task)
            res = cloudconvert.Task.find(id=upload_task_id)
            print(res)

    #### Convert

    convert_task_id = job['tasks'][1]['id']
    convert_task = cloudconvert.Task.find(id=convert_task_id)

    print('\n',convert_task)

    #### Download

    exported_url_task_id = job['tasks'][2]['id']
    res = cloudconvert.Task.wait(id=exported_url_task_id)  # Wait for job completion

    output_folder = 'domestic_zones2xlsx'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file = res.get("result").get("files")[0]
    res = cloudconvert.download(filename=os.path.join(output_folder,file['filename']), url=file['url'])
    print(res)