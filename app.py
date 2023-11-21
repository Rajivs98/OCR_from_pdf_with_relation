import PyPDF2
# import tesseract
import re
import spacy

def extract_text_(pdf_path):
    # Open the PDF file in binary mode
    # text = ""
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)

        # Extract text from each page
        text = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            # page_text = page.get_object()
            print("page_text------>  ",page_text)
            # text += page_text
            text.append(page_text)

    # Close the PDF file
    print("text: ", text)
    f.close()
    # print("text after close", text)

    return text


def extract_data(text):
    #Define regular expressions for key data points
    invoice_number_regex = re.compile(r'Invoice\s+(.*)')
    date_regex = re.compile(r'Date\s+(.*)')
    vendor_regex = re.compile(r'Vendor\s+(.*)')
    customer_regex = re.compile(r'Customer Name\s+(.*)')
    product_regex = re.compile(r'Itemized Products\s+(.*)')
    quantity_regex = re.compile(r'Quantities\s+(.*)')
    price_regex = re.compile(r'Price\s+(.*)')
    total_regex = re.compile(r'Total \s+(.*)')

    # invoice_number_regex = re.findall('\b','Invoice Number')
    # date_regex = re.findall('\b','Date')
    # vendor_regex = re.findall('\b','Vendor')
    # customer_regex = re.findall('\b','Customer Name')
    # product_regex = re.findall('\b','Itemized Products')
    # quantity_regex = re.findall('\b','Quantities')
    # price_regex = re.findall('\b','Price')
    # total_regex = re.findall('\b','Total')

    # print("Ijsdkjfjgkjsgfkj", invoice_number_regex)

    # Extract key data points using regular expressions

    # invoice_number = invoice_number_regex.search(text).group(1)
    invoice_match = invoice_number_regex.search(text)
    if invoice_match:
        invoice_number = invoice_match.group(1)
    else:
        invoice_number = None
    date = date_regex.search(text)
    if date:
        date = date.group(1)
    else:
        date = None
    vendor = vendor_regex.search(text)
    if vendor:
        vendor = vendor.group(1)
    else:
        vendor = None
    customer = customer_regex.search(text)
    if customer:
        customer = customer.group(1)
    else:
        customer = None

    # Extract product details
    products = []
    for product_match in product_regex.finditer(text):
        product = product_match.group(1)
        quantity = quantity_regex.search(text).group(1)
        price = price_regex.search(text).group(1)
        products.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })

    # Extract total amount
    total = total_regex.search(text)
    if total:
        total = total.group(1)
    else:
        total = None


    # Organize data into a structured format
    extracted_data = {
    'invoice_number': invoice_number or '',
    'date': date or '',
    'vendor': vendor or '',
    'customer': customer or '',
    'products': products or [],
    'total': total or 0
    }


    return extracted_data

def extract_relationships(text):
    # Load a spacy model for relationship extraction
    nlp = spacy.load('en_core_web_sm')

    # Parse the text using spacy
    doc = nlp(text)

    # Identify relationships between entities
    relationships = []
    for sent in doc.sents:
        for chunk in sent.noun_chunks:
            if chunk.root.head == sent.root:
                relationships.append((chunk.root.text, sent.root.text))

##     return relationships

def main():
    pdf_path = 'ticket_refund.pdf'

      ##Extract text from the PDF file
    text = extract_text_(pdf_path)

    ## Extract key data points from the text
    extracted_data = extract_data(text)

    ## Extract relationships between extracted data points
    relationships = extract_relationships(text)

    ## Present extracted data and relationships in a structured format
    print('Extracted Data:')
    print(extracted_data)

    print('Relationships:')
    print(relationships)

if __name__ == '__main__':
    main()
