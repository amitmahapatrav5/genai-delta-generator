from typing import List, TypedDict, Dict

from langgraph.graph import StateGraph, START, END

from state import State
from utils import config


from steps.step_1 import step_1
from steps.step_2 import step_2
from steps.step_3 import step_3
from steps.step_4 import step_4
from steps.step_5 import step_5
from steps.step_6 import step_6
from steps.step_7 import step_7

graph = StateGraph(State)

graph.add_node('step_1', step_1)
graph.add_node('step_2', step_2)
graph.add_node('step_3', step_3)
graph.add_node('step_4', step_4)
graph.add_node('step_5', step_5)
graph.add_node('step_6', step_6)
graph.add_node('step_7', step_7)

graph.add_edge(START, 'step_1')
graph.add_edge('step_1', 'step_2')
graph.add_edge('step_2', 'step_3')
graph.add_edge('step_3', 'step_4')
graph.add_edge('step_4', 'step_5')
graph.add_edge('step_5', 'step_6')
graph.add_edge('step_6', 'step_7')
graph.add_edge('step_7', END)

workflow = graph.compile()

final_state = workflow.invoke({
    'global_sop_list_file_path': config.get('data').get('global_sop_list_file_path'),
    'site_document_file_path': config.get('data').get('site_document_file_path'),
})

print(final_state)