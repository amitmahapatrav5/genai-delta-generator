from typing import List, TypedDict
import pandas as pd

class State(TypedDict):
    # Initial State
    global_sop_list_file_path: str
    site_document_file_path: str

    # Step 1 State
    global_sop_list_table_as_df: pd.DataFrame
    site_document_title_table_as_df: pd.DataFrame

    # Step 2 State
    filtered_global_sop_list_table_as_df: pd.DataFrame
    irrelevant_row_indices_in_global_sop_list_table_as_df: List[int]

    # Step 3 State

    # Step 4 State
    site_document_content: str

    # Step 5 State
    delta_table_as_df: pd.DataFrame

    # Step 6 State

    # Step 7 State
    delta_table_as_html: str