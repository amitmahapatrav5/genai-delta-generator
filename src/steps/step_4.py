from typing import Dict

from state import State
from components.parser import extract_pdf_elements


# Another function similar to this is writtten in step 1. I need to make this DRY.
def extract_site_document_content_from_pdf(filepath):
    '''
    Site Document PDF has exactly 4 parts
    1. Title Table
    2. Table of Contents
    3. Section wise content
    4. Document Versioning Table

    Point# 3 is the content we need to extract.
    '''
    elements = extract_pdf_elements(filepath)
    site_document_content_element = elements[2: ]
    site_document_content = '\n'.join([element.text for element in site_document_content_element])
    return site_document_content

def step_4(state: State) -> Dict:
    # In here, I can perform some more cleaning and chunking of the content.
    site_document_content = extract_site_document_content_from_pdf(state.get('site_document_file_path'))

    print('Step 4 Completed: Site Document Content extracted.')

    return { 'site_document_content': site_document_content }