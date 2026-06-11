-- 悦普 AI 后端 MySQL 8.x 初始化脚本
-- 默认数据库：yapmitai
-- 字符集：utf8mb4
--
-- 说明：
-- 1. 本脚本使用 CREATE TABLE IF NOT EXISTS，不会删除已有表或数据。
-- 2. 如果已有旧表需要更新结构，应使用数据库迁移工具，而不是重复执行本文件。

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `yapmitai`
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE `yapmitai`;

-- ============================================================
-- 1. 模型配置
-- 同时保存对话模型和 Embedding 模型配置。
-- ============================================================
CREATE TABLE IF NOT EXISTS `model_configs` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `provider_code` VARCHAR(50) NOT NULL COMMENT '供应商代码，例如 deepseek、openai',
    `provider_name` VARCHAR(100) NOT NULL COMMENT '供应商显示名称',
    `model_code` VARCHAR(100) NOT NULL COMMENT 'API 使用的模型代码',
    `display_name` VARCHAR(100) NOT NULL COMMENT '模型显示名称',
    `model_type` VARCHAR(20) NOT NULL COMMENT '模型类型：chat 或 embedding',
    `api_base_url` VARCHAR(500) NOT NULL COMMENT '模型 API 基础地址',
    `api_key_encrypted` TEXT NOT NULL COMMENT '加密后的 API Key',
    `api_key_last4` VARCHAR(10) NULL COMMENT 'API Key 后四位，用于界面展示',
    `dimension` INT NULL COMMENT 'Embedding 向量维度',
    `max_input_tokens` INT NULL COMMENT 'Embedding 模型最大输入 Token 数',
    `context_window_tokens` INT NULL COMMENT '对话模型上下文窗口 Token 数',
    `max_output_tokens` INT NULL COMMENT '对话模型最大输出 Token 数',
    `default_temperature` DOUBLE NULL COMMENT '对话模型默认温度',
    `enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    `is_default` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为该类型默认模型',
    `remark` TEXT NULL COMMENT '备注',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_model_configs_provider_model_type`
        (`provider_code`, `model_code`, `model_type`),
    KEY `ix_model_configs_provider_code` (`provider_code`),
    KEY `ix_model_configs_model_code` (`model_code`),
    KEY `ix_model_configs_model_type` (`model_type`),
    KEY `ix_model_configs_enabled` (`enabled`),
    KEY `ix_model_configs_is_default` (`is_default`),
    CONSTRAINT `ck_model_configs_model_type`
        CHECK (`model_type` IN ('chat', 'embedding')),
    CONSTRAINT `ck_model_configs_type_fields`
        CHECK (
            (
                `model_type` = 'chat'
                AND `context_window_tokens` IS NOT NULL
                AND `max_output_tokens` IS NOT NULL
            )
            OR
            (
                `model_type` = 'embedding'
                AND `dimension` IS NOT NULL
                AND `max_input_tokens` IS NOT NULL
            )
        )
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='模型配置';

-- ============================================================
-- 2. 智能体
-- 保存智能体基础配置、使用模型、提示词和业务指标。
-- ============================================================
CREATE TABLE IF NOT EXISTS `agents` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(100) NOT NULL COMMENT '智能体名称',
    `avatar` VARCHAR(500) NULL COMMENT '头像地址',
    `chat_model_config_id` INT NULL COMMENT '使用的对话模型配置 ID',
    `system_prompt` TEXT NOT NULL COMMENT '系统提示词',
    `category` VARCHAR(50) NOT NULL COMMENT '所属分类',
    `status` VARCHAR(30) NOT NULL COMMENT '运行状态',
    `enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    `today_done` INT NOT NULL DEFAULT 0 COMMENT '今日完成数量',
    `month_kpi` INT NOT NULL DEFAULT 0 COMMENT '本月 KPI',
    PRIMARY KEY (`id`),
    KEY `ix_agents_chat_model_config_id` (`chat_model_config_id`),
    KEY `ix_agents_category` (`category`),
    KEY `ix_agents_status` (`status`),
    CONSTRAINT `fk_agents_chat_model_config`
        FOREIGN KEY (`chat_model_config_id`)
        REFERENCES `model_configs` (`id`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='智能体';

-- ============================================================
-- 3. AI 工具
-- 保存 Prompt 技能或工具的定义、模型和输入输出结构。
-- ============================================================
CREATE TABLE IF NOT EXISTS `ai_tools` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name` VARCHAR(100) NOT NULL COMMENT '工具名称',
    `name_en` VARCHAR(150) NULL COMMENT '工具英文名称',
    `code` VARCHAR(80) NOT NULL COMMENT '工具唯一代码',
    `category` VARCHAR(50) NOT NULL COMMENT '工具分类',
    `description` TEXT NULL COMMENT '工具描述',
    `icon` VARCHAR(100) NULL COMMENT '图标',
    `model_config_id` INT NULL COMMENT '使用的模型配置 ID',
    `prompt_template` TEXT NOT NULL COMMENT 'Prompt 模板',
    `input_schema` JSON NULL COMMENT '输入参数结构',
    `output_schema` JSON NULL COMMENT '输出结果结构',
    `enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用',
    `is_system` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否为系统内置工具',
    `call_count` INT NOT NULL DEFAULT 0 COMMENT '调用次数',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序值',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_ai_tools_code` (`code`),
    KEY `ix_ai_tools_category` (`category`),
    KEY `ix_ai_tools_model_config_id` (`model_config_id`),
    KEY `ix_ai_tools_enabled` (`enabled`),
    KEY `ix_ai_tools_is_system` (`is_system`),
    KEY `ix_ai_tools_sort_order` (`sort_order`),
    CONSTRAINT `fk_ai_tools_model_config`
        FOREIGN KEY (`model_config_id`)
        REFERENCES `model_configs` (`id`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 工具';

-- ============================================================
-- 4. 企业知识库
-- 保存知识库本身的信息，文档内容和向量保存在其他存储中。
-- ============================================================
CREATE TABLE IF NOT EXISTS `knowledge_bases` (
    `id` VARCHAR(50) NOT NULL COMMENT '知识库 ID',
    `name` VARCHAR(100) NOT NULL COMMENT '知识库名称',
    `description` TEXT NOT NULL COMMENT '知识库描述',
    `knowledge_type` VARCHAR(20) NOT NULL DEFAULT 'text' COMMENT '知识类型',
    `status` VARCHAR(30) NOT NULL DEFAULT 'ready' COMMENT '处理状态',
    `embedding_model_config_id` INT NULL COMMENT 'Embedding 模型配置 ID',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `ix_knowledge_bases_name` (`name`),
    KEY `ix_knowledge_bases_status` (`status`),
    KEY `ix_knowledge_bases_embedding_model_config_id`
        (`embedding_model_config_id`),
    CONSTRAINT `fk_knowledge_bases_embedding_model_config`
        FOREIGN KEY (`embedding_model_config_id`)
        REFERENCES `model_configs` (`id`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='企业知识库';

-- ============================================================
-- 5. Agent 调用日志
-- 保存接口调用耗时、状态、Token 和成本。
-- ============================================================
CREATE TABLE IF NOT EXISTS `agent_call_logs` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `agent_id` VARCHAR(100) NULL COMMENT '智能体标识',
    `module` VARCHAR(100) NOT NULL DEFAULT 'system' COMMENT '调用模块',
    `path` VARCHAR(500) NOT NULL DEFAULT '' COMMENT '请求路径',
    `method` VARCHAR(20) NOT NULL DEFAULT 'GET' COMMENT 'HTTP 方法',
    `request_at` DATETIME(6) NOT NULL COMMENT '请求时间',
    `response_at` DATETIME(6) NULL COMMENT '响应时间',
    `status` VARCHAR(30) NOT NULL COMMENT '调用状态',
    `latency_ms` INT NOT NULL DEFAULT 0 COMMENT '耗时，单位毫秒',
    `cost` DOUBLE NOT NULL DEFAULT 0 COMMENT '调用成本',
    `prompt_tokens` INT NOT NULL DEFAULT 0 COMMENT '输入 Token 数',
    `completion_tokens` INT NOT NULL DEFAULT 0 COMMENT '输出 Token 数',
    `total_tokens` INT NOT NULL DEFAULT 0 COMMENT '总 Token 数',
    `error_msg` TEXT NULL COMMENT '错误信息',
    PRIMARY KEY (`id`),
    KEY `ix_agent_call_logs_agent_id` (`agent_id`),
    KEY `ix_agent_call_logs_module` (`module`),
    KEY `ix_agent_call_logs_status` (`status`)
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='Agent 调用日志';

-- ============================================================
-- 6. 智能体与知识库关联
-- 一个智能体可以关联多个知识库。
-- ============================================================
CREATE TABLE IF NOT EXISTS `agent_knowledge_bases` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `agent_id` INT NOT NULL COMMENT '智能体 ID',
    `knowledge_base_id` VARCHAR(50) NOT NULL COMMENT '知识库 ID',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_agent_knowledge_base`
        (`agent_id`, `knowledge_base_id`),
    KEY `ix_agent_knowledge_bases_agent_id` (`agent_id`),
    KEY `ix_agent_knowledge_bases_knowledge_base_id` (`knowledge_base_id`),
    CONSTRAINT `fk_agent_knowledge_bases_agent`
        FOREIGN KEY (`agent_id`)
        REFERENCES `agents` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT `fk_agent_knowledge_bases_knowledge_base`
        FOREIGN KEY (`knowledge_base_id`)
        REFERENCES `knowledge_bases` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='智能体与知识库关联';

-- ============================================================
-- 7. 历史会话
-- 每次与智能体的连续对话对应一条会话记录。
-- ============================================================
CREATE TABLE IF NOT EXISTS `conversations` (
    `id` VARCHAR(60) NOT NULL COMMENT '会话 ID',
    `agent_id` INT NULL COMMENT '智能体 ID',
    `title` VARCHAR(300) NOT NULL COMMENT '会话标题',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
        ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `ix_conversations_agent_id` (`agent_id`),
    CONSTRAINT `fk_conversations_agent`
        FOREIGN KEY (`agent_id`)
        REFERENCES `agents` (`id`)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='历史会话';

-- ============================================================
-- 8. 知识库文档
-- 保存上传文件的元数据和解析、向量化处理状态。
-- ============================================================
CREATE TABLE IF NOT EXISTS `knowledge_documents` (
    `id` VARCHAR(60) NOT NULL COMMENT '文档 ID',
    `knowledge_base_id` VARCHAR(50) NOT NULL COMMENT '所属知识库 ID',
    `filename` VARCHAR(500) NOT NULL COMMENT '原始文件名',
    `storage_path` VARCHAR(1000) NOT NULL COMMENT '文件存储路径',
    `content_type` VARCHAR(150) NOT NULL COMMENT '文件 MIME 类型',
    `size` INT NOT NULL COMMENT '文件大小，单位字节',
    `processing_status` VARCHAR(30) NOT NULL DEFAULT 'processing'
        COMMENT '处理状态',
    `chunk_count` INT NOT NULL DEFAULT 0 COMMENT '生成的知识切片数量',
    `error_message` TEXT NULL COMMENT '处理失败信息',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `ix_knowledge_documents_knowledge_base_id` (`knowledge_base_id`),
    KEY `ix_knowledge_documents_processing_status` (`processing_status`),
    CONSTRAINT `fk_knowledge_documents_knowledge_base`
        FOREIGN KEY (`knowledge_base_id`)
        REFERENCES `knowledge_bases` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='知识库文档';

-- ============================================================
-- 9. AI 工具最近输出
-- 保存工具运行结果，用于 Recent Outputs。
-- ============================================================
CREATE TABLE IF NOT EXISTS `skill_run_records` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `skill_id` INT NOT NULL COMMENT 'AI 工具 ID',
    `title` VARCHAR(150) NOT NULL COMMENT '结果标题',
    `target` VARCHAR(200) NULL COMMENT '目标',
    `suggested_action` TEXT NULL COMMENT '建议动作',
    `deliverables` TEXT NULL COMMENT '交付物',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `ix_skill_run_records_skill_id` (`skill_id`),
    CONSTRAINT `fk_skill_run_records_ai_tool`
        FOREIGN KEY (`skill_id`)
        REFERENCES `ai_tools` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='AI 工具最近输出';

-- ============================================================
-- 10. 会话消息
-- 保存用户和智能体的历史消息，以及 RAG 命中来源。
-- ============================================================
CREATE TABLE IF NOT EXISTS `messages` (
    `id` VARCHAR(60) NOT NULL COMMENT '消息 ID',
    `conversation_id` VARCHAR(60) NOT NULL COMMENT '会话 ID',
    `role` VARCHAR(30) NOT NULL COMMENT '消息角色，例如 user、assistant',
    `content` TEXT NOT NULL COMMENT '消息正文',
    `model` VARCHAR(150) NULL COMMENT '回答使用的模型',
    `sources` JSON NOT NULL COMMENT 'RAG 命中的知识来源',
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '创建时间',
    PRIMARY KEY (`id`),
    KEY `ix_messages_conversation_id` (`conversation_id`),
    KEY `ix_messages_role` (`role`),
    CONSTRAINT `fk_messages_conversation`
        FOREIGN KEY (`conversation_id`)
        REFERENCES `conversations` (`id`)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARACTER SET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='会话消息';
