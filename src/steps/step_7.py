from typing import Dict

from state import State


def step_7(state: State) -> Dict:
    '''
    
    '''

    for idx, row in state.get('delta_table_as_df').iterrows():
        status = "<br>".join(row.iloc[3].split('||'))
        comments = "<br>".join(row.iloc[4].split('||'))
        focus_areas = "<br>".join(row.iloc[1].split(','))
        document_titles = "<br>".join(row.iloc[2].split(','))
        
        state.get('delta_table_as_df').iloc[idx, 1] = focus_areas
        state.get('delta_table_as_df').iloc[idx, 2] = document_titles
        state.get('delta_table_as_df').iloc[idx, 3] = status
        state.get('delta_table_as_df').iloc[idx, 4] = comments

    delta_table_as_df = state.get('delta_table_as_df')
    delta_table_as_html = delta_table_as_df.to_html(index=False)
    
    print('Step 7 Completed: DDelta Table converted into HTML Format for User. This is stored in state')

    return { 'delta_table_as_html': delta_table_as_html }