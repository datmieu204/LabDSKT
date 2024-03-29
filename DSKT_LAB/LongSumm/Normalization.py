
import json
import os

json_folder = 'E:\\DSKT_LAB\\LongSumm\\output_JSON\\'

txt_folder = 'E:\\DSKT_LAB\\LongSumm\\text\\'

fields = ['id', 'title', 'authors', 'abstractText', 'references', 'sections']

for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
       
        json_file_path = os.path.join(json_folder, filename)
        txt_file_path = os.path.join(txt_folder, filename.replace('.json', '.txt'))

        # Đọc
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Ghi
        with open(txt_file_path, 'w', encoding='utf-8') as file:
            for field in fields:
                if field in data:
                    file.write(f"{field}: {data[field]}\n")
