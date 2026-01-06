import re

def extract_experience(description):
    """
    Extract years of experience from job description using regex.
    Returns a string like "3-5 years", "2+ years", or "Entry Level"
    """
    if not description:
        return "Not specified"
    
    text = description.lower()
    
    # Pattern 1: "X-Y years" or "X to Y years"
    pattern1 = r'(\d+)\s*[-to]+\s*(\d+)\s*(?:\+)?\s*years?'
    match = re.search(pattern1, text)
    if match:
        min_years = match.group(1)
        max_years = match.group(2)
        return f"{min_years}-{max_years} years"
    
    # Pattern 2: "X+ years" or "X or more years"
    pattern2 = r'(\d+)\s*\+?\s*(?:or more)?\s*years?'
    match = re.search(pattern2, text)
    if match:
        years = match.group(1)
        return f"{years}+ years"
    
    # Pattern 3: Check for entry level keywords
    entry_keywords = [
        'entry level', 'entry-level', 'junior', 'graduate',
        'no experience required', 'no experience necessary',
        '0 years', '0-1 years', '0-2 years'
    ]
    if any(keyword in text for keyword in entry_keywords):
        return "Entry Level"
    
    # Pattern 4: Check for senior keywords
    senior_keywords = ['senior', 'lead', 'principal', 'staff', 'architect']
    if any(keyword in text for keyword in senior_keywords):
        return "Senior (5+ years)"
    
    # Pattern 5: Check for mid-level keywords
    mid_keywords = ['mid-level', 'mid level', 'intermediate']
    if any(keyword in text for keyword in mid_keywords):
        return "Mid-Level (3-5 years)"
    
    return "Not specified"