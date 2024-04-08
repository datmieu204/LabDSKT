import glob
import os
import PyPDF2
from xml.etree.ElementTree import Element, SubElement, tostring
import re
import string

# Nguyen Tuan Dat

def extract_abstract_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        abstract_text = ""

        for page in pdf_reader.pages:
            abstract_text += page.extract_text().strip()

        abs_marker = r'[aA][bB][sS][tT][rR][aA][cC][tT]'
        abs_match = re.search(abs_marker, abstract_text)
        abs_index = 0

        if abs_match:
            abs_index = abs_match.end().real

        end_marker = r'1\.?\s?[Ii][Nn][Tt][Rr][Oo][Dd][Uu][Cc][Tt][Ii][Oo][Nn]'
        end_match = re.search(end_marker, abstract_text)
        end_index = len(abstract_text)

        if end_match:
            end_index = end_match.start().real
    

        abstract_text = abstract_text[abs_index:end_index].strip()
        abstract_text = re.sub(r'[^\x20-\x7E]', '', abstract_text)

        return abstract_text


def extract_section_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        section_text = ""

        for page in pdf_reader.pages:
            section_text += page.extract_text()

        end_marker = r'[rR][eE][fF][eE][rR][eE][nN][cC][eE][sS]'
        end_match = re.search(end_marker, section_text)
        end_index = len(section_text)

        if end_match:
            end_index = end_match.start().real

        section_text = section_text[:end_index].strip()

        return section_text


def extract_sections(section_text):
    section_pattern = r'^\d+(\.?\s)[A-Z][a-zA-Z]*'
    section_matches = re.finditer(section_pattern, section_text, re.MULTILINE)
    sections = []

    section_start = None  # Lưu trữ chỉ số bắt đầu của mục hiện tại

    for match in section_matches:
        if section_start is not None:
            section_end = match.start().real
            section_content = section_text[section_start:section_end].strip()
            section_content = re.sub(r'[^\x20-\x7E]', '', section_content)
            sections.append((section_title, section_content))

        section_title = match.group(0)    
        section_title = re.sub(r'[^\x20-\x7E]', '', section_title)
        # Lưu trữ chỉ số bắt đầu của mục mới
        section_start = match.end().real

    # Lưu phần cuối
    if section_start is not None:
        section_title = match.group(0)
        end_marker = r'[aA][cC][kK][nN][oO][wW][lL][eE][dD][gG](e?)[mM][eE][nN][tT](s?)'
        end_match = re.search(end_marker, section_text)
        end_index = len(section_text)   

        if end_match:
            end_index = end_match.start().real

        section_content = section_text[section_start:end_index].strip()
        section_content = re.sub(r'[^\x20-\x7E]', '', section_content)
        section_title = re.sub(r'[^\x20-\x7E]', '', section_title)
        sections.append((section_title, section_content))

    return sections



def extract_acknowledgement_text(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        ack_text = ""

        for page in pdf_reader.pages:
            ack_text += page.extract_text()

        ack_marker = r'[aA][cC][kK][nN][oO][wW][lL][eE][dD][gG](e?)[mM][eE][nN][tT](s?)'
        ack_match = re.search(ack_marker, ack_text)
        ack_index = 0

        if ack_match:
            ack_index = ack_match.end().real

        end_marker = r'[rR][eE][fF][eE][rR][eE][nN][cC][eE][sS]'
        end_match = re.search(end_marker, ack_text)
        end_index = len(ack_text)
        if end_match:
            end_index = end_match.start().real

        ack_text = ack_text[ack_index:end_index].strip()

        return ack_text

def convert_pdf_to_xml(pdf_path, xml_path):
    root = Element('PAPER')

    abstract_element = SubElement(root, 'ABSTRACT')

    abstract_text = extract_abstract_text(pdf_path)
    section_text = extract_section_text(pdf_path)

    abstract_sentences = abstract_text.split('. ')
    section_sentences = section_text.split('. ')
    sid_index = 0
    
    # Extract and add abstract sentences
    for i, sentence in enumerate(abstract_sentences, start=1):
        sentence = ''.join(filter(lambda x: x in string.printable, sentence))
        sentence = sentence.strip()
        sid_index = i
        s_element = SubElement(abstract_element, 'S', sid=str(sid_index), ssid=str(i))
        s_element.text = sentence

    # Extract and add sections
    sections = extract_sections(section_text)
    len_section = 0
    for i, (section_title, section_content) in enumerate(sections, start=len(abstract_sentences)+1):
        number = i-len(abstract_sentences)
        section_element = SubElement(root, 'SECTION', title=section_title , number=str(number))
        section_sentences = section_content.split('. ')
        for j, sentence in enumerate(section_sentences, start=1):
            len_section += 1
            sid_index += 1
            sentence = ''.join(filter(lambda x: x in string.printable, sentence))
            sentence = sentence.strip()
            s_element = SubElement(section_element, 'S', sid=str(sid_index), ssid=str(j))
            s_element.text = sentence

    # Acknowledgement or Acknowledgments
    ack_element = SubElement(root, 'SECTION', title='Acknowledgement' or 'Acknowledgments')
    ack_text = extract_acknowledgement_text(pdf_path)
    ack_sentences = ack_text.split('. ')

    for i, sentence in enumerate(ack_sentences, start=len_section+2):
        sentence = ''.join(filter(lambda x: x in string.printable, sentence))
        sentence = sentence.strip()
        id = (i-len_section-1)
        s_element = SubElement(ack_element, 'S', sid=str(i), ssid=str(id))
        s_element.text = sentence

    xml_content = tostring(root, encoding='utf-8')

    with open(xml_path, 'wb') as xml_file:
        xml_file.write(xml_content)

# # Test
# pdf_path = 'E:/DSKT_LAB/LongSumm/output_PDF_abstract/0_100/1050101.pdf'
# xml_path = 'E:/DSKT_LAB/test.xml'
# convert_pdf_to_xml(pdf_path, xml_path)

folder_path = 'E:/DSKT_LAB/LongSumm/output_PDF_extract'
folder_xml_path = 'E:/DSKT_LAB/LongSumm/output_XML_extract'

pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))

for pdf_file in pdf_files:
    pdf_file_name = os.path.basename(pdf_file)
    xml_file_name = os.path.splitext(pdf_file_name)[0] + '.xml'
    xml_file = os.path.join(folder_xml_path, xml_file_name)

    try:
        convert_pdf_to_xml(pdf_file, xml_file)
        print(f'Converted {pdf_file_name} to {xml_file_name}')
    except Exception as e:
        print(f'Failed to convert {pdf_file_name} to {xml_file_name}')
        print(e)




