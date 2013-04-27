"""
    Common functions
"""

def parse_post(data):
    ret = {}
    fields = data.split('&')
    for item in fields:
        key, value = item.split('=')
        ret[key] = value
