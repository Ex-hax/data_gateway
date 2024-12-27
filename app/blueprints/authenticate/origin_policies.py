from typing import Dict
'''
Blueprint level use in __init__py
Route level use for each route in routes.py and views.py
'''
class login_logout_level:
    setting: Dict[str,tuple[str]] = {
        'allow_origin': ('http://localhost:5000', 'https://abea-103-178-219-81.ngrok-free.app'),
        'allow_methods': ('POST', 'GET')
    }