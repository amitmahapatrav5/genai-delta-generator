# README

**Step 1:** Get *Global SOP Context Table* and *Site Document Title Table*
- Extract html table tags of *Global SOP Context Table* from Global SOP using `Unstructured`
- Extract html table tags of *Site Document Title Table* from Site Document using `Unstructured` 
- Convert the extracted html table into a pandas DataFrame as this dataframe will be required to be manipulated in the next steps.

**Step 2 - Filter Rows:** Filter the rows in *Global SOP Context Dataframe* based on *Site Document Title Dataframe* - Title
- Get *Title* from *Site Document Title Dataframe*.
- Iterate over each row in *Global SOP Context Dataframe* and feed *Title* along with *Global SOP Context Dataframe* row to LLM to filter out the irrelevant rows.
- Update the *Global SOP Context Dataframe* with the filtered rows.


**Step 3 - Filter Column 3:** Update "Global SOP Context Dataframe" - Policy Document Column
```
for row in rows:
	policy_document_names = table[row][col-3]
	**PROMPT**
	relevant_policy_docs: List = LLM_CALL(
					'Site Document Title',
					policy_document_names)
	update "Global SOP Context Dataframe" - Column 3
```

**Step 4 - Filter Column 2:** Update "Global SOP Context Dataframe" - Focus Area Column
```
for row in rows:
	focus_areas, relevant_policy_docs = table[row][col-2], table[row][col-3]
	# PROMPT - 3
	relevant_focus_areas: List = LLM_CALL(relevant_policy_docs, focus_areas)
	update "Global SOP Context Table" - Column 2	 
```

**Step 5 - Get Site Document Context:** Get "Site Document Context"
```
site_document_context = []
for element in elements_of_site_doc:
	ignore Title, TOC, PageNumber etc
	Consider Relevant elements (Title, ListItem, Image, Table etc)
	site_document_context.append(element)
```

**Step 6 - Prepare Delta Table:** Prepare Delta Table
- delta_table = global_sop_context_table + 'Status Column' + 'Citation Column'

**Step 7:**
```
for row in rows:
	focus_areas = table[row][col-2].split(',')
	for focus_area in focus_areas:
		# result: {included: Yes | No | Partial, citation: str }
		result = LLM_CALL(focus_area, site_document_context)
		update delta_table
return delta_table
```

**Step 8 - Convert Delta Table into HTML:** Convert Delta Table into HTML
- delta_table_as_html = delta_table.to_html(index=False, escape=False)
