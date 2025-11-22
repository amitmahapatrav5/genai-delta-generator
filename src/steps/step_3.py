from typing import Dict, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from utils import clean_df
from components.chat_model import chat_model


class RelevantPolicyDocument(TypedDict):
    relevant_existing_policy_document_titles: Annotated[str, "Relevant existing policy document titles separated by ','"]

prompt_template = PromptTemplate(
    template="""
    You will be given 2 strings

    existing_policy_document_titles: It is a string of policy document titles separated by ",".
    new_policy_document_title: It is a string of a single policy document title.
    
    Now you need to return a subset of existing_policy_document_titles separated by "," 
    which semantically match exactly same as the new_policy_document_title.
    
    Here is the existing policy document titles
    {existing_policy_document_titles}
    
    Here is the new policy document title
    {new_policy_document_title}
    
    Rules: Please provide entire title of the existing document not only the id or only the title.
    Example 'VI-301: Commercial Vehicle Insurance Package'
    """,
    input_variables=['existing_policy_document_titles', 'new_policy_document_title']
)


def step_3(state: State) -> Dict:
    '''
    This node filters the existing policy document titles in global sop list dataframe based on the site document title.
    '''
    
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    site_document_title_table_as_df = state.get('site_document_title_table_as_df')

    structured_model = chat_model.with_structured_output(RelevantPolicyDocument)
    chain = prompt_template | structured_model

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        existing_policy_document_titles = row.iloc[2].split(",")
        new_policy_document_title = site_document_title_table_as_df.iloc[0, 1]
        payload = { 'existing_policy_document_titles': existing_policy_document_titles , 'new_policy_document_title': new_policy_document_title }
        response = chain.invoke(payload)
        filtered_global_sop_list_table_as_df.iloc[ idx, 2 ] = response.get('relevant_existing_policy_document_titles')

    filtered_global_sop_list_table_as_df = clean_df(filtered_global_sop_list_table_as_df)
    print('Step 3 Completed: Global SOP Table Rows are filtered.')

    # Along with removing the filtered titles, I can store those titles in the state as well for audit
    return { 'filtered_global_sop_list_table_as_df': filtered_global_sop_list_table_as_df }