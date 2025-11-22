from typing import Dict

from state import State


def step_7(state: State) -> Dict:
    '''
    
    '''
    
    delta_table_as_df = state.get('delta_table_as_df')
    delta_table_as_html = delta_table_as_df.to_html(index=False)
    

    print('Step 7 Completed: DDelta Table converted into HTML Format for User. This is stored in state')

    return { 'delta_table_as_html': delta_table_as_html }