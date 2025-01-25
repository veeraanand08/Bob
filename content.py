import spacy
import fitz  # PyMuPDF

# Load spaCy's pre-trained model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""

    # Loop through each page of the PDF and extract text
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # Extract text from the page
    
    return text

# Function to extract important topics using Named Entity Recognition
def extract_important_entities(text):
    # Process the text with spaCy's NLP pipeline
    doc = nlp(text)

    # Extract named entities (e.g., organizations, dates, important terms)
    entities = set()
    for ent in doc.ents:
        entities.add(ent.text.strip())

    return list(entities)

# Combine both functions to generate the study list
def generate_study_list(pdf_file):
    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_file)

    # Extract important entities (e.g., topics, keywords)
    important_entities = extract_important_entities(text)

    # Return a list of topics to study
    return important_entities

# Example usage
#pdf_file = "study_guide.pdf"
#study_list = generate_study_list(pdf_file)
