# 医药领域知识图谱实现智能问答与分析服务

## 技术选型
前端开发：vue（element-ui、axios、vuex、route、neo4j-driver、neovis.js等。最后两个包用来实现图谱的可视化功能）<br>
后端开发：python+flask框架（将问答语句和后台管理的数据返回）<br>
深度学习环境：tensorflow1.14.0+keras2.2.5+cuda+cudnn（本项目涉及到对医疗文本语句的分类识别训练，使用了自然语言处理中的Bert模型和BiLSTM-CRF模型进行意图识别和实体识别）<br>
数据库：mongodb（存储爬虫爬取下来的医疗数据）、mysql（存储用户等后台管理信息）、neo4j（图数据库存储医疗三元组信息）<br>

深度学习部分参考并引用开源项目，同时开发了接口供前后端使用：https://github.com/wangle1218/KBQA-for-Diagnosis<br>
b站演示视频：https://www.bilibili.com/video/BV1gm421p7J3/?spm_id_from=333.999.list.card_archive.click&vd_source=99514f26313fa9f8c2037ed8c1bc2d6a<br>
csdn部分讲解：
（一）https://blog.csdn.net/m0_51177881/article/details/144688388?spm=1001.2014.3001.5501<br>
（二）https://blog.csdn.net/m0_51177881/article/details/144727394?spm=1001.2014.3001.5501<br>
 (三)https://blog.csdn.net/m0_51177881/article/details/144754910?spm=1001.2014.3001.5501
