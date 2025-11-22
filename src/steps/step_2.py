from typing import Dict, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from components.chat_model import chat_model

class RelevantPolicyDocument(TypedDict):
    relevant_existing_policy_document_titles: str

prompt_template = PromptTemplate(
    template='''
    You will be given 2 strings 
    existing_policy_document_titles: It is basically a list of policy documents which already exists.
    new_policy_document_title: Title of the new policy document.
    Now you need to return a subset of existing_policy_document_titles separated by "," 
    which match exactly same as the new_policy_document_title semantically.
    Here is the existing policy document titles
    {existing_policy_document_titles}
    Here is the new policy document title
    {new_policy_document_title}
    Rules: Please provide entire title of the existing document not only the id or only the title.
    Example 'VI-301: Commercial Vehicle Insurance Package'
    ''',
    input_variables=['existing_policy_document_titles', 'new_policy_document_title']
)

def step_2(state: State) -> Dict:
    '''
    This function filter outs the Column 3 of every row in the filtered global sop list table dataframe in Step 1
    and updates it with the relevant existing policy document titles.
    '''
    
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    site_document_title_table_as_df = state.get('site_document_title_table_as_df')

    structured_model = chat_model.with_structured_output(RelevantPolicyDocument)
    chain = prompt_template | structured_model

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        payload = { 'existing_policy_document_titles': row.iloc[2] , 'new_policy_document_title': site_document_title_table_as_df.iloc[0, 1] }
        response = chain.invoke(payload)
        filtered_global_sop_list_table_as_df.iloc[ idx, 2 ] = response.get('relevant_existing_policy_document_titles')
    

    print('Step 2 Completed: Global SOP Table Rows are filtered.')

    # Along with removing the filtered titles, I can store those titles in the state as well for audit
    return { 'filtered_global_sop_list_table_as_df': filtered_global_sop_list_table_as_df }