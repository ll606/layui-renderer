from dominate.tags import *
from dominate.util import raw
from typing import List

def navbar_child(
    title : str,
    title_link : str = "#",
    content : List[dom_tag] = [], 
    *args, **kwargs
):
    '''
        返回 nav item
    '''
    nav_item:li = li(cls="layui-nav-item", *args, **kwargs)
    nav_item += a(title, href=title_link)
    
    nav_child = dl(cls="layui-nav-child")
    for each in content:
        tmp:dd = dd()
        tmp += each
        nav_child += tmp
    
    nav_item += nav_child
    return nav_item
    