# DAT MIEU 

# import json
# from pathlib import Path
# from science_parse_api.api import parse_pdf

# host = 'http://localhost'
# port = '8080'

# # Đường dẫn file PDF
# pdf_dir = Path(r'E:\DSKT_LAB\LongSumm\output_PDF\100_200\414696.pdf')

# # PDF -> JSON
# parsed_pdf = parse_pdf(host, pdf_dir, port) 

# # Đường dẫn file JSON 
# output_dir = Path(r'E:\DSKT_LAB\LongSumm\output_JSON')
# output_filename = '414696.json'

# output_dir.mkdir(parents=True, exist_ok=True)

# output_path = output_dir / output_filename

# with open(output_path, 'w', encoding='utf-8') as f:
#     json.dump(parsed_pdf, f, ensure_ascii=False, indent=4)

# print(f'Kết quả đã được lưu vào {output_path}')

import json
from pathlib import Path
from science_parse_api.api import parse_pdf

# Địa chỉ Server
host = 'http://localhost'
port = '8080'

# Đường dẫn file PDF
pdf_dir = Path(r'E:\DSKT_LAB\LongSumm\output_PDF\1500_1600')

# Đường dẫn file JSON 
output_directory = Path(r'E:\DSKT_LAB\LongSumm\output_JSON')

output_directory.mkdir(parents=True, exist_ok=True)

for pdf_file in pdf_dir.glob('*.pdf'):
    # PDF -> JSON
    parsed_pdf = parse_pdf(host, pdf_file, port) 

    output_filename = pdf_file.stem + '.json'

    output_path = output_directory / output_filename

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(parsed_pdf, f, ensure_ascii=False, indent=4)

    print(f'Kết quả đã được lưu vào {output_path}')
