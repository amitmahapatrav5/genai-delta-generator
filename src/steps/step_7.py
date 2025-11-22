from typing import Dict, Literal, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from components.chat_model import chat_model

class Delta(TypedDict):
    status: Annotated[
        Literal[ 'Completely', 'Partially', 'Not at all' ], 
        "Whether the focus area is completely present or partially present or not present at all"
    ]
    comments: Annotated[str, "Why the focus area is not completely present"]


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


def step_7(state: State) -> Dict:
    '''
    This node will iterate each row of the filtered_global_sop_list_table_as_df
    And for each row, it will iterate each focus area 
    And evaluate whether the focus area is completely present or partially present or not present at all in the site_document_content.
    '''
    
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    site_document_content = state.get('site_document_content')
    delta_table_as_df = state.get('delta_table_as_df')
    
    structured_model = chat_model.with_structured_output(schema=Delta)
    chain = prompt_template | structured_model

    # This is for error handling
    if filtered_global_sop_list_table_as_df.empty:
        print("filtered_global_sop_list_table_as_df is empty. Skipping step 7 processing.")
        return { 'delta_table_as_df': delta_table_as_df }

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        focus_areas = row.iloc[1].split(',')
        status, comments = [], []

        for focus_area in focus_areas:
            payload = { 'focus_area': focus_area, 'site_document_content': site_document_content }
            response = chain.invoke(payload)
            status.append( f'{focus_area}:{response.get("status")}' )
            if response.get('status') == 'Partially':
                comments.append(f'{focus_area}:{response.get("comments")}')

    delta_table_as_df.iloc[idx, 3] = "||".join(status)
    delta_table_as_df.iloc[idx, 4] = "||".join(comments)

    print('Step 7 Completed: Delta Table Filled with Required Data')

    return { 'delta_table_as_df': delta_table_as_df }
