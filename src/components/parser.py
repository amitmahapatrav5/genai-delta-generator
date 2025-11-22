import nltk
from unstructured.partition.pdf import partition_pdf

for pkg in ["punkt", "punkt_tab", "averaged_perceptron_tagger_eng"]:
    try:
        nltk.data.find(f"tokenizers/{pkg}")
    except LookupError:
        nltk.download(pkg, quiet=True)

def extract_pdf_elements(filepath: str):
    elements = partition_pdf(
        filename=filepath,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True,
        languages=['English']
    )
    return elements