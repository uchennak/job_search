# # jobs/views.py
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator
# from .services.jsearch import fetch_jobs
# from .utils.filtering import keyword_filter
# from .utils.source_filter import is_blocked_source  # NEW IMPORT
# from .services.experience_parser import extract_experience

# def home_redirect(request):
#     return redirect('search')

# def search_form(request):
#     return render(request, 'jobs/search.html')

# def search_jobs(request):
#     q = request.GET.get("q", "")
#     location = request.GET.get("location", "").strip()
#     radius = request.GET.get("radius", "").strip()
    
#     # Validate required fields
#     if not q or not location:
#         error_message = "Both job keywords and location are required."
#         return render(request, 'jobs/results.html', {
#             "jobs": [],
#             "error": error_message
#         })
    
#     exclude_raw = request.GET.get("exclude", "")
#     exclude = [k.strip() for k in exclude_raw.split(",") if k.strip()]
    
#     limit = int(request.GET.get("limit", 25))
#     title_only = request.GET.get("title_only") == "on"
#     description_only = request.GET.get("description_only") == "on"
#     page_number = request.GET.get("page", 1)
#     results_per_page = int(request.GET.get("per_page", 10))
    
#     # Determine mode based on checkboxes
#     mode = "both"
#     if title_only:
#         mode = "title"
#     elif description_only:
#         mode = "description"
    
#     # Calculate pages needed
#     pages_needed = max(1, (limit // 10) + 1)
    
#     # Fetch jobs from API with location and radius
#     raw_jobs = fetch_jobs(q, location=location, radius=radius, num_pages=pages_needed)
    
#     if not raw_jobs:
#         return render(request, 'jobs/results.html', {
#             "jobs": [],
#             "query": q,
#             "location": location,
#             "radius": radius,
#             "message": "No jobs found matching your criteria."
#         })
    
#     # Filter and process jobs
#     filtered_jobs = []
#     blocked_count = 0  # Track how many jobs were blocked
    
#     for job in raw_jobs:
#         # NEW: Check if job is from a blocked source
#         if is_blocked_source(job):
#             blocked_count += 1
#             continue
        
#         # Check for excluded keywords
#         if not keyword_filter(job, exclude, mode):
#             job["experience_required"] = extract_experience(job.get("job_description", ""))
#             filtered_jobs.append(job)
            
#             if len(filtered_jobs) >= limit:
#                 break
    
#     # Log how many were blocked
#     print(f"DEBUG - Blocked {blocked_count} jobs from weak sources")
    
#     # Paginate the filtered results
#     paginator = Paginator(filtered_jobs, results_per_page)
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         "jobs": page_obj,
#         "query": q,
#         "location": location,
#         "radius": radius,
#         "exclude": exclude_raw,
#         "title_only": "on" if title_only else "",
#         "description_only": "on" if description_only else "",
#         "limit": limit,
#         "per_page": results_per_page,
#         "blocked_count": blocked_count  # Pass to template if you want to display it
#     }
    
#     return render(request, 'jobs/results.html', context)
# jobs/views.py
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .services.jsearch import fetch_jobs
from .utils.filtering import keyword_filter
from .utils.source_filter import is_blocked_source
from .services.experience_parser import extract_experience

def home_redirect(request):
    return redirect('search')

def search_form(request):
    return render(request, 'jobs/search.html')

def search_jobs(request):
    q = request.GET.get("q", "")
    location = request.GET.get("location", "").strip()
    radius = request.GET.get("radius", "").strip()
    
    # Validate required fields
    if not q or not location:
        error_message = "Both job keywords and location are required."
        return render(request, 'jobs/results.html', {
            "jobs": [],
            "error": error_message
        })
    
    exclude_raw = request.GET.get("exclude", "")
    exclude = [k.strip() for k in exclude_raw.split(",") if k.strip()]
    
    limit = int(request.GET.get("limit", 25))
    page_number = request.GET.get("page", 1)
    results_per_page = int(request.GET.get("per_page", 10))

    # Get search scope from radio button (both, title_only, or description_only)
    search_scope = request.GET.get("search_scope", "both")

    # Map search_scope to mode
    if search_scope == "title_only":
        mode = "title"
    elif search_scope == "description_only":
        mode = "description"
    else:
        mode = "both"
    
    # Calculate pages needed (fetch more since we'll filter)
    pages_needed = max(1, (limit // 10) + 3)  # Fetch extra pages for filtering
    
    # Fetch jobs from API with location and radius
    raw_jobs = fetch_jobs(q, location=location, radius=radius, num_pages=pages_needed)
    
    if not raw_jobs:
        return render(request, 'jobs/results.html', {
            "jobs": [],
            "query": q,
            "location": location,
            "radius": radius,
            "message": "No jobs found matching your criteria."
        })
    
    # Filter and process jobs
    filtered_jobs = []
    blocked_count = 0
    mode_filtered_count = 0  # Track how many filtered by title/description mode
    
    # Split search query into keywords
    search_keywords = [kw.strip().lower() for kw in q.split() if kw.strip()]
    
    for job in raw_jobs:
        # Filter 1: Check if job is from a blocked source
        if is_blocked_source(job):
            blocked_count += 1
            continue
        
        # Filter 2: Check if search keywords appear in the right place (title/description/both)
        title = job.get("job_title", "").lower()
        description = job.get("job_description", "").lower()
        
        # Check if ALL search keywords appear in the appropriate field(s)
        if mode == "title":
            # ALL keywords must be in title
            if not all(keyword in title for keyword in search_keywords):
                mode_filtered_count += 1
                continue
        elif mode == "description":
            # ALL keywords must be in description
            if not all(keyword in description for keyword in search_keywords):
                mode_filtered_count += 1
                continue
        # If mode == "both", keep all jobs (API already filtered)
        
        # Filter 3: Check for excluded keywords (always checks both title and description)
        if keyword_filter(job, exclude, mode):
            continue
        
        # Job passed all filters
        job["experience_required"] = extract_experience(job.get("job_description", ""))
        filtered_jobs.append(job)
        
        if len(filtered_jobs) >= limit:
            break
    
    # Debug logging
    print(f"DEBUG - Total jobs from API: {len(raw_jobs)}")
    print(f"DEBUG - Blocked from weak sources: {blocked_count}")
    print(f"DEBUG - Filtered by {mode} mode: {mode_filtered_count}")
    print(f"DEBUG - After all filters: {len(filtered_jobs)}")
    
    # Paginate the filtered results
    paginator = Paginator(filtered_jobs, results_per_page)
    page_obj = paginator.get_page(page_number)
    
    context = {
        "jobs": page_obj,
        "query": q,
        "location": location,
        "radius": radius,
        "exclude": exclude_raw,
        "search_scope": search_scope,
        "limit": limit,
        "per_page": results_per_page,
        "blocked_count": blocked_count,
        "mode_filtered_count": mode_filtered_count
    }
    
    return render(request, 'jobs/results.html', context)