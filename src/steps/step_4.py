from typing import Dict, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from utils import clean_df
from components.chat_model import chat_model


class RelevantFocusArea(TypedDict):
    relevant_focus_areas: Annotated[str, "Relevant focus areas separated by ','"]

prompt_template = PromptTemplate(
    template='''
    You will be given 2 strings 
    relevant_policy_document_titles: It is basically a list of policy documents, separated by ","
    list_of_focus_areas: It is a list of focus areas. This list may include some focus areas which are not at all related to any document titles.
    Now you need to return a subset of list_of_focus_areas, MUST be separated by comma(",") 
    which is relevant to atleaset one of the relevant policy documents.
    Here is the list of relevant policy document titles
    {relevant_policy_document_titles}
    Here is the list of focus areas
    {focus_areas}
    ''',
    input_variables=['relevant_policy_document_titles', 'focus_areas']
)

def step_4(state: State) -> Dict:
    '''
    This node filters the focus areas in global sop list dataframe based on the relevant policy document titles.
    '''

    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    
    structured_model = chat_model.with_structured_output(RelevantFocusArea)
    chain = prompt_template | structured_model

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        focus_areas, relevant_policy_document_titles = row.iloc[1], row.iloc[2]
        payload = { 'relevant_policy_document_titles': relevant_policy_document_titles , 'focus_areas': focus_areas }
        response = chain.invoke(payload)
        filtered_global_sop_list_table_as_df.iloc[ idx, 1 ] = response.get('relevant_focus_areas')

    filtered_global_sop_list_table_as_df = clean_df(filtered_global_sop_list_table_as_df)
    print('Step 4 Completed: Global SOP Document Titles are filtered.')

    # Along with removing the filtered focus areas, I can store those in the state as well for audit
    return { 'filtered_global_sop_list_table_as_df': filtered_global_sop_list_table_as_df }