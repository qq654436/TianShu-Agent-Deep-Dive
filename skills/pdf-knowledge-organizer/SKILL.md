# SKILL.md - PDF 知识库整理

**技能名称**: `pdf-knowledge-organizer`  
**版本**: 1.0.0  
**作者**: 天枢计划 (TianShu)  
**许可证**: MIT

---

## 📋 技能描述

自动整理本地 PDF 文档，提取关键信息，建立索引，支持语义搜索。适用于论文、报告、技术文档等知识库管理场景。

**触发条件**: 当用户需要整理、搜索、分析 PDF 文档时自动激活。

---

## 🎯 何时使用 (When to Use)

- ✅ 批量整理本地 PDF 文档
- ✅ 从 PDF 提取关键信息 (标题/作者/摘要)
- ✅ 建立 PDF 知识库索引
- ✅ 语义搜索 PDF 内容
- ✅ 生成 PDF 阅读报告/摘要

---

## ⚙️ 配置要求

### 环境变量
```bash
# 可选：配置向量数据库用于语义搜索
export VECTOR_DB_PATH="/home/admin/.openclaw/workspace/knowledge/vector_db"

# 可选：配置 LLM API 用于摘要生成
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxx"
```

### 依赖安装
```bash
pip install PyPDF2 pdfplumber chromadb
```

---

## 📦 安装方式

### 方式 1: ClawHub
```bash
clawhub install pdf-knowledge-organizer
```

### 方式 2: 手动安装
```bash
git clone https://github.com/qq654436/TianShu-Agent-Deep-Dive.git
cd TianShu-Agent-Deep-Dive/tian_shu/skills/pdf-knowledge-organizer
pip install -r requirements.txt
cp -r . ~/.openclaw/skills/pdf-knowledge-organizer/
```

---

## 🚀 使用示例

### 示例 1: 整理单个 PDF
```python
# 在对话中
帮我整理一下这个 PDF：/home/admin/Documents/ai_paper.pdf
```

**响应**:
```
📄 PDF 信息已提取

**标题**: Attention Is All You Need
**作者**: Vaswani et al.
**年份**: 2017
**页数**: 15
**大小**: 1.2MB

**摘要**:
We propose the Transformer, a new network architecture based entirely on attention mechanisms...

**关键词**: Transformer, Attention, NLP, Deep Learning

📁 已归档至：`knowledge/papers/2017_vaswani_transformer.pdf`
🔖 索引已更新
```

### 示例 2: 批量整理文件夹
```python
整理 /home/admin/Documents/papers/ 目录下所有 PDF
```

**响应**:
```
📚 批量整理完成

**扫描目录**: /home/admin/Documents/papers/
**发现 PDF**: 23 个
**成功处理**: 21 个
**失败**: 2 个 (加密/损坏)

**分类统计**:
- AI/ML: 12 篇
- System: 5 篇
- Other: 4 篇

📁 已归档至：`knowledge/papers/`
🔖 索引已更新：`knowledge/index.json`
```

### 示例 3: 搜索 PDF 内容
```python
搜索关于 Transformer 架构的论文
```

**响应**:
```
🔍 搜索结果："Transformer 架构"

| 标题 | 相似度 | 年份 | 引用 |
|------|--------|------|------|
| Attention Is All You Need | 95% | 2017 | 75k+ |
| Transformer-XL | 87% | 2019 | 5k+ |
| BERT | 82% | 2018 | 50k+ |

💡 点击标题查看摘要或全文
```

### 示例 4: 生成阅读报告
```python
给这篇 PDF 生成阅读报告：ai_paper.pdf
```

**响应**:
```
📝 阅读报告已生成

# AI Paper 阅读报告

## 核心贡献
1. 提出 Transformer 架构
2. 证明自注意力机制有效性
3. 刷新多项 SOTA

## 关键方法
- Multi-Head Attention
- Positional Encoding
- Layer Normalization

## 实验结果
- WMT 14 En-De: 28.4 BLEU
- WMT 14 En-Fr: 41.8 BLEU

## 个人笔记
[用户可在此添加笔记]

📁 报告保存：`knowledge/reports/ai_paper_report.md`
```

---

## 🔧 技能实现

### 核心函数
```python
def organize_pdf(pdf_path: str, output_dir: str = None) -> dict:
    """
    整理单个 PDF 文档
    
    Args:
        pdf_path: PDF 文件路径
        output_dir: 输出目录
    
    Returns:
        dict: {title, author, year, pages, summary, keywords}
    """
    import pdfplumber
    
    with pdfplumber.open(pdf_path) as pdf:
        # 提取元数据
        metadata = pdf.metadata or {}
        
        # 提取第一页内容用于摘要
        first_page = pdf.pages[0].extract_text()
        
        # 生成摘要 (调用 LLM)
        summary = generate_summary(first_page)
        
        # 提取关键词
        keywords = extract_keywords(first_page)
        
        return {
            "title": metadata.get("Title", "Unknown"),
            "author": metadata.get("Author", "Unknown"),
            "year": extract_year(metadata),
            "pages": len(pdf.pages),
            "summary": summary,
            "keywords": keywords
        }
```

### 向量索引
```python
def build_vector_index(documents: list) -> ChromaDB:
    """
    构建向量索引用于语义搜索
    """
    from chromadb import PersistentClient
    
    client = PersistentClient(path=VECTOR_DB_PATH)
    collection = client.get_or_create_collection("pdf_knowledge")
    
    for doc in documents:
        collection.add(
            documents=[doc["content"]],
            metadatas=[{"title": doc["title"]}],
            ids=[doc["id"]]
        )
    
    return collection
```

### 工具依赖
| 工具 | 用途 |
|------|------|
| `pdf` | PDF 文档分析 |
| `read`/`write` | 文件操作 |
| `exec` | 依赖安装/命令执行 |

---

## 📝 输出格式

### 单文档响应
```
📄 PDF 信息已提取

**标题**: {title}
**作者**: {author}
**年份**: {year}
**页数**: {pages}

**摘要**: {summary}

**关键词**: {keywords}
```

### 批量响应
```
📚 批量整理完成

**扫描目录**: {dir}
**发现 PDF**: {count} 个
**成功处理**: {success} 个

**分类统计**:
- {category}: {count} 篇
```

---

## ⚠️ 注意事项

1. **加密 PDF**: 不支持密码保护的 PDF
2. **扫描版 PDF**: OCR 功能需额外配置
3. **大文件**: >100MB 文件处理较慢
4. **中文支持**: 需安装中文字体

---

## 🆚 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-19 | 初始版本，基础整理功能 |
| 1.1.0 | 2026-03-26 | 语义搜索 (计划) |
| 1.2.0 | 2026-04-02 | OCR 支持 (计划) |

---

## 📞 支持

- **GitHub**: [TianShu-Agent-Deep-Dive](https://github.com/qq654436/TianShu-Agent-Deep-Dive)
- **问题反馈**: 创建 Issue
- **企业支持**: 查看 [premium/](../premium/) 企业级配置包

---

## 🔗 相关技能

- `feishu-auto-doc` - 飞书文档自动发布
- `crypto-price-tracker` - 加密货币行情追踪

---

## 💰 企业级功能 (Premium)

| 功能 | Free | Pro | Enterprise |
|------|------|-----|------------|
| 单文档整理 | ✅ | ✅ | ✅ |
| 批量整理 (≤10) | ✅ | ✅ | ✅ |
| 批量整理 (∞) | ❌ | ✅ | ✅ |
| 语义搜索 | ❌ | ✅ | ✅ |
| OCR 支持 | ❌ | ❌ | ✅ |
| 私有部署 | ❌ | ❌ | ✅ |

**价格**: Pro ¥99/月 | Enterprise ¥9999/年

---

**🗡️ 利刃行动技能包** | 天枢计划 © 2026
