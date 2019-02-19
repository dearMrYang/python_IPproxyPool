# python_IPproxyPool

##### python+flask+mongo的ip代理池



### 运行
    - python manange.py



#### 步骤
    1. 爬取网站ip
        2. 验证爬取的ip是否可用
        - 可用加入使数据库
        3. 验证数据库ip是否可用
        - 不可用删除
        4. flask获取数据库ip

### 目录
    - core 代码文件
        - db_mongo.py   数据库操作
        - flask_server.py  flask文件
        - settings.py   配置文件，爬取规则
        - spider.py 爬取ip解析ip
        - check.py  验证ip文件
    - manage.py启动文件 