## 百度贴吧爬虫
#### 工具：python，chromedriver，selenium
#### 环境配置：
>pip install selenium
>chromedriver:https://sites.google.com/a/chromium.org/chromedriver/
#### 代码简介：
***本python文件定义了一个tieba_info类，其中有三个主要函数:***
* init函数:用来初始化tieba_info类，包括阻止图片加载，设置为开发者模式，防止被网站识别。
* search_main函数:用来进行用户登陆，以及主要信息的爬取（帖子的名称和链接）。需要注意的是运行这一步必须加载图片，否则无法点击响应的按钮。
* search_detail函数:用来对每个帖子进行细节信息的爬取（帖子的总页数，用户昵称，用户评论）
#### 运行测试：
![](login.gif)




