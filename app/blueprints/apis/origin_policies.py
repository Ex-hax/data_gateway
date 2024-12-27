from typing import Dict
'''
Blueprint level use in __init__py
Route level use for each route in routes.py and views.py
'''
class test_route_level:
    setting: Dict[str,tuple[str]] = {
        'allow_methods': ('POST'),
        'allow_headers': ('Content-type', 'Authorization')
    }