# def keyword_filter(job, excluded_keywords, mode="both"):
#     """
#     Returns True if job contains any excluded keywords (should be filtered out)
#     Returns False if job is clean (should be included)
#     """
#     if not excluded_keywords:
#         return False  # No exclusions, keep the job
    
#     title = job.get("job_title", "").lower()
#     description = job.get("job_description", "").lower()
    
#     if mode == "title":
#         search_text = title
#     elif mode == "description":
#         search_text = description
#     else:  # both
#         search_text = f"{title} {description}"
    
#     # Check if any exclude keyword is present
#     for keyword in excluded_keywords:
#         if keyword.lower() in search_text:
#             return True  # Found excluded keyword, filter out this job
    
#     return False  # No excluded keywords found, keep this job
def keyword_filter(job, excluded_keywords, mode="both"):
    """
    Returns True if job contains any excluded keywords (should be filtered out)
    Returns False if job is clean (should be included)
    
    Note: Excluded keywords ALWAYS check both title and description,
    regardless of mode. The mode only affects the search query matching.
    """
    if not excluded_keywords:
        return False  # No exclusions, keep the job
    
    title = job.get("job_title", "").lower()
    description = job.get("job_description", "").lower()
    
    # Always check both title and description for excluded keywords
    search_text = f"{title} {description}"
    
    # Check if any exclude keyword is present
    for keyword in excluded_keywords:
        if keyword.lower() in search_text:
            return True  # Found excluded keyword, filter out this job
    
    return False  # No excluded keywords found, keep this job