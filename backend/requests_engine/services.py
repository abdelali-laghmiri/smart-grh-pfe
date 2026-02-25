from users.models import UserProfile

def find_hierarchical_approver(employee_profile, required_positions):
    """"
        climb the managerial chin until we find a user with one of the required positions

    """
    
    current = employee_profile.manager

    while current is not None:
        if current.job_position == required_positions:
            return current   

        current = current.manager

    return None