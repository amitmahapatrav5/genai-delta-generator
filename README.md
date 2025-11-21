# README

STEP 1: Get "Global SOP Context Table" and "Site Document Title"
- Extract "Title" from Site Document using Unstructured
- Extract "Table" from Global SOP using Unstructured
**PROMPT - 1**
- Feed the "Title" and "Table" to LLM and get a "Structured Output" of which row(s) are relevant for processing
- Extract the rows from HTML table and create a table object which is only relevant for our further process. This is the "Global SOP Context Table"


STEP 2: Update "Global SOP Context Table" - Policy Document Column
```
for row in rows:
	policy_document_names = table[row][col-3]
	**PROMPT - 2**
	relevant_policy_docs: List = LLM_CALL(
					'Site Document Title',
					policy_document_names)
	update "Global SOP Context Table" - Column 3
```

STEP 3: Update "Global SOP Context Table" - Focus Area Column
```
for row in rows:
	focus_areas, relevant_policy_docs = table[row][col-2], table[row][col-3]
	# PROMPT - 3
	relevant_focus_areas: List = LLM_CALL(relevant_policy_docs, focus_areas)
	update "Global SOP Context Table" - Column 2	 
```

STEP 4: Get "Site Document Context"
```
site_document_context = []
for element in elements_of_site_doc:
	ignore Title, TOC, PageNumber etc
	Consider Relevant elements (Title, ListItem, Image, Table etc)
	site_document_context.append(element)
```

Step 5: Prepare Delta Table
- delta_table = global_sop_context_table + 'Status Column' + 'Citation Column'

STEP 6:
```
for row in rows:
	focus_areas = table[row][col-2].split(',')
	for focus_area in focus_areas:
		# result: {included: Yes | No | Partial, citation: str }
		result = LLM_CALL(focus_area, site_document_context)
		update delta_table
return delta_table
```