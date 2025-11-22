from typing import Dict

from state import State


def step_5(state: State) -> Dict:
    '''
    '''
    filtered_global_sop_list_table_as_df = state.get('filtered_global_sop_list_table_as_df')
    delta_table_as_df = filtered_global_sop_list_table_as_df.copy()
    delta_table_as_df["Status"] = ""
    delta_table_as_df["Comments"] = ""

    print('Step 5 Completed: Delta Table Initialized')

    return { 'delta_table_as_df': delta_table_as_df }