from pdfminer.high_level import extract_text
import spacy

def extract_data(text):
    # Splitting the text by lines for simpler processing
    lines = text.split('\n')

    # Initialize variables to store extracted data
    extracted_data = {
        'invoice_number': None,
        'date': None,
        'vendor': None,
        'customer': None,
        'products': [],
        'total': None
    }

    # Define keywords for extraction
    keywords_mapping = {
        'Invoice Number': 'invoice_number',
        'Date': 'date',
        'Vendor/Supplier Name': 'vendor',
        'Customer Name': 'customer',
        'Itemized Products': 'products',
        'Total Amount': 'total'
    }

    current_category = None

    # Iterate through each line to extract data
    for line in lines:
        for keyword, category in keywords_mapping.items():
            if keyword in line:
                current_category = category
                break

        # Process the line based on the identified category
        if current_category:
            if current_category == 'products':
                # For products, assuming a specific format (adjust as per your PDF structure)
                product_info = line.split(',')
                if len(product_info) >= 3:
                    product = product_info[0].strip()
                    quantity = product_info[1].strip()
                    price = product_info[2].strip()
                    extracted_data['products'].append({
                        'product': product,
                        'quantity': quantity,
                        'price': price
                    })
            else:
                value = line.replace(keyword, '').strip()
                extracted_data[current_category] = value

    return extracted_data

def extract_relationships(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    relationships = []
    for sent in doc.sents:
        for chunk in sent.noun_chunks:
            if chunk.root.head == sent.root:
                relationships.append((chunk.root.text, sent.root.text))
    return relationships

def main():
    pdf_path = 'PO2.pdf'
    text = extract_text(pdf_path)
    extracted_data = extract_data(text)
    relationships = extract_relationships(text)

    print('Extracted Data:')
    print(extracted_data)

    print('Relationships:')
    print(relationships)

if __name__ == '__main__':
    main()
