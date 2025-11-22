from io import StringIO
from typing import Dict

import pandas as pd

from state import State
from components.parser import extract_pdf_elements


def extract_global_sop_list_table_as_df_from_pdf(filepath):
    '''
    Global SOP PDF has exactly 3 tables.
    1. Title Table
    2. SOP List Table which might span through multiple pages.
    3. Document Versioning Table

    Table# 2 is the table we need to extract.
    '''
    elements = extract_pdf_elements(filepath)
    global_sop_list_table_element = elements[0].to_dict() # this hardcoded value will be removed in future
    global_sop_list_table_as_html = global_sop_list_table_element['metadata']['text_as_html']
    global_sop_list_table_as_df = pd.read_html(StringIO(global_sop_list_table_as_html))[0]
    return global_sop_list_table_as_df

def extract_site_document_title_table_as_df_from_pdf(filepath):
    '''
    Site Document PDF has exactly 4 parts
    1. Title Table
    2. Table of Contents
    3. Section wise content
    4. Document Versioning Table

    Table# 1 is the table we need to extract.
    '''
    elements = extract_pdf_elements(filepath)
    site_document_title_table_element = elements[0].to_dict()
    site_document_title_table_as_html = site_document_title_table_element['metadata']['text_as_html']
    site_document_title_table_as_df = pd.read_html(StringIO(site_document_title_table_as_html))[0]
    return site_document_title_table_as_df

def step_1(state: State) -> Dict:
    '''
    This function will extract the global sop list table and site document title table from the pdf files.
    Then it will convert the global sop list table and site document title table into pandas dataframes so table manipulation can be done easily.
    '''
    global_sop_list_file_path = state.get('global_sop_list_file_path')
    site_document_file_path = state.get('site_document_file_path')

    global_sop_list_table_as_df = extract_global_sop_list_table_as_df_from_pdf(filepath=global_sop_list_file_path)
    site_document_title_table_as_df = extract_site_document_title_table_as_df_from_pdf(filepath=site_document_file_path)

    print("Step 1: Completed: Relevant Tables are extracted from Global SOP and Site Documents")

    return { 
        'global_sop_list_table_as_df': global_sop_list_table_as_df,
        'site_document_title_table_as_df': site_document_title_table_as_df,
    }