def feature_flags(request):
    user = request.user
    flags = {
        "is_priority_feature_enabled" : False,
    }
    # Ensure the user is authenticated before cjhecking groups
    if user.is_authenticated:
        flags["is_priorityfeature_enabled"] = user.groups.filter(
            name = "Task prioritization Beta Testers"
        ).exists()
    
    return flags