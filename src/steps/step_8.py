from typing import Dict

from state import State


def step_8(state: State) -> Dict:
    '''
    This node will convert the delta_table_as_df into HTML format for user.
    '''
    delta_table_as_df = state.get('delta_table_as_df')
    delta_table_as_df = delta_table_as_df.replace({r'^"(.*)"$': r'\1'}, regex=True) # remove wrapping double quotes
    delta_table_as_df = delta_table_as_df.replace({r"^'(.*)'$": r'\1'}, regex=True) # remove wrapping single quotes

    for idx, row in delta_table_as_df.iterrows():
        focus_areas = "<br>".join(row.iloc[1].split(','))
        document_titles = "<br>".join(row.iloc[2].split(','))
        
        focus_area_status_pairs = row.iloc[3].split('||')
        statuses = ['<ul>']
        for pair in focus_area_status_pairs:
            focus_area, status = pair.split(":")
            statuses.append(f'<li><b>{focus_area}</b>: {status}</li>')
        statuses.append('</ul>')

        focus_area_comment_pairs = row.iloc[4].split('||')
        comments = ['<ul>']
        for pair in focus_area_comment_pairs:
            focus_area, comment = pair.split(":")
            comments.append(f'<li><b>{focus_area}</b>: {comment}</li>')
        comments.append('</ul>')

        delta_table_as_df.iloc[idx, 1] = focus_areas
        delta_table_as_df.iloc[idx, 2] = document_titles
        delta_table_as_df.iloc[idx, 3] = "".join(statuses)
        delta_table_as_df.iloc[idx, 4] = "".join(comments)

    delta_table_as_html = delta_table_as_df.to_html(index=False, escape=False)
    print('Step 8 Completed: Delta Table converted into HTML Format for User. This is stored in state')

    return { 'delta_table_as_html': delta_table_as_html }