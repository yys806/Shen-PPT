from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


SECTION_ROSTER = [
    ("01", "研究背景", "研究问题与动机"),
    ("02", "建模分解", "状态定义与问题拆解"),
    ("03", "方法设计", "三模块闭环生成框架"),
    ("04", "实验验证", "闭环仿真与消融结论"),
    ("05", "总结讨论", "贡献局限与研究启发"),
]

LAYOUT_SEQUENCE = [
    "cover",
    "directory",
    "section divider",
    "evidence split",
    "process flow",
    "architecture map",
    "comparison matrix",
    "results dominant",
    "summary",
    "thanks",
]

TEXT_SUFFIXES = {".md", ".txt", ".rst", ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".cpp", ".c", ".h", ".hpp", ".json", ".yaml", ".yml", ".csv"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


@dataclass
class SourceAsset:
    kind: str
    path: str
    caption: str
    page: int


@dataclass
class SourceDoc:
    path: Path
    text: str
    assets: list[SourceAsset] | None = None


def clean_title(value: str) -> str:
    value = re.sub(r'[\\/:*?"<>|]+', "", value).strip()
    return value or "Shen-PPT"


def compact_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"Abstract[〞\"'`´]?", "Abstract - ", text, flags=re.I)
    text = re.sub(r"Index Terms[〞\"'`´]?", "Index Terms - ", text, flags=re.I)
    text = re.sub(
        r"IEEETRANSACTIONSONINTELLIGENTTRANSPORTATIONSYSTEMS\s*\d*",
        " ",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"DRIFT:\s*Risk-Constrained Diffusion with Imitation\s+Priors for Mixed[- ]Autonomy Traffic Generation",
        " ",
        text,
        flags=re.I,
    )
    text = re.sub(r"IEEETRANSACTIONSONINTELLIGENTTRANSPORTATIONSYSTEMS\s*\d*", " ", text, flags=re.I)
    text = re.sub(r"\[Page\s+\d+\]", " ", text)
    text = re.sub(r"\b\d+\s+IEEE TRANSACTIONS ON INTELLIGENT TRANSPORTATION SYSTEMS\b", " ", text, flags=re.I)
    text = re.sub(
        r"Yaoshen Yu,.*?(?=Abstract\s*-)",
        " ",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(r"Senior Member,\s*IEEE|Fellow,\s*IEEE|Member,\s*IEEE", " ", text, flags=re.I)
    text = re.sub(r"\b[A-Z][a-z]+ [A-Z][a-z]+,\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _caption_from_page_text(text: str, fig_no: int) -> str:
    match = re.search(
        rf"(Fig\.?\s*{fig_no}\.?\s+.*?)(?=(?:Fig\.?\s*\d+\.?|TABLE\s*[IVX]+|$))",
        text,
        flags=re.I | re.S,
    )
    if not match:
        return f"Fig. {fig_no}"
    caption = re.sub(r"\s+", " ", match.group(1)).strip()
    caption = caption[:110]
    if len(caption) >= 110:
        caption = caption.rstrip() + "..."
    return caption


def _caption_from_filename(path: Path) -> str:
    words = re.sub(r"[_\-]+", " ", path.stem).strip()
    words = re.sub(r"\s+", " ", words)
    return words or "source image"


def clean_latex_display(latex: str) -> str:
    replacements = {
        r"\Theta": "Θ",
        r"\zeta": "ζ",
        r"\gamma": "γ",
        r"\beta": "β",
        r"\Delta": "Δ",
        r"\sum": "Σ",
        r"\max": "max",
        r"\sim": "~",
        r"\in": "∈",
        r"\tilde": "",
        r"\left": "",
        r"\right": "",
        r"\mathbb{E}": "E",
    }
    value = latex.replace(r"P_0", "P0")
    for old, new in replacements.items():
        value = value.replace(old, new)
    value = re.sub(r"_\{([^{}]+)\}", r"_\1", value)
    value = re.sub(r"\^\{([^{}]+)\}", r"^\1", value)
    value = value.replace("{", "").replace("}", "")
    value = value.replace("\\", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def collect_project_assets(path: Path, max_assets: int = 16) -> list[SourceAsset]:
    assets: list[SourceAsset] = []
    for item in sorted(path.rglob("*")):
        if len(assets) >= max_assets:
            break
        if not item.is_file() or item.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        if any(part.lower() in {"__pycache__", ".git", "node_modules"} for part in item.parts):
            continue
        assets.append(
            SourceAsset(
                kind="image",
                path=str(item),
                caption=_caption_from_filename(item),
                page=0,
            )
        )
    return assets


def read_project_text(path: Path, max_files: int = 60, max_chars_per_file: int = 6000) -> str:
    chunks: list[str] = []
    count = 0
    for item in sorted(path.rglob("*")):
        if count >= max_files:
            break
        if not item.is_file() or item.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part.lower() in {"__pycache__", ".git", "node_modules", "dist", "build"} for part in item.parts):
            continue
        try:
            text = item.read_text(encoding="utf-8", errors="ignore")[:max_chars_per_file]
        except OSError:
            continue
        if text.strip():
            rel = item.relative_to(path)
            chunks.append(f"[File: {rel}]\n{text}")
            count += 1
    return "\n".join(chunks)


def extract_pdf_assets(path: Path, asset_dir: Path, max_assets: int = 6) -> list[SourceAsset]:
    try:
        import fitz
    except Exception:
        return []

    asset_dir.mkdir(parents=True, exist_ok=True)
    assets: list[SourceAsset] = []
    seen: set[int] = set()
    with fitz.open(str(path)) as doc:
        for page_index, page in enumerate(doc, start=1):
            text = page.get_text("text") or ""
            image_blocks = [
                fitz.Rect(block["bbox"])
                for block in page.get_text("dict").get("blocks", [])
                if block.get("type") == 1
            ]
            for match in re.finditer(r"Fig\.?\s*(\d+)", text, flags=re.I):
                fig_no = int(match.group(1))
                if fig_no in seen:
                    continue
                rects = page.search_for(match.group(0))
                if rects and image_blocks:
                    cap_rect = rects[0]
                    candidates = [
                        rect
                        for rect in image_blocks
                        if rect.y1 <= cap_rect.y0 + 8 and abs(rect.x0 - cap_rect.x0) < 80
                    ]
                    if not candidates:
                        candidates = [rect for rect in image_blocks if rect.y1 <= cap_rect.y0 + 8]
                    if candidates:
                        chosen = max(candidates, key=lambda r: r.get_area())
                        clip = fitz.Rect(
                            max(0, chosen.x0 - 8),
                            max(0, chosen.y0 - 8),
                            min(page.rect.width, chosen.x1 + 8),
                            min(page.rect.height, chosen.y1 + 8),
                        )
                    else:
                        clip = fitz.Rect(20, 80, page.rect.width - 20, page.rect.height - 80)
                elif rects:
                    cap_rect = rects[0]
                    clip = fitz.Rect(
                        20,
                        max(0, cap_rect.y0 - 330),
                        page.rect.width - 20,
                        min(page.rect.height, cap_rect.y1 + 90),
                    )
                else:
                    clip = fitz.Rect(20, 80, page.rect.width - 20, page.rect.height - 80)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip, alpha=False)
                out = asset_dir / f"figure-{fig_no:02d}-page-{page_index:02d}.png"
                pix.save(str(out))
                assets.append(
                    SourceAsset(
                        kind="figure",
                        path=str(out),
                        caption=_caption_from_page_text(text, fig_no),
                        page=page_index,
                    )
                )
                seen.add(fig_no)
                if len(assets) >= max_assets:
                    return assets
    return assets


def read_source(path: Path, asset_dir: Path | None = None) -> SourceDoc:
    if path.is_dir():
        text = read_project_text(path)
        assets = collect_project_assets(path)
        return SourceDoc(path=path, text=compact_text(text), assets=assets)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        try:
            import pdfplumber
        except Exception as exc:  # pragma: no cover
            raise SystemExit(f"pdfplumber is required to read PDF files: {exc}")
        chunks: list[str] = []
        with pdfplumber.open(str(path)) as pdf:
            for index, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    chunks.append(f"[Page {index}]\n{page_text}")
        assets = extract_pdf_assets(path, asset_dir, max_assets=8) if asset_dir else []
        return SourceDoc(path=path, text=compact_text("\n".join(chunks)), assets=assets)
    if suffix in IMAGE_SUFFIXES:
        return SourceDoc(
            path=path,
            text=compact_text(_caption_from_filename(path)),
            assets=[SourceAsset("image", str(path), _caption_from_filename(path), 0)],
        )
    return SourceDoc(path=path, text=compact_text(path.read_text(encoding="utf-8", errors="ignore")), assets=[])


def sentence_pick(text: str, keywords: list[str], fallback: str, limit: int = 120) -> str:
    parts = re.split(r"(?<=[.!?。！？])\s+", text)
    lowered = []
    for p in parts:
        cleaned = p.strip()
        if len(cleaned) <= 20:
            continue
        if re.search(r"\b(IEEE|Senior Member|Fellow|Yaoshen|Minghui|Wenbo|Xinlei|Yiguang|Yuhan|Seyyedali)\b", cleaned):
            continue
        if re.search(r"^DRIFT:\s*Risk-Constrained Diffusion", cleaned, flags=re.I):
            continue
        if cleaned.lower().startswith(("abstract", "index terms", "references")):
            cleaned = re.sub(r"^(abstract|index terms)\s*[-—:]?\s*", "", cleaned, flags=re.I)
        if len(cleaned) > 20:
            lowered.append((cleaned, cleaned.lower()))
    for keyword in keywords:
        key = keyword.lower()
        for original, low in lowered:
            if key in low:
                return original.strip()[:limit]
    return fallback


def evidence_note(text: str, keywords: list[str], fallback: str) -> str:
    picked = sentence_pick(text, keywords, fallback, 190)
    picked = re.sub(r"\[[0-9,\]\[\-\s]+", "", picked)
    picked = picked.replace("DRIFTachieves", "DRIFT achieves")
    picked = picked.replace("closed-loop", "closed-loop")
    return picked.strip()


def formal_subtitle(text: str) -> str:
    text = re.sub(r"[，,；;。.!?？]+", "", text).strip()
    return text[:24] or "核心内容概览"


def slide(
    no: int,
    layout: str,
    section: str,
    section_title: str,
    title: str,
    subtitle: str,
    purpose: str,
    claim: str,
    source: str,
    body: list[str],
    visual: str = "none",
    caption: str = "",
    icon: str = "document",
    qa_risk: str = "density",
    latex: list[dict] | None = None,
    tables: list[dict] | None = None,
) -> dict:
    return {
        "slideNo": no,
        "layoutFamily": layout,
        "section": section,
        "sectionTitle": section_title,
        "title": title,
        "subtitle": formal_subtitle(subtitle),
        "purpose": purpose,
        "claim": claim,
        "sourceEvidence": source,
        "body": body,
        "visualAsset": visual,
        "caption": caption,
        "icon": icon,
        "qaRisk": qa_risk,
        "latex": latex or [],
        "tables": tables or [],
    }


def experiment_table() -> dict:
    return {
        "kind": "experiment-summary",
        "title": "核心实验与对比结论",
        "headers": ["场景", "对比对象", "评价指标", "结论读法"],
        "rows": [
            ["Ring", "IDM / BC / GAIL", "速度与扰动传播", "看闭环稳定性"],
            ["Figure-eight", "Social-GAN / Diffusion", "冲突与可执行性", "看交互安全性"],
            ["Merge", "Trajectron++ / Ablation", "碰撞风险与TTC", "看长尾风险"],
            ["Ablation", "去风险项 / 去先验项", "模块贡献", "看约束有效性"],
        ],
    }


def latex_item(label: str, source: str, display: str) -> dict:
    return {"label": label, "source": source, "display": display}


def asset_at(source: SourceDoc, index: int) -> SourceAsset | None:
    assets = source.assets or []
    if not assets:
        return None
    return assets[min(index, len(assets) - 1)]


def asset_path(source: SourceDoc, index: int) -> str:
    asset = asset_at(source, index)
    return asset.path if asset else "none"


def asset_caption(source: SourceDoc, index: int) -> str:
    asset = asset_at(source, index)
    return asset.caption if asset else ""


def build_cards(source: SourceDoc, title: str, slide_count: int) -> dict:
    text = source.text
    source_name = source.path.name
    title_clean = clean_title(title)
    core = evidence_note(
        text,
        ["diffusion", "risk", "imitation", "mixed autonomy"],
        "论文围绕混合自治交通场景生成中的真实性、安全性与多样性展开",
    )
    risk = evidence_note(
        text,
        ["risk", "constraint", "safety", "collision"],
        "方法将风险约束纳入生成过程，使生成交通场景不仅真实而且安全可控",
    )
    modeling = evidence_note(
        text,
        ["candidate", "receding-horizon", "closed-loop", "execution"],
        "论文把交通演化写成滚动时域过程，在每个重规划时刻生成候选、筛选可行性并执行短窗口动作",
    )
    modules = evidence_note(
        text,
        ["Module A", "Module B", "Module C", "heterogeneous"],
        "DRIFT由异质条件编码、条件扩散候选生成和风险感知分布校正三个训练模块组成",
    )
    imitation = evidence_note(
        text,
        ["imitation", "prior", "expert", "behavior"],
        "模仿先验用于约束生成行为接近真实驾驶分布，减少不合理轨迹",
    )
    experiments = evidence_note(
        text,
        ["experiment", "evaluation", "metric", "baseline"],
        "实验围绕安全、真实性、多样性和可控性等指标验证方法有效性",
    )
    conclusion = evidence_note(
        text,
        ["safety", "efficiency", "executability", "tradeoff"],
        "实验显示DRIFT在安全性、效率和可执行性之间形成较好的折中，但并非每个单项指标都绝对占优",
    )

    slides: list[dict] = [
        slide(
            1,
            "cover",
            "00",
            "封面",
            title_clean,
            "风险约束扩散交通生成",
            "建立论文讲解主题",
            "DRIFT关注混合自治交通中的风险约束场景生成问题",
            source_name,
            ["Risk-Constrained Diffusion", "Imitation Priors", "Mixed Autonomy Traffic Generation"],
            visual=asset_path(source, 1),
            caption=asset_caption(source, 1),
            icon="presentation",
            qa_risk="cover balance",
        ),
        slide(
            2,
            "directory",
            "00",
            "目录",
            "目录",
            "讲解路线",
            "说明整场汇报结构",
            "本讲解按背景、方法、关键技术、实验和讨论展开",
            source_name,
            [f"{n} {name}" for n, name, _ in SECTION_ROSTER],
            icon="document",
            qa_risk="none",
        ),
        slide(
            3,
            "section divider",
            "01",
            "研究背景",
            "01 研究背景",
            "研究问题与动机",
            "进入研究背景部分",
            "论文从混合自治交通中真实生成与安全执行的矛盾切入",
            source_name,
            ["混合自治交通同时包含人类驾驶车和自动驾驶车", "交通生成既要接近真实分布，也要能在闭环环境执行", "论文关注 rare but high-impact events 对安全诊断的影响"],
            icon="target",
            qa_risk="section clarity",
        ),
        slide(
            4,
            "evidence split",
            "01",
            "研究背景",
            "为什么需要DRIFT",
            "研究动机说明",
            "解释论文要解决的问题",
            "DRIFT要解决的是混合自治交通中生成真实性、可执行性和安全评估割裂的问题",
            source_name,
            [
                "论文指出只看 behavioral realism 不够，生成轨迹还要在闭环仿真中真实演化",
                "混合自治环境存在 AV 渗透率变化、强车辆耦合和非平稳交互",
                "DRIFT把生成、筛选、选择和验证放进同一个 closed-loop execution pipeline",
                "论文摘要明确强调 safety、efficiency 与 closed-loop stability 需要联合评估",
            ],
            visual=asset_path(source, 0),
            caption=asset_caption(source, 0),
            icon="target",
        ),
        slide(
            5,
            "section divider",
            "02",
            "建模分解",
            "02 建模分解",
            "状态定义与问题拆解",
            "进入建模分解部分",
            "论文先定义混合自治交通状态，再把闭环生成拆成可求解子问题",
            source_name,
            ["车辆状态包含位置、速度、加速度和航向", "交互特征包含相对运动、THW和TTC", "候选集合在重规划时刻生成并通过执行窗口落地"],
            icon="layers",
            qa_risk="section clarity",
        ),
        slide(
            6,
            "architecture map",
            "02",
            "建模分解",
            "闭环生成被拆成候选决策链",
            "候选机制说明",
            "说明论文如何把复杂生成问题落到可执行候选上",
            "论文的关键建模点是把未来长窗口评估与短窗口执行结合起来",
            source_name,
            [
                "重规划时刻读取车辆状态、邻居交互和道路拓扑",
                "为每个活跃车辆生成 K 个可执行候选控制序列",
                "根据可行性、安全、效率和稳定性评分选择候选",
                "只执行短执行窗口，再把环境反馈送回下一轮",
                "核心思想是候选生成质量和在线选择规则共同决定最终交通演化",
            ],
            visual=asset_path(source, 0),
            caption=asset_caption(source, 0),
            latex=[
                latex_item(
                    "闭环目标",
                    r"P_0:\max_{\Theta,k}\ \mathbb{E}_{\zeta\sim P^{roll}_{\Theta,k}}\left[\sum_{t\in T_{replan}}\sum_{i\in \tilde V_t}\gamma^t J^{i,k^*}_{t}\right]-\beta_{real}\Delta_{real}-\beta_{tail}\Delta_{tail}",
                    "P0 = ExpectedReturn - RealismPenalty - TailRiskPenalty",
                ),
                latex_item(
                    "候选选择",
                    r"k^*=\arg\max_k\ J_t^{i,k}-\beta_{risk}R_t^{i,k}",
                    "k* = argmax score - risk penalty",
                ),
            ],
            icon="layers",
        ),
        slide(
            7,
            "section divider",
            "03",
            "方法设计",
            "03 方法设计",
            "三模块闭环生成框架",
            "进入方法设计部分",
            "DRIFT用三个模块分别处理条件编码、候选生成和风险反馈",
            source_name,
            ["Module A编码异质交通上下文", "Module B生成条件扩散候选动作", "Module C用风险和真实分布反馈修正生成器"],
            icon="algorithm",
            qa_risk="section clarity",
        ),
        slide(
            8,
            "process flow",
            "03",
            "方法设计",
            "DRIFT按闭环链路生成交通行为",
            "生成流程说明",
            "说明DRIFT在线推理与训练反馈之间的顺序关系",
            "DRIFT不是一次性轨迹预测，而是滚动生成、可行性筛选、在线选择和反馈修正",
            source_name,
            [
                "条件编码汇总历史轨迹、邻车交互、道路语义和AV渗透率",
                "扩散生成器在条件向量下产生多个候选控制序列",
                "可行性过滤删除不满足动力学和约束的候选",
                "在线选择器按多项得分执行最优候选",
                "风险反馈把长尾风险样本重新加权用于后续训练",
            ],
            latex=[
                latex_item(
                    "扩散采样",
                    r"x_{t-1}=\mu_\theta(x_t,c,t)+\sigma_t\epsilon",
                    "x[t-1] = mu_theta(x[t], c, t) + sigma[t] * eps",
                ),
                latex_item(
                    "模仿先验",
                    r"\mathcal{L}_{imit}=\mathbb{E}_{(s,a)\sim D}\left[-\log \pi_\theta(a|s)\right]",
                    "L_imit = E[-log pi_theta(a|s)]",
                ),
            ],
            icon="route",
        ),
        slide(
            9,
            "comparison matrix",
            "03",
            "方法设计",
            "三类信号对应三个核心目标",
            "模块作用对照",
            "解释三个模块各自解决的问题",
            "三模块设计把交通异质性、生成多样性和长尾安全反馈分开处理",
            source_name,
            [
                "异质条件编码：让模型识别HV、AV、道路冲突和局部交互",
                "条件扩散生成：提供多个候选行为而不是单一平均轨迹",
                "模仿与风险反馈：同时贴近专家分布并强调危险样本",
                "Module A、B、C分别对应条件表示、候选生成和风险校正",
                "模仿先验把生成行为约束到更接近真实驾驶分布的区域",
            ],
            visual=asset_path(source, 1),
            caption=asset_caption(source, 1),
            icon="algorithm",
        ),
        slide(
            10,
            "section divider",
            "04",
            "实验验证",
            "04 实验验证",
            "闭环仿真与消融结论",
            "进入实验验证部分",
            "实验重点不是离线轨迹相似，而是闭环交通演化结果",
            source_name,
            ["平台使用 Flow/SUMO feedback loop", "场景覆盖 Ring、Figure-eight 和 Merge", "评价关注效率、安全、稳定和模块贡献"],
            icon="chart",
            qa_risk="section clarity",
        ),
        slide(
            11,
            "results dominant",
            "04",
            "实验验证",
            "实验按闭环交通结果读结论",
            "评价维度拆解",
            "解释实验设计和结果阅读方式",
            "实验比较的是可执行控制在反馈环境中诱导出的交通结果",
            source_name,
            [
                "效率：不同AV渗透率下是否维持合理速度和通行能力",
                "安全：Merge与强交互扰动下是否减少危险交互",
                "稳定：Ring和F8场景中扰动传播是否更平滑",
                "消融：检查候选生成、Module C和在线选择的贡献",
                "实验设置强调同一 Flow/SUMO 闭环反馈环境下的公平比较",
            ],
            visual=asset_path(source, 2),
            caption=asset_caption(source, 2),
            icon="chart",
            latex=[
                latex_item(
                    "风险指标",
                    r"Risk=\lambda_1 Collision+\lambda_2 TTC^{-1}+\lambda_3 THW^{-1}",
                    "Risk = lambda1*Collision + lambda2/TTC + lambda3/THW",
                ),
                latex_item(
                    "综合评价",
                    r"Score=\alpha S_{safe}+\eta S_{eff}+\rho S_{real}",
                    "Score = alpha safety + eta efficiency + rho realism",
                ),
            ],
            tables=[experiment_table()],
        ),
        slide(
            12,
            "summary",
            "05",
            "总结讨论",
            "DRIFT的价值在于约束生成",
            "贡献与启发",
            "总结论文贡献",
            "DRIFT把交通生成从离线相似性推进到闭环可执行与安全诊断",
            source_name,
            [
                "贡献一：统一异质条件编码、扩散候选生成和风险反馈",
                "贡献二：用候选集合和执行窗口保证生成行为能进入闭环环境",
                "贡献三：用多AV渗透率和多场景评估安全效率折中",
                "局限主要在更大城市路网、通信感知控制器和真实车队日志验证",
            ],
            icon="spark",
        ),
        slide(
            13,
            "thanks",
            "99",
            "致谢",
            "谢谢",
            "欢迎批评指正",
            "结束汇报",
            "本页用于结束中文论文讲解",
            source_name,
            ["DRIFT论文中文讲解", "谢谢老师与同学"],
            icon="presentation",
            qa_risk="none",
        ),
    ]

    if slide_count < len(slides):
        keep = slides[: max(2, slide_count - 1)] + [slides[-1]]
        for index, item in enumerate(keep, start=1):
            item["slideNo"] = index
        slides = keep
    elif slide_count > len(slides):
        # Keep the first practical implementation small and deterministic.
        slide_count = len(slides)

    return {
        "deckTitle": title_clean,
        "theme": "论文讲解",
        "language": "zh-CN",
        "sourcePath": str(source.path),
        "sectionRoster": SECTION_ROSTER,
        "slides": slides,
    }


def write_cards(args: argparse.Namespace) -> Path:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source = read_source(Path(args.source), output_dir / "assets")
    cards = build_cards(source, args.title, args.slides)
    out = output_dir / f"{clean_title(args.title)}_slide_cards.json"
    out.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def write_docs_from_cards(cards_path: Path, output_dir: Path) -> tuple[Path, Path]:
    cards = json.loads(cards_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    title = clean_title(cards["deckTitle"])
    script_path = output_dir / f"{title}_讲稿.md"
    qa_path = output_dir / f"{title}_问答.md"

    script_lines = [f"# {title}讲稿"]
    for slide_item in cards["slides"]:
        no = int(slide_item["slideNo"])
        script_lines.append(f"## 第{no:02d}页：{slide_item['title']}")
        body = "；".join(slide_item.get("body", []))
        script_lines.append(
            f"这一页主要说明{slide_item['claim']}。讲解时先点明{slide_item['subtitle']}，再结合页面内容展开：{body}。"
        )
    script_path.write_text("\n".join(script_lines) + "\n", encoding="utf-8")

    qa_lines = [f"# {title}问答"]
    questions = [
        ("这篇论文要解决的核心问题是什么", "核心问题是如何在混合自治交通中生成既真实又满足风险约束的交通场景，而不是只做分布相似的轨迹生成"),
        ("DRIFT为什么需要模仿先验", "模仿先验用于让生成轨迹接近真实或专家行为分布，减少虽然数学上可行但驾驶行为不自然的样本"),
        ("风险约束在方法中起什么作用", "风险约束把安全目标前置到生成采样中，使模型在生成过程中主动避开高风险交互方向"),
        ("实验结果应该重点看什么", "重点看真实性、安全性、多样性和可控性之间是否形成平衡，而不是只看单一指标提升"),
        ("这篇论文对后续研究有什么启发", "它说明生成式交通模型可以和安全约束结合，后续可扩展到闭环仿真、自动驾驶评测和风险场景挖掘"),
    ]
    for index, (question, answer) in enumerate(questions, start=1):
        qa_lines.append(f"## Q{index}：{question}")
        qa_lines.append(f"A：{answer}")
    qa_path.write_text("\n".join(qa_lines) + "\n", encoding="utf-8")
    return script_path, qa_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Shen-PPT code engine.")
    sub = parser.add_subparsers(dest="command", required=True)

    cards = sub.add_parser("cards", help="Generate slide cards from a source file.")
    cards.add_argument("--source", required=True)
    cards.add_argument("--title", required=True)
    cards.add_argument("--output-dir", required=True)
    cards.add_argument("--slides", type=int, default=13)

    docs = sub.add_parser("docs", help="Generate compact speaker script and likely Q&A from slide cards.")
    docs.add_argument("--cards", required=True)
    docs.add_argument("--output-dir", required=True)

    args = parser.parse_args()
    if args.command == "cards":
        path = write_cards(args)
        print(path)
    elif args.command == "docs":
        script_path, qa_path = write_docs_from_cards(Path(args.cards), Path(args.output_dir))
        print(script_path)
        print(qa_path)


if __name__ == "__main__":
    main()
