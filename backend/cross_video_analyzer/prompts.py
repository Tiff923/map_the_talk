CONTRAST_IDENTIFICATION_PROMPT = """
Given the following list of insights about the subtopic "{subtopic_name}" from different videos, identify any points of contrast, disagreement, or opposing perspectives.

For each contrast you find, provide:
1. A summary of the contrast (what is the disagreement or difference?)
2. The list of insight IDs that represent the opposing viewpoints
3. The list of video IDs these insights come from
4. The type of contrast (methodological, philosophical, practical, etc.)

Insights:
{insights_json}

Format your response as a JSON object with a key "contrasts" whose value is an array of objects with keys: "summary", "insight_ids", "video_ids", "contrast_type".
""" 

CONCEPTUAL_OVERLAP_PROMPT = """
Given the following list of themes and subtopics from multiple videos, identify any concepts (themes or subtopics) that are semantically similar, related, or overlapping, even if they are described differently.

For each overlap you find, provide:
1. The primary concept (name and type: 'theme' or 'subtopic')
2. The list of overlapping concepts (names and types)
3. The list of video IDs these concepts appear in
4. Whether these concepts should be merged in a visualization (true/false)
5. A semantic similarity score (0-1)

Concepts:
{concepts_json}

Format your response as a JSON object with a key "overlaps" whose value is an array of objects with keys: "primary_concept", "primary_type", "overlapping_concepts", "overlapping_types", "video_ids", "should_merge", "semantic_similarity".
""" 