from utils import get_comma_separated_list
from langchain_core.prompts import PromptTemplate

result = get_comma_separated_list(
    content_without_separation="HI-101: Individual Health Insurance Policy HI-102: Family Floater Health Insurance Policy HI-201: Critical Illness Coverage Document",
    prompt_template=PromptTemplate(
        template="""You will be given a string of Insurance Document Titles: {items_to_parse}. 
        Your task is to return these items as a comma-separated string.""",
        input_variables=["items_to_parse"]
    ),
    input_variable_name="items_to_parse"
)

print(result)