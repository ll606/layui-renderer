from setuptools import setup

setup(
    name = 'layui-renderer',
    version = '0.1.0', 
    author = 'Lingyun Liu',
    author_email = '17610893086@163.com', 
    description = 'This is a package for using python to render the front end framework of layui.', 
    license = "MIT",
    keywords = ['layui', 'front end', 'html'],
    url = '',
    packages = ['components'], 
    install_requires = ['dominate>=2.7.0'], 
)