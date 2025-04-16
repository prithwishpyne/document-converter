import fitz
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    pdf_document = fitz.open(pdf_path)
    
    for page in pdf_document:
        text += page.get_text()
    
    pdf_document.close()
    return text

def process_text(text):
    HEADER_PATTERN = r'^\d+\.\s*[A-Z][A-Z\s]+\s*$'
    SUBSECTION_PATTERN = r'^\d+(\.\d+)+\.?\s'
    # BULLET_PATTERN = r'^\s*(?:[•\-\*\+\u2022\u2023\u25E6|||]\s+|\d+[\).]\s+|[a-zA-Z][\).]\s+).*'
    BULLET_PATTERN = r'^\s*(?:[•\-|||]\s+|\d+[).\]]\s+|[a-zA-Z][).\]]\s+).*'
    SENTENCE_END_PATTERN = r'[.!?]$'

    lines = text.split('\n')
    processed_lines = []
    current_indent = 0
    in_paragraph = False
    current_paragraph = []

    for line in lines:
        # Skip empty lines and page numbers
        if not line.strip() or re.match(r'^\d+$', line.strip()):
            if in_paragraph and current_paragraph:
                processed_lines.append('\t' * (current_indent + 1) + ' '.join(current_paragraph))
                current_paragraph = []
                in_paragraph = False
            if not line.strip():  # If page number, skip and move to next line of data
                pass
            continue

        line = line.strip()
        if re.match(HEADER_PATTERN, line):
            if in_paragraph and current_paragraph:
                processed_lines.append('\t' * (current_indent + 1) + ' '.join(current_paragraph))
                current_paragraph = []
            in_paragraph = False
            current_indent = 0
            processed_lines.append(line)

        elif re.match(SUBSECTION_PATTERN, line):
            
            if in_paragraph and current_paragraph:
                processed_lines.append('\t' * (current_indent + 1) + ' '.join(current_paragraph))
                current_paragraph = []
            in_paragraph = False
            # Extract the subsection level f
            section_parts = re.findall(r'\d+', line)
            current_indent = len(section_parts) - 1  # Indentation based on section depth
            processed_lines.append('\t' * current_indent + line)

        # Handle bullet points
        elif re.match(BULLET_PATTERN, line):
            if in_paragraph and current_paragraph:
                processed_lines.append('\t' * (current_indent + 1) + ' '.join(current_paragraph))
                current_paragraph = []
            in_paragraph = False
            
            bullet_removed_line = re.sub(r'^s*(?:[•\-|||]\s+|\d+[).\]]\s+|[a-z][).\]]\s+)', '', line)
            processed_lines.append('\t' * (current_indent + 2) + '-> ' + bullet_removed_line.strip())

        else:
            if line.endswith('-'):
                current_paragraph.append(line[:-1])
            else:
                current_paragraph.append(line)
                if re.search(SENTENCE_END_PATTERN, line):
                    if in_paragraph or current_paragraph:
                        processed_lines.append('\t' * (current_indent + 1) + ' '.join(current_paragraph))
                        current_paragraph = []
                        in_paragraph = False
                else:
                    in_paragraph = True

    return '\n'.join(processed_lines)

def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    pdf_path = 'Labour Act.pdf'
    output_path = 'output.txt'  # File will be created in the backend directory
    
    raw_text = extract_text_from_pdf(pdf_path)
    
    processed_text = process_text(raw_text)

    save_text_to_file(processed_text, output_path)
    
    print(f"Text extracted and saved to {output_path}")

if __name__ == "__main__":
    main()