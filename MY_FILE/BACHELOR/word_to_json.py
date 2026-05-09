from docx import Document
from docx.opc.constants import RELATIONSHIP_TYPE as RT
import json

def get_hyperlink_target(paragraph):
    """Extracts the URL from a paragraph if it contains a hyperlink."""
    for rel in paragraph.part.rels.values():
        if rel.reltype == RT.HYPERLINK:
            return rel.target
    return "#"

def process_word_file(file_path):
    doc = Document(file_path)
    all_data = []
    current_item = None
    
    # Get all paragraphs
    paras = doc.paragraphs
    
    i = 0
    while i < len(paras):
        line = paras[i].text.strip()
        
        if not line:
            i += 1
            continue

        # TRIGGER: New Record
        if "Independent provider" in line or "Provided by university" in line:
            if current_item:
                all_data.append(current_item)
            current_item = {
                "UNIVERSITY": "Unknown",
                "SCHOLARSHIP": "Unknown",
                "AMOUNT": "Unknown",
                "DEADLINE": "Unknown",
                "LOCATION": "Unknown",
                "LINK": "#"
            }
            i += 1
            continue

        if current_item is None:
            i += 1
            continue

        # Extract Amount
        if any(x in line for x in ["INR", "USD", "GBP", "EUR", "benefits"]):
            current_item["AMOUNT"] = line

        # Extract Deadline
        elif line.lower() == "deadline":
            if i + 1 < len(paras):
                current_item["DEADLINE"] = paras[i+1].text.strip()
                i += 1

        # Extract University, Location, and HYPERLINK
        elif "Read more about eligibility" in line:
            # Look for the hidden URL in this specific paragraph
            current_item["LINK"] = get_hyperlink_target(paras[i])
            
            if i + 1 < len(paras):
                current_item["UNIVERSITY"] = paras[i+1].text.strip()
            if i + 2 < len(paras):
                current_item["LOCATION"] = paras[i+2].text.strip()
            i += 2

        # Extract Scholarship Name (If we have a deadline but no name yet)
        elif current_item["SCHOLARSHIP"] == "Unknown":
            if line not in ["Grant", "Merit-based", "Need-based", "Deadline"]:
                current_item["SCHOLARSHIP"] = line

        i += 1

    if current_item:
        all_data.append(current_item)

    # Save to JSON
    with open('final_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)

    print(f"Success! Processed {len(all_data)} records with links from Word.")

# Run the script
process_word_file('data.docx')