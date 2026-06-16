-- YAPMITAI PostgreSQL 中文备注
-- 可重复执行，不修改表数据。

COMMENT ON TABLE model_configs IS '模型配置表：统一管理 Chat 与 Embedding 外部模型连接参数';
COMMENT ON COLUMN model_configs.id IS '主键，自增ID';
COMMENT ON COLUMN model_configs.provider_code IS '供应商程序编码，如 deepseek、openai';
COMMENT ON COLUMN model_configs.provider_name IS '供应商显示名称，如 DeepSeek、OpenAI';
COMMENT ON COLUMN model_configs.model_code IS 'API调用时使用的模型名称';
COMMENT ON COLUMN model_configs.display_name IS '前端页面展示名称';
COMMENT ON COLUMN model_configs.model_type IS '模型类型：chat 或 embedding';
COMMENT ON COLUMN model_configs.api_base_url IS '模型API基础地址';
COMMENT ON COLUMN model_configs.api_key_encrypted IS '加密后的API Key';
COMMENT ON COLUMN model_configs.api_key_last4 IS 'API Key后四位，用于页面脱敏显示';
COMMENT ON COLUMN model_configs.dimension IS 'Embedding模型输出向量维度';
COMMENT ON COLUMN model_configs.max_input_tokens IS 'Embedding模型单段文本最大输入Token数';
COMMENT ON COLUMN model_configs.context_window_tokens IS 'Chat模型输入与输出合计的上下文窗口Token数';
COMMENT ON COLUMN model_configs.max_output_tokens IS 'Chat模型单次最大输出Token数';
COMMENT ON COLUMN model_configs.default_temperature IS 'Chat模型默认生成温度';
COMMENT ON COLUMN model_configs.enabled IS '是否启用该模型配置';
COMMENT ON COLUMN model_configs.is_default IS '是否为该模型类型的默认配置';
COMMENT ON COLUMN model_configs.remark IS '模型配置备注';
COMMENT ON COLUMN model_configs.created_at IS '创建时间';
COMMENT ON COLUMN model_configs.updated_at IS '最后更新时间';

COMMENT ON TABLE agents IS '智能体表：保存智能体基本信息、Chat模型和运行状态';
COMMENT ON COLUMN agents.id IS '智能体主键ID';
COMMENT ON COLUMN agents.name IS '智能体名称';
COMMENT ON COLUMN agents.avatar IS '智能体头像地址';
COMMENT ON COLUMN agents.chat_model_config_id IS '关联的Chat模型配置ID，指向model_configs.id';
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = 'agents'
          AND column_name = 'model'
    ) THEN
        COMMENT ON COLUMN agents.model IS
            '旧版兼容模型字段，当前业务使用chat_model_config_id关联模型配置';
    END IF;
END $$;
COMMENT ON COLUMN agents.system_prompt IS '智能体系统提示词';
COMMENT ON COLUMN agents.category IS '智能体业务分类';
COMMENT ON COLUMN agents.status IS '智能体当前运行状态';
COMMENT ON COLUMN agents.enabled IS '智能体是否启用';
COMMENT ON COLUMN agents.today_done IS '智能体今日完成任务数量';
COMMENT ON COLUMN agents.month_kpi IS '智能体本月KPI数值';

COMMENT ON TABLE knowledge_bases IS '本地知识库表：保存知识库信息及其Embedding模型配置';
COMMENT ON COLUMN knowledge_bases.id IS '知识库主键ID';
COMMENT ON COLUMN knowledge_bases.name IS '知识库名称';
COMMENT ON COLUMN knowledge_bases.description IS '知识库描述';
COMMENT ON COLUMN knowledge_bases.knowledge_type IS '知识库类型，如text或image';
COMMENT ON COLUMN knowledge_bases.status IS '知识库处理状态';
COMMENT ON COLUMN knowledge_bases.embedding_model_config_id IS '关联的Embedding模型配置ID，指向model_configs.id';
COMMENT ON COLUMN knowledge_bases.created_at IS '创建时间';
COMMENT ON COLUMN knowledge_bases.updated_at IS '最后更新时间';

COMMENT ON TABLE knowledge_documents IS '知识库文档表：记录上传文件、存储位置和向量化处理状态';
COMMENT ON COLUMN knowledge_documents.id IS '文档主键ID';
COMMENT ON COLUMN knowledge_documents.knowledge_base_id IS '所属知识库ID，指向knowledge_bases.id';
COMMENT ON COLUMN knowledge_documents.filename IS '上传时的原始文件名';
COMMENT ON COLUMN knowledge_documents.storage_path IS '原始文件在服务器中的存储路径';
COMMENT ON COLUMN knowledge_documents.content_type IS '文件MIME类型';
COMMENT ON COLUMN knowledge_documents.size IS '文件大小，单位为字节';
COMMENT ON COLUMN knowledge_documents.processing_status IS '文档解析和向量化处理状态';
COMMENT ON COLUMN knowledge_documents.chunk_count IS '文档切片数量';
COMMENT ON COLUMN knowledge_documents.error_message IS '处理失败时的错误信息';
COMMENT ON COLUMN knowledge_documents.created_at IS '上传创建时间';

COMMENT ON TABLE agent_knowledge_bases IS '智能体与知识库关联表：记录智能体可使用的本地知识库';
COMMENT ON COLUMN agent_knowledge_bases.id IS '关联记录主键ID';
COMMENT ON COLUMN agent_knowledge_bases.agent_id IS '智能体ID，指向agents.id';
COMMENT ON COLUMN agent_knowledge_bases.knowledge_base_id IS '知识库ID，指向knowledge_bases.id';
COMMENT ON COLUMN agent_knowledge_bases.created_at IS '关联创建时间';

COMMENT ON TABLE conversations IS '对话会话表：保存一次智能体对话的会话信息';
COMMENT ON COLUMN conversations.id IS '会话主键ID';
COMMENT ON COLUMN conversations.agent_id IS '参与对话的智能体ID，指向agents.id';
COMMENT ON COLUMN conversations.title IS '会话标题';
COMMENT ON COLUMN conversations.created_at IS '会话创建时间';
COMMENT ON COLUMN conversations.updated_at IS '会话最后更新时间';

COMMENT ON TABLE messages IS '对话消息表：保存用户问题、AI回答和引用来源';
COMMENT ON COLUMN messages.id IS '消息主键ID';
COMMENT ON COLUMN messages.conversation_id IS '所属会话ID，指向conversations.id';
COMMENT ON COLUMN messages.role IS '消息角色，如user、assistant或system';
COMMENT ON COLUMN messages.content IS '消息正文内容';
COMMENT ON COLUMN messages.model IS '生成该消息时使用的模型编码';
COMMENT ON COLUMN messages.sources IS 'RAG回答引用的知识来源，JSON数组';
COMMENT ON COLUMN messages.created_at IS '消息创建时间';

COMMENT ON TABLE agent_call_logs IS '调用日志表：记录接口和模型调用的耗时、Token、费用与异常';
COMMENT ON COLUMN agent_call_logs.id IS '调用日志主键ID';
COMMENT ON COLUMN agent_call_logs.agent_id IS '相关智能体或调用方标识';
COMMENT ON COLUMN agent_call_logs.module IS '所属业务模块';
COMMENT ON COLUMN agent_call_logs.path IS '请求接口路径';
COMMENT ON COLUMN agent_call_logs.method IS 'HTTP请求方法';
COMMENT ON COLUMN agent_call_logs.request_at IS '请求开始时间';
COMMENT ON COLUMN agent_call_logs.response_at IS '响应完成时间';
COMMENT ON COLUMN agent_call_logs.status IS '调用状态';
COMMENT ON COLUMN agent_call_logs.latency_ms IS '调用耗时，单位为毫秒';
COMMENT ON COLUMN agent_call_logs.cost IS '本次调用估算费用';
COMMENT ON COLUMN agent_call_logs.prompt_tokens IS '输入Token数量';
COMMENT ON COLUMN agent_call_logs.completion_tokens IS '输出Token数量';
COMMENT ON COLUMN agent_call_logs.total_tokens IS '输入与输出Token总数';
COMMENT ON COLUMN agent_call_logs.error_msg IS '调用失败时的错误信息';

COMMENT ON TABLE ai_tools IS 'AI工具表：保存Prompt Skill工具定义、模型配置和前端展示信息';
COMMENT ON COLUMN ai_tools.id IS '主键，自增ID';
COMMENT ON COLUMN ai_tools.name IS '技能名称';
COMMENT ON COLUMN ai_tools.name_en IS '英文名称';
COMMENT ON COLUMN ai_tools.code IS '唯一编码';
COMMENT ON COLUMN ai_tools.category IS '分类';
COMMENT ON COLUMN ai_tools.description IS '技能说明';
COMMENT ON COLUMN ai_tools.icon IS '图标或图标文字';
COMMENT ON COLUMN ai_tools.model_config_id IS '使用的Chat模型配置ID，指向model_configs.id';
COMMENT ON COLUMN ai_tools.prompt_template IS 'Prompt模板，支持{{task}}占位符';
COMMENT ON COLUMN ai_tools.input_schema IS '输入字段配置，JSONB';
COMMENT ON COLUMN ai_tools.output_schema IS '输出格式配置，JSONB';
COMMENT ON COLUMN ai_tools.enabled IS '是否启用';
COMMENT ON COLUMN ai_tools.is_system IS '是否系统内置';
COMMENT ON COLUMN ai_tools.call_count IS '调用次数';
COMMENT ON COLUMN ai_tools.sort_order IS '排序值';
COMMENT ON COLUMN ai_tools.created_at IS '创建时间';
COMMENT ON COLUMN ai_tools.updated_at IS '更新时间';

COMMENT ON TABLE skill_run_records IS '技能运行记录表：保存AI工具最近运行结果历史';
COMMENT ON COLUMN skill_run_records.id IS '主键，自增ID';
COMMENT ON COLUMN skill_run_records.skill_id IS '关联技能ID，指向ai_tools.id';
COMMENT ON COLUMN skill_run_records.title IS '结果标题，如AI多语言文案 · 结果包';
COMMENT ON COLUMN skill_run_records.target IS '结果中的目标';
COMMENT ON COLUMN skill_run_records.suggested_action IS '结果中的建议动作';
COMMENT ON COLUMN skill_run_records.deliverables IS '结果中的交付物';
COMMENT ON COLUMN skill_run_records.created_at IS '生成时间';

COMMENT ON TABLE workflow_tasks IS '工作流任务表：每个任务绑定一个AI团队并保存发布状态';
COMMENT ON COLUMN workflow_tasks.id IS '工作流任务主键ID';
COMMENT ON COLUMN workflow_tasks.team_id IS '关联的AI团队ID，指向ai_teams.id';
COMMENT ON COLUMN workflow_tasks.name IS '工作流任务名称';
COMMENT ON COLUMN workflow_tasks.description IS '任务目标、说明和交付要求';
COMMENT ON COLUMN workflow_tasks.enabled IS '是否启用该工作流';
COMMENT ON COLUMN workflow_tasks.status IS '工作流状态：draft、ready、running、completed或failed';
COMMENT ON COLUMN workflow_tasks.created_at IS '创建时间';
COMMENT ON COLUMN workflow_tasks.updated_at IS '最后更新时间';

COMMENT ON TABLE workflow_task_agents IS '工作流任务员工表：保存团队员工的执行顺序和实时状态';
COMMENT ON COLUMN workflow_task_agents.id IS '任务员工关联主键ID';
COMMENT ON COLUMN workflow_task_agents.task_id IS '所属工作流任务ID';
COMMENT ON COLUMN workflow_task_agents.agent_id IS 'AI员工ID，指向agents.id';
COMMENT ON COLUMN workflow_task_agents.sort_order IS 'Agent在线性工作流中的执行顺序';
COMMENT ON COLUMN workflow_task_agents.run_status IS '当前执行状态：idle、queued、running、completed或failed';
COMMENT ON COLUMN workflow_task_agents.output IS 'Agent本次执行的结构化输出，JSON格式';
COMMENT ON COLUMN workflow_task_agents.error_message IS 'Agent执行失败时的错误信息';
COMMENT ON COLUMN workflow_task_agents.started_at IS 'Agent开始执行时间';
COMMENT ON COLUMN workflow_task_agents.finished_at IS 'Agent完成执行时间';

COMMENT ON TABLE workflow_runs IS '工作流运行记录表：记录顺序执行过程和最终PDF报告';
COMMENT ON COLUMN workflow_runs.id IS '运行记录唯一ID';
COMMENT ON COLUMN workflow_runs.task_id IS '所属工作流任务ID';
COMMENT ON COLUMN workflow_runs.status IS '运行状态：running、completed或failed';
COMMENT ON COLUMN workflow_runs.current_agent_id IS '当前正在执行的AI员工ID';
COMMENT ON COLUMN workflow_runs.prompt IS '用户输入的一句话需求';
COMMENT ON COLUMN workflow_runs.report_data IS '全部Agent输出汇总后的报告数据，JSON格式';
COMMENT ON COLUMN workflow_runs.pdf_path IS '最终PDF报告在服务器中的存储路径';
COMMENT ON COLUMN workflow_runs.error_message IS '运行失败时的错误信息';
COMMENT ON COLUMN workflow_runs.started_at IS '运行开始时间';
COMMENT ON COLUMN workflow_runs.completed_at IS '运行完成时间';
