# Scrapy_FindJob
使用Scrapy 爬取智联招聘  与 51job网站

# 本项目 添加了  代理ip功能  和  随机使用 user-agent

# 其中如果需要使用 代理ip需要修改一些代码
1. 在settings.py 文件中 填写该值 ORDERNO,SECRET(在讯代理网站购买动态转发20元100000条) 
2. [scrapy框架添加不了讯代理的代理ip问题](https://www.jianshu.com/p/b8e2e9bed7c5)
3. 在settings.py 中 取消注解 'findjob.middlewares.MyProxy' : 542,

# 虽然 本程序不需要 代理ip 但是以后万一需要的话 就可以复制粘贴代码了

# 环境
1. scrapy
2. mongodb
3. pymongo
