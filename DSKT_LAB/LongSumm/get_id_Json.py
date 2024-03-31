import json
import glob

json_files = glob.glob('E:/DSKT_LAB/LongSumm/abstractive_summaries/by_clusters/1200_1300/*.json')

# Lọc id để trích xuất những file PDF còn thiếu

for file_path in json_files:
    with open(file_path) as f:
        data = json.load(f)

    field1 = data['id']
    
    print("File:", file_path)
    print("Field 1:", field1)
    print()
