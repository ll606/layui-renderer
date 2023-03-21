from components.basic import *
from functools import lru_cache

def goto_page():
    goto_form = form(method='post', style='padding:20px')
    goto_form += add_input(
        name = 'page-url',
        label_= '跳转至网页:', 
        type = 'url',
        required = True,
        placeholder = '请在此输入想要跳转的网页',
        label_width = '150px'
    )
    
    goto_form += add_input(
        name = 'page-goto-sleeptime',
        label_= '程序休眠时间(秒)',
        type = 'number',
        required = True, 
        value = '0',
        label_width = '150px'
    )
    submit_area = add_form_submit(style='text-align:center')
    submit_area['style'] = 'text-align:center;'
    
    goto_form += submit_area
    return goto_form

def panel():
    panel_area = div(style='display:inline-block;')

    return panel_area

def load_process():
    load_form = form(
        method='post', 
        id = "load-process-form", 
        style = "padding:20px",
    )
    upload = add_input(
        name = 'upload-process', 
        type = 'file',
        style = 'display:none'
    )
    
    load_form += add_button(
        label = '上传文件',
        color = 'normal',
        border = True,
        style = 'margin-bottom:20px',
        mount_js = '''
document.querySelector("[name='upload-process']").click()
'''
    )
    
    load_form += upload
    
    load_form += add_input(
        name = 'process-looptimes',
        type = 'number', 
        label_ = '循环次数',
        required = True, 
        value = '1'
    )
    
    load_form += add_form_submit(style='text-align:center')
    
    return load_form


def op_element():
    op_form = form(method='post', style="padding:20px")
    
    op_form += add_select(
        name = 'locate-element-by', 
        label_ = '请选择定位元素的方式:',
        options = [
            {'label':'ID', 'value':'id'},
            {'label':'CSS 选择器', 'value':'css selector'}, 
            {'label':'xpath', 'value':'xpath'},
        ], 
        label_width = '200px'
    )
    
    op_form += add_input(
        name = 'locate-element-value', 
        label_ = '请输入定位元素的值:',
        type = 'text',
        required = True,
        label_width = '200px'
    )
    
    op_form += add_select(
        name = 'operations-to-element', 
        label_= '请选择对元素的操作:',
        options = [
            {'label':'点击元素', 'value':'click'},
            {'label':'向元素输入值', 'value':'type'},
            {'label':'清空元素', 'value':'clear'}
        ],
        label_width = '200px'
    )
    
    op_form += add_input(
        name = 'text-sent-to-element', 
        label_ = '对元素输入的值',
        type = 'text', 
        label_width = '200px',
        disabled = True
    )
    
    op_form += add_form_submit(style='text-align:center')
    return op_form

@lru_cache
def index():
    doc: dom_tag = new_doc('自动化UI界面')
    root: dom_tag = doc.get_scope('root')
    foot: dom_tag = doc.get_scope('foot')
    root['style'] = (
        'width:50%; margin-left:25%; margin-right:25%;'
        'margin-top: 200px'
    )
    
    root += panel()
    
    tabs = add_tabs(
        content = [
            {'title':'加载流程', 'content': load_process()},
            {'title':'跳转页面', 'content': goto_page()},
            {'title':'操作元素', 'content': op_element()}
            
        ], skin='card'
    )
    
    root += tabs
    
    foot += script(raw('''
let text_sent_to_element = document.querySelector("input[name='text-sent-to-element']");
ele = document.querySelector("[name='operations-to-element']").parentNode.querySelector("input");
setInterval(()=>{
    if(ele === null){
        ele = document.querySelector("[name='operations-to-element']").parentNode.querySelector("input");
    }
    if(ele.value === "向元素输入值"){
            text_sent_to_element.removeAttribute("disabled");
        }else{
            text_sent_to_element.value = "";
            text_sent_to_element.setAttribute("disabled", "");
        }
}, 500)
'''))
    
    return doc.render()
