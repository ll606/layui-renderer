from dominate.tags import *
from dominate.util import raw
from typing import Literal, Callable, Optional, List, Iterable, Union
from markdown import markdown
from functools import partial
from random import randint

form = partial(form, cls = 'layui-form')

def new_doc(title:str) -> dom_tag:
    '''
        新建一个网页文档，默认使用layui框架
        并且新建 root 和 foot 标签
        
        如果在文档顶端输出内容则在root标签中输出
        如果在文档底部输出内容则在foot标签中输出
        
        输入：
            title: 网页标题
            
        返回值：
            返回 html : dom_tag
        
        使用例子：
            doc : dom_tag = new_doc("新建html")
    '''
    doc:dom_tag = html()
    head_tag:dom_tag = head()
    head_tag += meta(charset="UTF-8")
    head_tag += meta(
        http_equiv="X-UA-Compatible",
        content = "IE=edge"
    )
    
    head_tag += meta(
        name='viewport',
        content="width=device-width, initial-scale=1.0"
    )
    
    head_tag += raw('<title>%s</title>'%title)
    head_tag += link(
        rel="stylesheet",
        href = "https://www.layuicdn.com/layui-v2.6.10/css/layui.css",
        defer = ''
    )
    
    head_tag += script(
        src = "https://www.layuicdn.com/layui-v2.6.10/layui.js",
        defer = ''
    )
    
    doc += head_tag
    
    body_tag = body()
    
    body_tag += div(id="scope-root")
    foot = div(id="scope-foot")
    body_tag += foot
    
    doc += body_tag
    
    def get_scope(doc: dom_tag, scope: str) -> dom_tag:
        return doc.getElementById('scope-%s' % scope)
    
    doc.get_scope = partial(get_scope, doc)
    
    foot += script(raw('''
layui.use('form',function(){
     var form = layui.form
    form.render('select')
})
'''))
    
    return doc

def add_button(
    label : str = '',
    color : Literal[
        'default', 'primary', 'normal', 
        'warm', 'danger', 'disabled'
    ] = 'default',
    size : Literal[
        'default', 'large', 'small', 
        'mini', 'fluid'
    ] = 'default',
    radius : bool = True,
    border : bool = False,
    disabled : bool = False,
    mount_js: Optional[str] = None,
    *args, **kwargs
) -> button:
    '''
        输入：
            label: 
                按钮中的文本内容
                
            color: 
                按钮颜色，具体颜色详见 layui 文档
                可选值有 
                default, primary, normal, warm
                danger, disabled
                
                默认： default
            
            size:
                按钮大小， 可选值有：
                default, large, small, mini, fluid
                
                如果选择 fluid， 按钮将会尽可能的占满
                横向空间
            
            radius:
                bool 类型
                True: 圆角按钮, False: 方角按钮
            
            border:
                如果 border 为True, 则
                按钮内部为白色，color值为边框颜色
            
            disabled: 
                是否禁用按钮
        
        输出：
            返回 button : dom_tag 标签
    '''
    btn = button(label, cls="layui-btn", *args, **kwargs)
    if border:
        btn['class'] += ' layui-btn-primary layui-border-%s' % (
            {
                'default':'green','normal':'blue','warm':'orange',
                'danger':'red', 'primary':'black'
            }.get(color, 'green')
        )

    else:
        if color.lower().strip() != 'default':
            btn['class'] += ' layui-btn-%s'%color
        else:
            btn['class'] += ' layui-btn'
    
    if size.lower().strip() != 'default':
        sizemap:dict = {
            'large':'lg',
            'small':'sm',
            'mini':'xs',
            'fluid':'fluid'
        }
        btn['class'] += ' layui-btn-%s'%sizemap.get(size)
    
    if disabled:
        btn['class'] += ' layui-btn-disabled'
    
    if radius:
        btn['class'] += ' layui-btn-radius'
    
    if mount_js is not None:
        but_id = hash(str(randint(0,100))+mount_js)
        button_area:div = div(id='button-area-%s'%but_id)
        button_area += btn
        js:script = script(raw(
'''
    document.querySelector("#button-area-%s").addEventListener("click",()=>{
        %s
    })
'''%(but_id, mount_js)
        ))
        button_area += js
        return button_area

    return btn

def add_input(
    name : str,
    label_ : str = '',
    type : Literal[
        'text','password','date','datetime','datetime-local',
        'email', 'file', 'image', 'month', 'number', 'radio',
        'range', 'tel', 'time', 'url', 'week', 'switch'
    ] = 'text',
    required : bool = False, 
    placeholder : str = '',
    skin : Optional[Literal['primary','switch']] = None,
    lay_text: Optional[str] = None,
    style : str = 'margin-bottom:20px',
    datalist_ : List[Union[int,str,float]] = [],
    label_width : Optional[str] = '150px',
    *args, **kwargs
) -> input_:
    '''
        这个函数，将会根据参数变为不同的 input 类型，
        如，如果 type 参数的值为 switch， 渲染到网
        页上就会是一个switch 按钮, 会考虑对这个函数
        进行二次封装
        
        输入:
            name <str> : 
                输出input标签的name属性
            
            label_ <str> :
                输出input的提示标签，注意当渲染到网页
                上时，这个label_标签将会与input组件
                横向排布
            
            skin <Literal["primary", "switch"]>
                当 type 为checkbox时生效
                primary 则 checkbox 是最原始的html5样式
                switch 则 checkbox 是 switch 样式
            
            lay_text <str> :
                当输出一个 switch 按钮时，switch 按钮中
                开，关状态下不同的文本，用 "|" 分开
                
                如: on|off
            
            style: 
                input组件的默认css行内样式
    '''
    div_area = div(cls="layui-form-item", style = style)
    input_block = div(cls='layui-input-block')
    
    if label_.strip() != '':
        div_area += label(label_, cls="layui-form-label", style="width:auto")
       
        input_block['style'] = 'margin-left: %s;' % label_width
    else:
        input_block['style'] = 'margin-left: 20px;'    
    
    
    div_area += input_block
    
    inpt = input_(
        type="%s"%(type if type.lower().strip() != 'switch' else 'checkbox'),
        placeholder = placeholder,
        cls = 'layui-input',
        name = name,
        list = '%s-list'%name,
        *args, **kwargs
    )
    if required:
        inpt['required'] = ''
        inpt['lay-verify'] = 'required'
    
    if skin is not None:
        inpt['lay-skin'] = skin
        
    if lay_text is not None:
        inpt['lay-text'] = lay_text
    
    input_block += inpt
    
    data = datalist(id='%s-list'%name)
    for each in datalist_:
        data += option(str(each))
    input_block += data
    
    return div_area

def add_markdown(md_text:str):
    return raw(markdown(md_text))

def add_form_submit(*args, **kwargs):
    submit_area = div(cls='ws-form-submit-btns', *args, **kwargs)
    submit_area += add_button(
        label = '提交', color = 'default', type = 'submit',
        radius = False
    )
    submit_area += add_button(
        label = '重置', color = 'warm', type = 'cancel',
        radius = False
    )

    return submit_area

class add_form:
    '''
        渲染html中的表单，自带提交和重置按钮
        输入:
            action : 对应form中的action属性
        例子:
            >>> with add_form():
            ...     do_something()
            
        或者将add_form作为装饰器使用。
        
        例子:
            @add_form()
            def do_something():
                ...
    '''
    def __init__(self, action : Optional[str] = None, method:Optional[str] = None) -> None:
        self.form_ = form(cls='layui-form', action = action, method = method)
    
    def __enter__(self):
        return self.form_.__enter__()
    
    def __exit__(self, *args, **kwargs):
        self.form_.__exit__(*args, **kwargs)
        submit_area = div(cls='ws-form-submit-btns')
        submit_area += add_button(
            label = '提交', color = 'default', type = 'submit',
            radius = False
        )
        submit_area += add_button(
            label = '重置', color = 'warm', type = 'cancel',
            radius = False
        )
        self.form_ += submit_area
    
    def __call__(self, func:Callable) -> Callable:
        
        def wrapper(*args, **kwargs):
            with self.form_:
                res = func(*args, **kwargs)
                
            submit_area = div(cls='ws-form-submit-btns')
            submit_area += add_button(
                label = '提交', color = 'default', type = 'submit',
                radius = False
            )
            submit_area += add_button(
                label = '重置', color = 'warm', type = 'cancel',
                radius = False
            )
            self.form_ += submit_area
            
            return res
        
        return wrapper   
    
def add_tabs(
    content : List[dict[str:str]],
    skin : Literal['brief','card','default'] = 'default',
    *args, **kwargs
) -> div:
    '''
    输入:
        content:
            [
                {'title':'早饭','content':h1('包子 豆浆')},
                {'title':'午饭','content':h1('火锅')},
                {'title':'晚饭','content':h1('面条')},
            ]
        
        skin <Literal['brief','card','default']>:
            layui 的样式选择，详见layui文档
    '''
    
    tab:div = div(cls='layui-tab', *args, **kwargs)
    if skin.lower().strip() == 'brief':
        tab['class'] += ' layui-tab-brief'
        tab['lay-filter'] = 'docDemoTabBrief'
    
    elif skin.lower().strip() == 'card':
        tab['class'] += ' layui-tab-card'
    
    tab_content:div = div(cls='layui-tab-content')
    titles:ul = ul(cls='layui-tab-title')
    for i,each in enumerate(content):
        new_div = div()
        if i == 0:
            titles += li(each['title'], cls="layui-this")
            new_div['class'] = 'layui-tab-item layui-show'
            
        else:
            titles += li(each['title'])
            new_div['class'] = 'layui-tab-item'
        new_div += each['content']
        tab_content += new_div
    
    tab += titles
    tab += tab_content
    return tab        

def navbar(
    content: Iterable[dom_tag],
    position:Literal['horizontal','vertical','side'] = 'horizontal',
    *args, **kwargs
):
    '''
        这个函数用于生成网页的导航栏。
        
        输入:
            content:
                可迭代对象，其中应该包含导航栏中的按钮，或者子菜单
            
            position:
                导航栏位置
                horizontal 横向水平放置
                vertical 垂直放置
                side 垂直，占满侧边垂直空间，且会置于其他元素之上
    '''
    
    bar:ul = ul(cls ='layui-nav', *args, **kwargs)
    if position.lower().strip() == 'vertical':
        bar['class'] += ' layui-nav-tree'
    
    if position.lower().strip() == 'side':
        bar['class'] += ' layui-nav-tree layui-nav-side'
    
    bar['lay-filter'] = ""
    for each in content:
        item = li(cls='layui-nav-item')
        item += each
        bar += item
    return bar

        

def add_select(
    name:str,    
    options: dict[str:str], 
    label_:str = '',
    style:str = 'margin-bottom:20px',
    label_width: str = '150px', 
    *args, **kwargs
):
    '''
        options 格式:
        [
            {'label':'上海', 'value':'Shanghai', 'disabled': True, 'selected':False}
        ]
        注:
            也可以不用写 disabled 和 selected
            如果字典中没有disabled, 默认启用选项
            没有selected, 默认不选中
    '''
    
    select_container: div = div(cls="layui-form-item", style=style)
    
    select_label: label = label(label_, cls='layui-form-label')
    
    select_container += select_label
    
    select_block: div = div(cls='layui-input-block')
    
    if label_.strip() == '':
        select_block['style'] = 'margin-left: 20px;'
    else:
        select_block['style'] = 'margin-left: %s;' % label_width
        select_label['style'] = 'width: auto;'
    
    select_area: select = select(name = name, *args, **kwargs)
    select_area['lay-verify'] = ""
    for op in options:
        select_area += option(
            op['label'], value = op['value'], disabled = op.get('disabled'),
            selected = op.get('selected')
        )
    
    select_block += select_area
    select_container += select_block
    return select_container

def main():
    doc = new_doc('test')
    root = doc.getElementById('scope-root')
    
    root += add_button(
        label = 'test', color = 'danger'
    )
    
    with add_form(method='post') as fm:
        h1('这是一个测试表单')
        p('这是一个switch开关')
        add_input(
            name = 'test',
            type = 'checkbox',
            skin = 'switch',
            lay_text='on|off'
        )
        
        add_input(
            name = 'test2',
            label_= '这是一个标签',
            required = True,
            type = 'text',
            datalist_ = ['a','b','c'],
            label_width = '200px'
        )
        root += fm
        
    root += add_tabs(
        [
            {'title':'早饭','content':h1('包子 豆浆')},
            {'title':'午饭','content':h1('火锅')},
            {'title':'晚饭','content':h1('面条')},
        ], skin = 'card'
    )
    
    root += add_markdown('# this is a `markdown test`')
    
    with open('test.html','w',encoding='utf8') as f:
        f.write(doc.render())

if __name__ == '__main__':
    main()