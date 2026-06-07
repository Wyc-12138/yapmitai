import { miniStat, page, progress, statusBadge } from "../../../../shared/ui.js";

const typeLabel = (type) => (type === "image" ? "图片" : "文本");

function localKnowledgeTable(context) {
  const keyword = context.knowledgeKeyword.trim().toLowerCase();
  const filtered = keyword
    ? context.localLibraries.filter(
        (item) =>
          item.name.toLowerCase().includes(keyword) ||
          item.description.toLowerCase().includes(keyword)
      )
    : context.localLibraries;
  const pageSize = 4;
  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const currentPage = Math.min(context.knowledgePage, totalPages);
  const items = filtered.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return `
    <section class="knowledge-table-section">
      <div class="knowledge-table-toolbar">
        <div><h2>本地知识库</h2><span>共 ${filtered.length} 个知识库</span></div>
        <div class="knowledge-actions">
          <div class="knowledge-search">
            <input id="knowledge-search" value="${context.knowledgeKeyword}" placeholder="搜索名称或描述">
            <button class="ghost-btn" data-action="search-knowledge">搜索</button>
          </div>
          <button class="primary-btn" data-action="open-knowledge-create">+ 添加知识库</button>
        </div>
      </div>
      <div class="table-wrap knowledge-table">
        <table>
          <thead><tr>
            <th>知识库名称</th><th>知识库描述</th><th>类型</th>
            <th>上传文档</th><th>创建时间</th><th>操作</th>
          </tr></thead>
          <tbody>
            ${items.length ? items.map((library) => `
              <tr>
                <td><strong>${library.name}</strong></td>
                <td><span class="knowledge-description">${library.description}</span></td>
                <td><span class="knowledge-type ${library.knowledgeType}">${typeLabel(library.knowledgeType)}</span></td>
                <td>
                  <label class="upload-btn">
                    上传${library.knowledgeType === "image" ? "图片" : "文档"}
                    <input type="file" data-knowledge-upload="${library.id}" accept="${library.knowledgeType === "image" ? "image/*" : ".txt,.md,.pdf,.doc,.docx"}">
                  </label>
                  <small>${library.collectionCount} 个文档</small>
                </td>
                <td>${library.createdAt}</td>
                <td><div class="row-actions">
                  <button class="tiny-btn" data-knowledge-detail="${library.id}">查看文档</button>
                  <button class="danger-btn" data-knowledge-delete="${library.id}">删除</button>
                </div></td>
              </tr>`).join("") : `<tr><td colspan="6"><div class="empty-state">暂无知识库</div></td></tr>`}
          </tbody>
        </table>
      </div>
      <div class="pagination">
        <button class="icon-btn" data-knowledge-page="${Math.max(1, currentPage - 1)}" ${currentPage === 1 ? "disabled" : ""}>‹</button>
        ${Array.from({ length: totalPages }, (_, index) => index + 1)
          .map((number) => `<button class="${number === currentPage ? "active" : ""}" data-knowledge-page="${number}">${number}</button>`)
          .join("")}
        <button class="icon-btn" data-knowledge-page="${Math.min(totalPages, currentPage + 1)}" ${currentPage === totalPages ? "disabled" : ""}>›</button>
      </div>
    </section>`;
}

function createModal() {
  return `
    <div class="modal-backdrop" data-action="close-knowledge-create">
      <div class="modal knowledge-modal" data-stop>
        <div class="modal-title-row">
          <div><h2>添加知识库</h2><span>创建后可上传文本或图片文档</span></div>
          <button class="icon-btn" data-action="close-knowledge-create">×</button>
        </div>
        <label class="field-label required">知识库名称</label>
        <input id="knowledge-name" placeholder="请输入知识库名称">
        <label class="field-label required">知识库类型</label>
        <select id="knowledge-type"><option value="text">文本</option><option value="image">图片</option></select>
        <label class="field-label required">知识库描述</label>
        <textarea id="knowledge-description" placeholder="请输入知识库描述"></textarea>
        <div id="knowledge-form-error" class="form-error"></div>
        <div class="modal-actions">
          <button class="primary-btn" data-action="create-knowledge">确定添加</button>
          <button class="ghost-btn" data-action="close-knowledge-create">取消</button>
        </div>
      </div>
    </div>`;
}

function detailModal(library) {
  const documents = library.documents || [];
  return `
    <div class="modal-backdrop" data-action="close-knowledge-detail">
      <div class="modal knowledge-modal" data-stop>
        <div class="modal-title-row">
          <div><h2>${library.name}</h2><span>本地知识库详情</span></div>
          <button class="icon-btn" data-action="close-knowledge-detail">×</button>
        </div>
        <div class="knowledge-detail-grid">
          <div><span>类型</span><strong>${typeLabel(library.knowledgeType)}</strong></div>
          <div><span>文档数量</span><strong>${library.collectionCount}</strong></div>
          <div><span>Embedding</span><strong>${library.embeddingModel || "-"}</strong></div>
          <div><span>回答模型</span><strong>${library.answerModel || "-"}</strong></div>
        </div>
        <div class="knowledge-detail-description"><span>知识库描述</span><p>${library.description}</p></div>
        <div class="collection-placeholder">
          <strong>已索引文档</strong>
          <p>${documents.length ? documents.map((item) => `${item.filename}（${item.chunkCount} 个切片）`).join("<br>") : "当前还没有上传文档。"}</p>
        </div>
        <button class="primary-btn full" data-action="close-knowledge-detail">关闭</button>
      </div>
    </div>`;
}

function localRagWorkspace(context) {
  const result = context.ragResult;
  return `
    <section class="local-rag-workspace">
      <div class="rag-workspace-head">
        <div>
          <h2>本地知识库真实问答</h2>
          <span>Embedding 检索 Chroma，回答模型根据命中切片生成答案</span>
        </div>
        <span class="api-state ${context.externalAiConfigured ? "ready" : "missing"}">
          ${context.externalAiConfigured ? "外部模型 API 已连接" : "未配置 EXTERNAL_AI_API_KEY"}
        </span>
      </div>
      <div class="rag-input-row">
        <textarea id="local-rag-question" placeholder="输入一个只能通过已上传文档回答的问题">${context.ragQuestion}</textarea>
        <button class="primary-btn" data-action="ask-local-knowledge" ${context.ragBusy || !context.selectedKnowledgeBaseId ? "disabled" : ""}>
          ${context.ragBusy ? "检索并生成中…" : "真实提问"}
        </button>
      </div>
      ${context.ragError ? `<div class="model-call-result error">${context.ragError}</div>` : ""}
      ${result ? `
        <div class="rag-answer">
          <div class="rag-answer-meta">
            <strong>${result.model}</strong>
            <span>会话 ${result.conversationId}</span>
            <span>Token ${result.usage?.total_tokens ?? result.usage?.totalTokens ?? "-"}</span>
          </div>
          <p>${result.answer}</p>
          <details>
            <summary>查看命中的 ${result.contexts?.length || 0} 个知识切片</summary>
            ${(result.contexts || []).map((item) => `<blockquote>${item}</blockquote>`).join("")}
          </details>
        </div>` : ""}
    </section>`;
}

export default {
  path: "/enterprise/knowledge/agent",
  layout: "shell",
  render(context) {
    return page(
      "企业智库",
      "Enterprise Knowledge Center",
      "统一管理外部 Agent 向量库与企业本地知识资产。",
      `
      <div class="knowledge-columns">
        <section class="knowledge-source external">
          <div class="knowledge-source-head">
            <div class="knowledge-source-icon">外</div>
            <div><h2>外部 Agent 向量库</h2><span>External Agent Vector Store</span></div>
            ${statusBadge("working")}
          </div>
          <p>通过 Agent Gateway 接入外部向量数据库。该区域不使用本地知识库的模型配置。</p>
          <div class="mini-stat-grid">${miniStat("向量条目", "1,284")}${miniStat("索引集合", "24")}</div>
          ${progress("同步状态", 100)}
          <div class="knowledge-meta"><span>上次同步：2 分钟前</span><span>由外部 Agent 管理</span></div>
          <button class="primary-btn full" data-action="sync-knowledge">立即同步外部向量库</button>
          <div id="sync-result"></div>
        </section>
        <section class="knowledge-source local">
          <div class="knowledge-source-head">
            <div class="knowledge-source-icon">本</div>
            <div><h2>本地知识库</h2><span>PostgreSQL + Chroma</span></div>
            <span class="status-badge standby">本地托管</span>
          </div>
          <p>文件信息保存在 PostgreSQL，文档切片和 Embedding 向量保存在 Chroma。</p>
          <div class="mini-stat-grid">
            ${miniStat("知识库", String(context.localLibraries.length))}
            ${miniStat("文档总数", String(context.localLibraries.reduce((sum, item) => sum + item.collectionCount, 0)))}
          </div>
          <label class="model-library-picker">
            <span>当前配置的本地知识库</span>
            <select id="local-model-knowledge-base" ${context.localLibraries.length ? "" : "disabled"}>
              ${context.localLibraries.length
                ? context.localLibraries.map((item) => `<option value="${item.id}" ${context.selectedKnowledgeBaseId === item.id ? "selected" : ""}>${item.name}</option>`).join("")
                : `<option value="">请先创建知识库</option>`}
            </select>
          </label>
          <div class="model-switch-block">
            <div class="model-switch-title"><span>Embedding 模型</span><small>仅作用于本地知识库</small></div>
            <div class="model-buttons">${context.embeddingModels.map((model) => `<button class="${context.embeddingModel === model ? "active" : ""}" data-embedding-model="${model}">${model}</button>`).join("")}</div>
          </div>
          <div class="model-switch-block">
            <div class="model-switch-title"><span>回答生成模型</span><small>仅作用于本地知识库 RAG</small></div>
            <div class="model-buttons">${context.answerModels.map((model) => `<button class="${context.answerModel === model ? "active" : ""}" data-answer-model="${model}">${model}</button>`).join("")}</div>
          </div>
          <div class="local-model-actions">
            <button class="ghost-btn" data-action="test-local-models" ${context.modelBusy || !context.selectedKnowledgeBaseId ? "disabled" : ""}>
              ${context.modelBusy ? "真实调用中…" : "测试 Embedding + 回答模型"}
            </button>
            <button class="primary-btn" data-action="open-knowledge-create">添加本地知识库</button>
          </div>
          ${context.modelActionStatus ? `<div class="model-call-result ${context.modelTestResult ? "success" : ""}">${context.modelActionStatus}</div>` : ""}
          ${context.modelTestResult ? `
            <div class="model-test-grid">
              <div><span>Embedding</span><strong>${context.modelTestResult.embeddingModel}</strong><small>${context.modelTestResult.embeddingDimensions} 维向量</small></div>
              <div><span>回答模型</span><strong>${context.modelTestResult.answerModel}</strong><small>${context.modelTestResult.answer}</small></div>
            </div>` : ""}
        </section>
      </div>
      ${localRagWorkspace(context)}
      ${localKnowledgeTable(context)}
      ${context.knowledgeCreateOpen ? createModal() : ""}
      ${context.selectedKnowledge ? detailModal(context.selectedKnowledge) : ""}
      `
    );
  }
};
