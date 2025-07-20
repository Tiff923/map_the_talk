THEME_EXTRACTION_PROMPT = """
Analyze the following video transcript and extract the main themes discussed. 
A theme is a broad topic or concept that the video explores.

Transcript:
{transcript}

Please identify 3-5 main themes and provide:
1. Theme name (short, descriptive)
2. Brief description of what the theme covers
3. Confidence level (0-1) based on how prominently this theme appears

Format your response as a JSON array of objects with keys: "name", "description", "confidence".
"""

SUBTOPIC_EXTRACTION_PROMPT = """
Given the theme "{theme_name}" and the following transcript context, identify specific subtopics that fall under this theme.

Theme Description: {theme_description}
Transcript Context: {context}

Please identify 2-4 subtopics and provide:
1. Subtopic name (specific, actionable)
2. Brief explanation of what this subtopic covers
3. How it relates to the parent theme

Format your response as a JSON array of objects with keys: "name", "explanation", "relation_to_theme".
"""

INSIGHT_EXTRACTION_PROMPT = """
Analyze the following video transcript and the list of subtopics. For each insight you extract, specify which subtopic (by name) it is most closely related to.

Subtopics:
{subtopic_list}

Transcript:
{transcript}

Please identify 3-5 key insights and provide:
1. The insight content (what the creator is saying)
2. Why this insight is valuable or unique
3. The type of insight (methodological, philosophical, practical, etc.)
4. The related subtopic name (must match one of the subtopic names above)

Format your response as a JSON array of objects with keys: "content", "value", "type", "related_subtopic_name".
""" 