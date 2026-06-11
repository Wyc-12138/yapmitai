<template>
  <section>
    <PageHeader eyebrow="Enterprise Knowledge Center" title="企业智库" description="统一管理外部 Agent 向量库与企业本地知识资产。" />
    <div class="knowledge-columns">
      <section class="knowledge-source external">
        <div class="knowledge-source-head"><div class="knowledge-source-icon">外</div><div><h2>外部 Agent 向量库</h2><span>External Agent Vector Store</span></div><span class="status-badge working">工作中</span></div>
        <p>通过 Agent Gateway 接入外部向量数据库。该区域不使用本地知识库的模型配置。</p>
        <div class="mini-stat-grid"><div class="mini-stat"><span>向量条目</span><strong>1,284</strong></div><div class="mini-stat"><span>索引集合</span><strong>24</strong></div></div>
        <ProgressBar label="同步状态" :value="100" /><div class="knowledge-meta"><span>上次同步：2 分钟前</span><span>由外部 Agent 管理</span></div>
        <button class="primary-btn full" @click="syncMessage = '同步完成，共 1,284 条知识'">立即同步外部向量库</button><div v-if="syncMessage" class="success-line">{{ syncMessage }}</div>
      </section>

      <section class="knowledge-source local">
        <div class="knowledge-source-head"><div class="knowledge-source-icon">本</div><div><h2>本地知识库</h2><span>PostgreSQL + Chroma</span></div><span class="status-badge standby">本地托管</span></div>
        <p>文件信息保存在 PostgreSQL，文档切片和 Embedding 向量保存在 Chroma。</p>
        <div class="mini-stat-grid"><div class="mini-stat"><span>知识库</span><strong>{{ libraries.length }}</strong></div><div class="mini-stat"><span>文档总数</span><strong>{{ documentTotal }}</strong></div></div>
        <label class="model-library-picker"><span>当前配置的本地知识库</span><select v-model="selectedId" :disabled="!libraries.length" @change="loadModelConfig"><option v-for="item in libraries" :key="item.id" :value="item.id">{{ item.name }}</option><option v-if="!libraries.length" value="">请先创建知识库</option></select></label>
        <div class="model-switch-block"><div class="model-switch-title"><span>Embedding 模型</span><small>仅作用于本地知识库</small></div><div class="model-buttons"><button v-for="model in embeddingModels" :key="model" :class="{ active: embeddingModel === model }" @click="embeddingModel = model; saveModelConfig()">{{ model }}</button></div></div>
        <div class="model-switch-block"><div class="model-switch-title"><span>回答生成模型</span><small>仅作用于本地知识库 RAG</small></div><div class="model-buttons"><button v-for="model in answerModels" :key="model" :class="{ active: answerModel === model }" @click="answerModel = model; saveModelConfig()">{{ model }}</button></div></div>
        <div class="local-model-actions"><button class="ghost-btn" :disabled="modelBusy || !selectedId" @click="testModels">{{ modelBusy ? "真实调用中…" : "测试 Embedding + 回答模型" }}</button><button class="primary-btn" @click="createOpen = true">添加本地知识库</button></div>
        <div v-if="modelStatus" class="model-call-result" :class="{ success: modelTestResult }">{{ modelStatus }}</div>
        <div v-if="modelTestResult" class="model-test-grid"><div><span>Embedding</span><strong>{{ modelTestResult.embeddingModel }}</strong><small>{{ modelTestResult.embeddingDimensions }} 维向量</small></div><div><span>回答模型</span><strong>{{ modelTestResult.answerModel }}</strong><small>{{ modelTestResult.answer }}</small></div></div>
      </section>
    </div>

    <section class="local-rag-workspace">
      <div class="rag-workspace-head"><div><h2>本地知识库真实问答</h2><span>Embedding 检索 Chroma，回答模型根据命中切片生成答案</span></div><span class="api-state" :class="configured ? 'ready' : 'missing'">{{ configured ? "外部模型 API 已连接" : "未配置外部模型 API" }}</span></div>
      <div class="rag-input-row"><textarea v-model.trim="question" placeholder="输入一个只能通过已上传文档回答的问题"></textarea><button class="primary-btn" :disabled="ragBusy || !selectedId" @click="ask">{{ ragBusy ? "检索并生成中…" : "真实提问" }}</button></div>
      <div v-if="ragError" class="model-call-result error">{{ ragError }}</div>
      <div v-if="ragResult" class="rag-answer"><div class="rag-answer-meta"><strong>{{ ragResult.model }}</strong><span>会话 {{ ragResult.conversationId }}</span><span>Token {{ ragResult.usage?.total_tokens ?? ragResult.usage?.totalTokens ?? "-" }}</span></div><p>{{ ragResult.answer }}</p><details><summary>查看命中的 {{ ragResult.contexts?.length || 0 }} 个知识切片</summary><blockquote v-for="item in ragResult.contexts || []" :key="item">{{ item }}</blockquote></details></div>
    </section>

    <section class="knowledge-table-section">
      <div class="knowledge-table-toolbar"><div><h2>本地知识库</h2><span>共 {{ filtered.length }} 个知识库</span></div><div class="knowledge-actions"><div class="knowledge-search"><input v-model.trim="keyword" placeholder="搜索名称或描述"><button class="ghost-btn" @click="page = 1">搜索</button></div><button class="primary-btn" @click="createOpen = true">+ 添加知识库</button></div></div>
      <div class="table-wrap knowledge-table"><table><thead><tr><th>知识库名称</th><th>知识库描述</th><th>类型</th><th>上传文档</th><th>创建时间</th><th>操作</th></tr></thead><tbody>
        <tr v-for="library in pageItems" :key="library.id"><td><strong>{{ library.name }}</strong></td><td><span class="knowledge-description">{{ library.description }}</span></td><td><span class="knowledge-type" :class="library.knowledgeType">{{ library.knowledgeType === "image" ? "图片" : "文本" }}</span></td><td><label class="upload-btn">上传{{ library.knowledgeType === "image" ? "图片" : "文档" }}<input type="file" :accept="library.knowledgeType === 'image' ? 'image/*' : '.txt,.md,.pdf,.doc,.docx'" @change="upload(library.id, $event)"></label><small>{{ library.collectionCount }} 个文档</small></td><td>{{ library.createdAt }}</td><td><div class="row-actions"><button class="tiny-btn" @click="openDetail(library)">查看文档</button><button class="danger-btn" @click="removeLibrary(library)">删除</button></div></td></tr>
        <tr v-if="!pageItems.length"><td colspan="6"><div class="empty-state">暂无知识库</div></td></tr>
      </tbody></table></div>
      <div class="pagination"><button class="icon-btn" :disabled="page === 1" @click="page--">‹</button><button v-for="number in totalPages" :key="number" :class="{ active: number === page }" @click="page = number">{{ number }}</button><button class="icon-btn" :disabled="page === totalPages" @click="page++">›</button></div>
    </section>

    <div v-if="createOpen" class="modal-backdrop" @click.self="createOpen = false"><div class="modal knowledge-modal"><div class="modal-title-row"><div><h2>添加知识库</h2><span>创建后可上传文本或图片文档</span></div><button class="icon-btn" @click="createOpen = false">×</button></div><label class="field-label required">知识库名称</label><input v-model.trim="createForm.name" placeholder="请输入知识库名称"><label class="field-label required">知识库类型</label><select v-model="createForm.knowledgeType"><option value="text">文本</option><option value="image">图片</option></select><label class="field-label required">知识库描述</label><textarea v-model.trim="createForm.description" placeholder="请输入知识库描述"></textarea><div v-if="formError" class="form-error">{{ formError }}</div><div class="modal-actions"><button class="primary-btn" @click="createLibrary">确定添加</button><button class="ghost-btn" @click="createOpen = false">取消</button></div></div></div>

    <div v-if="detail" class="modal-backdrop" @click.self="detail = null"><div class="modal knowledge-modal"><div class="modal-title-row"><div><h2>{{ detail.name }}</h2><span>本地知识库详情</span></div><button class="icon-btn" @click="detail = null">×</button></div><div class="knowledge-detail-grid"><div><span>类型</span><strong>{{ detail.knowledgeType === "image" ? "图片" : "文本" }}</strong></div><div><span>文档数量</span><strong>{{ detail.collectionCount }}</strong></div><div><span>Embedding</span><strong>{{ detail.embeddingModel || "-" }}</strong></div><div><span>回答模型</span><strong>{{ detail.answerModel || "-" }}</strong></div></div><div class="knowledge-detail-description"><span>知识库描述</span><p>{{ detail.description }}</p></div><div class="collection-placeholder"><strong>已索引文档</strong><p v-if="detail.documents?.length"><template v-for="doc in detail.documents" :key="doc.id">{{ doc.filename }}（{{ doc.chunkCount }} 个切片）<br></template></p><p v-else>当前还没有上传文档。</p></div><button class="primary-btn full" @click="detail = null">关闭</button></div></div>
  </section>
</template>
<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import PageHeader from "../../../../components/PageHeader.vue";
import ProgressBar from "../../../../components/ProgressBar.vue";
import { knowledgeApi } from "./api/index.js";
const libraries = ref([]), selectedId = ref(""), embeddingModels = ref([]), answerModels = ref([]);
const embeddingModel = ref(""), answerModel = ref(""), configured = ref(false), modelBusy = ref(false), modelStatus = ref(""), modelTestResult = ref(null);
const keyword = ref(""), page = ref(1), createOpen = ref(false), detail = ref(null), formError = ref(""), syncMessage = ref("");
const question = ref(""), ragBusy = ref(false), ragError = ref(""), ragResult = ref(null);
const createForm = reactive({ name: "", knowledgeType: "text", description: "" });
const filtered = computed(() => { const key = keyword.value.toLowerCase(); return key ? libraries.value.filter((item) => item.name.toLowerCase().includes(key) || item.description.toLowerCase().includes(key)) : libraries.value; });
const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / 4)));
const pageItems = computed(() => filtered.value.slice((page.value - 1) * 4, page.value * 4));
const documentTotal = computed(() => libraries.value.reduce((sum, item) => sum + item.collectionCount, 0));
watch(totalPages, (value) => { if (page.value > value) page.value = value; });
async function loadLibraries() { try { const response = await knowledgeApi.listLibraries({ page_size: 100 }); libraries.value = response.data?.items || []; if (!libraries.value.some((item) => item.id === selectedId.value)) selectedId.value = libraries.value[0]?.id || ""; } catch (error) { modelStatus.value = error.message; } }
async function loadModelConfig() { try { const response = await knowledgeApi.getModelConfig(selectedId.value); const config = response.data; embeddingModels.value = config.embeddingModels || []; answerModels.value = config.answerModels || []; embeddingModel.value = config.embeddingModel; answerModel.value = config.answerModel; configured.value = config.configured; } catch (error) { modelStatus.value = error.message; } }
async function saveModelConfig() { if (!selectedId.value) return; try { await knowledgeApi.updateModelConfig({ knowledge_base_id: selectedId.value, embedding_model: embeddingModel.value, answer_model: answerModel.value }); modelStatus.value = "模型配置已保存到该知识库。"; } catch (error) { modelStatus.value = error.message; } }
async function testModels() { modelBusy.value = true; modelTestResult.value = null; try { const response = await knowledgeApi.testModels({ knowledge_base_id: selectedId.value, text: "请确认本地知识库模型连接正常" }); modelTestResult.value = response.data; modelStatus.value = "真实模型调用成功。"; } catch (error) { modelStatus.value = error.message; } finally { modelBusy.value = false; } }
async function ask() { if (!question.value) return; ragBusy.value = true; ragError.value = ""; try { const response = await knowledgeApi.query({ query: question.value, limit: 5, knowledge_base_id: selectedId.value }); ragResult.value = response.data; } catch (error) { ragError.value = error.message; } finally { ragBusy.value = false; } }
async function createLibrary() { if (!createForm.name || !createForm.description) { formError.value = "请完整填写知识库名称和描述。"; return; } try { const response = await knowledgeApi.createLibrary({ name: createForm.name, knowledge_type: createForm.knowledgeType, description: createForm.description }); libraries.value.unshift(response.data); selectedId.value = response.data.id; createOpen.value = false; Object.assign(createForm, { name: "", knowledgeType: "text", description: "" }); await loadModelConfig(); } catch (error) { formError.value = error.message; } }
async function openDetail(library) { detail.value = library; try { detail.value = (await knowledgeApi.getLibrary(library.id)).data; } catch {} }
async function removeLibrary(library) { if (!window.confirm(`确定删除知识库“${library.name}”吗？关联文档和向量数据也会被删除，此操作无法撤销。`)) return; try { await knowledgeApi.deleteLibrary(library.id); await loadLibraries(); await loadModelConfig(); } catch (error) { modelStatus.value = error.message; } }
async function upload(id, event) { const file = event.target.files?.[0]; if (!file) return; modelStatus.value = `正在处理 ${file.name}…`; try { await knowledgeApi.uploadCollection(id, file); modelStatus.value = `${file.name} 已完成切片和向量化。`; await loadLibraries(); } catch (error) { modelStatus.value = error.message; } event.target.value = ""; }
onMounted(async () => { await loadLibraries(); await loadModelConfig(); });
</script>
<style scoped></style>
