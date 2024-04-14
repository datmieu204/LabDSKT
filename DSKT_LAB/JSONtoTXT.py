import json

json_file = 'E:/DSKT_LAB/AAAI.json'
txt_file = 'E:/DSKT_LAB/AAAI.txt'

fields = {
    'doc_name': 'title',
    'author': 'metadata',
}

body_field = 'body'

# body_fields = {
#     'title': 'Section',
#     'content': 'Content',
# }

tmp_title = []

def write_body(data, field, file, indent_level=0):
    indent = '  ' * indent_level
    
    if isinstance(data, list):
        for item in data:
            write_body(item, field, file, indent_level)
    elif isinstance(data, dict):
        if 'title' in data and 'content' in data:
            title = data['title']

            if title != 'References' and title in tmp_title:
                file.write(f"{indent}- {data['title']}")
                file.write(f"{indent}: {data['content']}\n")
                # file.write(f"{indent}- {body_fields['title']}: {data['title']}\n")
                # file.write(f"{indent}  {body_fields['content']}: {data['content']}\n")
                # for item in data['content']:
                #     file.write(f"{indent}  - {item}\n")
        else:
            for key, value in data.items():
                write_body(value, field, file, indent_level+1)

with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

text_data = json.dumps(data, indent=4, ensure_ascii=False)

check = False

if body_field in data:
    for paragraph in data[body_field]:
        # tmp_title.append(paragraph['title'])
        if paragraph['title'] == 'Abstract':
            check = True
        if check:
            tmp_title.append(paragraph['title'])

# if 'figures' in data:
#     for figure in data['figures']:
#         data['author'].append(figure['caption'])

with open(txt_file, 'w', encoding='utf-8') as file:
    for field in fields:
        if field in data:
            new_field = fields[field]
            file.write(f"- {new_field}: {data[field]}\n")

    if body_field in data:
        file.write("- plain_text:\n")
        write_body(data[body_field], body_field, file,  indent_level=1)



# print(tmp_title)
