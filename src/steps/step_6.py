from typing import Dict, Literal, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from components.chat_model import chat_model

class Delta(TypedDict):
    included: Literal[ 'Completely', 'Partially', 'Not at all' ]
    citation: Annotated[str, "Why the focus area is not completely present"]


prompt_template = PromptTemplate(
    template='''
    You will be given 2 stings.
    Site Document Content: This is the content is extracted from a document which contains details on several focus areas.
    Focus Area: This is a specific focus area.
    Given the Site Document Content and Focus Area, please evaluate strictly whether the given focus area is properly present or partiall present or not present at all.
    If the focus area is partially present, provide a one-liner comment on what is missing.
    If the focus area is not at all present or completely present, no need to provide any comment.

    Here is the Site Document Content
    {site_document_content}
    
    Focus Area
    {focus_area}
    ''',
    input_variables=['site_document_content', 'focus_area']
)


def step_6(state: State) -> Dict:
    '''
    
    '''
    
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    site_document_content = state.get('site_document_content')
    delta_table_as_df = state.get('delta_table_as_df')
    
    structured_model = chat_model.with_structured_output(schema=Delta)
    chain = prompt_template | structured_model

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        focus_areas = row.iloc[1].split(',')
        status, comments = [], []

        for focus_area in focus_areas:
            payload = { 'focus_area': focus_area, 'site_document_content': site_document_content }
            response = chain.invoke(payload)
            status.append( f'{focus_area}: {response.get("included")}' )
            if response.get('included') == 'Partially':
                comments.append(f'{focus_area}: {response.get("citation")}')
    
    delta_table_as_df.iloc[idx, 3] = "||".join(status)
    delta_table_as_df.iloc[idx, 4] = "||".join(comments)

    print('Step 6 Completed: Delta Table Filled with Required Data')

    return { 'delta_table_as_df': delta_table_as_df }
