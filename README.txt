YAPMITAI Growth Team Agent 开发需求书 v1.0
开发负责人：黄冠钰
项目周期：2-3周

项目目标：
完成YAPMITAI Growth Team四大智能体开发，并接入统一Workflow，实现：
用户输入一句需求
↓
AI市场分析师
↓
AI品牌营销经理
↓
AI内容创作官
↓
AI投流专家
↓
自动生成完整品牌增长方案

一、项目目标
用户输入：
“我要把海南椰子水卖到马来西亚市场”
系统自动生成：
1.市场分析报告
2.品牌定位方案
3.内容资产包
4.广告投放方案
最终输出：
PDF增长报告
全流程控制在：
2-5分钟

二、技术要求
开发语言：
Python
框架：
FastAPI
Agent框架：
LangGraph
大模型：
GPT-4o
备用：
Claude
搜索工具：
Tavily
数据库：
PostgreSQL
向量库：
Chroma

三、统一Agent接口
所有Agent必须继承：
BaseAgent
统一输入：
{ “task_id”:““,”product”:““,”market”:““,”target_customer”:““,”budget”:“” }
统一输出：
{ “agent_name”:““,”status”:“success”, “result”:{} }
禁止Agent互相直接调用。
必须通过Workflow传递结果。

四、Agent01 市场分析师
名称：
AI Market Analyst
职责：
分析目标市场
输出市场报告

输入：
产品名称
目标国家
目标用户

调用工具：
GPT
Tavily Search

输出字段：
{ “market_size”:““,”industry_trend”:““,”target_customer”:““,”top_competitors”:[], “opportunities”:[] }

必须输出：
1 市场规模
2 用户画像
3 行业趋势
4 TOP10竞品
5 市场机会

验收标准：
输出内容不少于1500字
JSON结构标准化
生成时间小于60秒

五、Agent02 品牌营销经理
名称：
AI Brand Marketing Manager
职责：
根据市场报告制定品牌战略

输入：
市场分析报告

输出：
{ “positioning”:““,”slogan”:““,”usp”:““,”channel_strategy”:““,”growth_strategy”:“” }

必须输出：
品牌定位
品牌口号
核心卖点
竞争优势
渠道策略
增长策略

验收标准：
输出不少于1000字
形成完整品牌战略文档

六、Agent03 内容创作官
名称：
AI Content Creator
职责：
根据品牌方案生成营销内容

输入：
品牌方案

输出：
TikTok脚本
Facebook广告文案
Instagram内容
小红书内容
EDM邮件

要求：
TikTok脚本
10条
Facebook广告
10条
Instagram内容
10条
小红书内容
10条
EDM邮件
5条

输出结构：
{ “tiktok”:[], “facebook”:[], “instagram”:[], “xiaohongshu”:[], “email”:[] }

验收标准：
内容总量不少于5000字
支持中英文

七、Agent04 AI投流专家
名称：
AI Media Buying Specialist
职责：
生成广告投放方案

输入：
市场报告
品牌方案
内容资产

输出：
{ “budget_plan”:{}, “audience”:{}, “channel_mix”:{}, “ab_testing”:[], “roi_prediction”:{} }

必须输出：
预算拆分
Meta预算
TikTok预算
Google预算

用户画像
年龄
性别
兴趣

A/B测试策略

ROI预测
CTR
CPA
ROAS

验收标准：
输出标准化JSON
支持导出PDF

八、Workflow开发
LangGraph实现：
START
↓
Market Analyst
↓
Brand Manager
↓
Content Creator
↓
Media Buying
↓
END

Workflow Context：
{ “market_report”:{}, “brand_strategy”:{}, “content_assets”:{}, “media_plan”:{} }
所有Agent读写统一Context

九、API接口
POST
/api/task/start
创建任务

GET
/api/task/{id}
查询任务状态

GET
/api/task/{id}/report
获取最终报告

十、PDF报告
生成：
Growth Strategy Report
内容：
第一页
项目摘要
第二页
市场分析
第三页
品牌战略
第四页
内容资产
第五页
广告方案
第六页
执行建议

十一、开发排期
Week1
完成：
Market Agent
Brand Agent

Week2
完成：
Content Agent
Media Buying Agent

Week3
完成：
Workflow
PDF
联调测试

十二、最终验收
必须满足：
用户创建任务
正常
四个Agent自动执行
正常
结果自动传递
正常
生成PDF
正常
总耗时
小于5分钟
代码提交Git仓库
部署测试环境
可公网访问
完成后进入YAPMITAI Agent Framework统一接入阶段。