# jobs/utils/source_filter.py

# List of blocked job sources/boards
BLOCKED_SOURCES = [
    "bebee",
    "talentify",
    "jobcase",
    "whatjobs",
    "talent.com",
    "jobilize",
    "jooble",
    "adzuna",
    "neuvoo",
    "jobrapido",
    "mitula",
    "trovit",
    "locanto",
    "geebo",
    # Add more as you discover them
]

def is_blocked_source(job):
    """
    Check if a job is from a blocked/weak source
    
    Args:
        job: Job dictionary from API
    
    Returns:
        True if job should be blocked, False if it should be kept
    """
    # Check employer/company name
    employer = job.get("employer_name", "").lower()
    
    # Check job board name if available
    job_board = job.get("job_publisher", "").lower()
    
    # Check apply link domain
    apply_link = job.get("job_apply_link", "").lower()
    
    # Check against blocked sources
    for blocked in BLOCKED_SOURCES:
        blocked_lower = blocked.lower()
        
        # Check if blocked source appears in any field
        if (blocked_lower in employer or 
            blocked_lower in job_board or 
            blocked_lower in apply_link):
            return True
    
    return False


def get_blocked_sources():
    """Return the list of blocked sources"""
    return BLOCKED_SOURCES.copy()