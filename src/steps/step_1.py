from io import StringIO
from typing import Dict, TypedDict, Annotated

import pandas as pd
from langchain_core.prompts import PromptTemplate

from state import State
from components.chat_model import chat_model
from components.parser import extract_pdf_elements


class RelevantRow(TypedDict):
    relevance: bool

prompt_template = PromptTemplate(
    template='''
    You will be given a single row of a table and a title.
    By looking at the row and title, you need to respond if the row is compleatly relevant to the title or not.
    Here is the row in html tag
    {row_as_html}
    Here is the title
    {title}
    ''',
    input_variables=['row_as_html', 'title']
)

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
    Then it will filter the rows in global sop list dataframe based on the site document title.
    '''
    global_sop_list_file_path = state.get('global_sop_list_file_path')
    site_document_file_path = state.get('site_document_file_path')

    global_sop_list_table_as_df = extract_global_sop_list_table_as_df_from_pdf(filepath=global_sop_list_file_path)
    site_document_title_table_as_df = extract_site_document_title_table_as_df_from_pdf(filepath=site_document_file_path)

    structured_model = chat_model.with_structured_output(schema=RelevantRow)
    chain = prompt_template | structured_model

    irrelevant_row_indices_in_global_sop_list_table_as_df = []
    for idx, row in global_sop_list_table_as_df.iterrows():
        row_as_html = row.to_frame().to_html(index=False)
        payload = { 'row_as_html': row_as_html, 'title': site_document_title_table_as_df.iloc[ 0, 1 ] }
        response = chain.invoke(payload)
        if response.get('relevance') is False:
            irrelevant_row_indices_in_global_sop_list_table_as_df.append(idx)

    filtered_global_sop_list_table_as_df = global_sop_list_table_as_df.drop(irrelevant_row_indices_in_global_sop_list_table_as_df)

    print("Step 1: Completed: Relevant Tables are extracted from Global SOP and Site Documents")

    return { 
        'global_sop_list_table_as_df': global_sop_list_table_as_df,
        'site_document_title_table_as_df': site_document_title_table_as_df,
        'filtered_global_sop_list_table_as_df': filtered_global_sop_list_table_as_df,
        'irrelevant_row_indices_in_global_sop_list_table_as_df': irrelevant_row_indices_in_global_sop_list_table_as_df
    }