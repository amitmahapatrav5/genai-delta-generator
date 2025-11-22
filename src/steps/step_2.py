from typing import Dict, TypedDict, Annotated

from langchain_core.prompts import PromptTemplate

from state import State
from components.chat_model import chat_model


class RelevantRow(TypedDict):
    relevance: Annotated[bool, "Whether the row is relevant to the title or not"]

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

def step_2(state: State) -> Dict:
    '''
    This node filters the rows in global sop list dataframe based on the site document title.
    '''
    global_sop_list_table_as_df = state.get('global_sop_list_table_as_df')
    site_document_title_table_as_df = state.get('site_document_title_table_as_df')

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

    print("Step 2: Completed: Irrelevant rows are filtered from Global SOP List Dataframe")

    return { 
        'filtered_global_sop_list_table_as_df': filtered_global_sop_list_table_as_df,
        'irrelevant_row_indices_in_global_sop_list_table_as_df': irrelevant_row_indices_in_global_sop_list_table_as_df
    }