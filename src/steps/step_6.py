from typing import Dict

from state import State


def step_6(state: State) -> Dict:
    '''
    This node initializes the delta dataframe by copying the filtered global sop list dataframe and adding 2 new columns.
    '''
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    delta_table_as_df = filtered_global_sop_list_table_as_df.copy()
    delta_table_as_df["Status"] = ""
    delta_table_as_df["Comments"] = ""

    print('Step 6 Completed: Delta Table Initialized')

    return { 'delta_table_as_df': delta_table_as_df }