from yaml import safe_load
from typing import List, TypedDict, Annotated

import pandas as pd
from langchain_core.prompts import PromptTemplate

from components.chat_model import chat_model


def _get_comma_separated_list(content_without_separation: str, prompt_template: PromptTemplate, input_variable_name: str):
    """
    Processes a string of items using a language model to parse them into a structured list,
    then returns them as a comma-separated string.

    Args:
        content_without_separation (str): The input string containing items,
                                          e.g., "Health Insurance Life Insurance Vehicle Insurance".
        prompt_template (PromptTemplate): A LangChain PromptTemplate that guides the LLM
                                          to parse the input into a list of items, including a one-shot example.
                                          e.g., PromptTemplate(
                                              template = '''
                                              You will be given a string of items separated by spaces: {items_to_parse}.
                                              Your task is to return these items as a comma-separated string.
                                              
                                              Example:
                                              Input: "Health Insurance Life Insurance Vehicle Insurance"
                                              Output: ["Health Insurance", "Life Insurance", "Vehicle Insurance"]
                                              
                                              Now, process the following:
                                              ''',
                                              input_variables=["items_to_parse"]
                                          )
        input_variable_name (str): The name of the input variable in the prompt_template
                                   that will receive `content_without_separation`.

    Returns:
        str: A comma-separated string of the parsed items,
             e.g., "Health Insurance,Life Insurance,Vehicle Insurance".
    """
    class CommaSeparatedItems(TypedDict):
        items: Annotated[List[str], "Comma separated list of items"]

    structured_model = chat_model.with_structured_output(CommaSeparatedItems)
    chain = prompt_template | structured_model
    response = chain.invoke({ input_variable_name: content_without_separation })
    return ",".join(response.get('items'))


def clean_df(filtered_global_sop_list_table_as_df: pd.DataFrame) -> pd.DataFrame:
    title_identification_prompt_template = PromptTemplate(
        template='''
        You will be given a string of policy document titles may or may not be separated by any semantic separator.
        If the string is separated by any semantic separator, please follow the separator strictly
        If not, please go through the entire string and semantically identify all the policy document titles.
        Once identified, please create a python list where each element is the policy document title.

        For example, 
        Given: "VI-101: Comprehensive Motor Insurance Policy VI-102: Third-Party Liability Insurance Document VI-201: Zero-Depreciation Add-On Coverage Sheet", 
        Output: ["VI-101: Comprehensive Motor Insurance Policy", "VI-102: Third-Party Liability Insurance Document", "VI-201: Zero-Depreciation Add-On Coverage Sheet"]

        Here is the string of policy document titles
        {policy_document_titles}
        ''',
        input_variables=['policy_document_titles']
    )

    focus_area_identification_prompt_template = PromptTemplate(
        template='''
        You will be given a string of focus areas may or may not be separated by any semantic separator.
        If the string is separated by any semantic separator, please follow the separator strictly
        If not, please go through the entire string and semantically identify all the focus areas.
        Once identified, please create a python list where each element is the focus area.

        For example, 
        Given: "Premium Evaluation Framework Coverage Restrictions Garage Network Accessibility Vehicle Condition & Pre-Inspection Rules Claim Assessment Workflow", 
        Output: ["Premium Evaluation Framework", "Coverage Restrictions", "Garage Network Accessibility", "Vehicle Condition & Pre-Inspection Rules", "Claim Assessment Workflow"]

        Here is the string of focus areas
        {focus_areas}
        ''',
        input_variables=['focus_areas']
    )

    for idx, row in filtered_global_sop_list_table_as_df.iterrows():
        focus_areas, document_titles = row.iloc[1], row.iloc[2]
        
        comma_separated_document_titles = _get_comma_separated_list(
            content_without_separation=document_titles,
            prompt_template=title_identification_prompt_template,
            input_variable_name='policy_document_titles'
        )
        
        comma_separated_focus_areas = _get_comma_separated_list(
            content_without_separation=focus_areas,
            prompt_template=focus_area_identification_prompt_template,
            input_variable_name='focus_areas'
        )
        row.iloc[1], row.iloc[2] = comma_separated_focus_areas, comma_separated_document_titles

    return filtered_global_sop_list_table_as_df