import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "scripts" / "shen_ppt_engine.py"

spec = importlib.util.spec_from_file_location("shen_ppt_engine", ENGINE)
engine = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["shen_ppt_engine"] = engine
spec.loader.exec_module(engine)


class ShenPptEngineTests(unittest.TestCase):
    def run_engine(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ENGINE), *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_engine_writes_valid_slide_cards_from_markdown(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            source = tmp_path / "paper-notes.md"
            source.write_text(
                "\n".join(
                    [
                        "# DRIFT",
                        "Risk-constrained diffusion with imitation priors.",
                        "The method generates mixed autonomy traffic scenes.",
                        "It combines diffusion generation, imitation priors, and risk constraints.",
                        "Experiments compare safety, realism, and diversity.",
                    ]
                ),
                encoding="utf-8",
            )
            out = tmp_path / "out"
            result = self.run_engine(
                "cards",
                "--source",
                str(source),
                "--title",
                "DRIFT论文中文讲解",
                "--output-dir",
                str(out),
                "--slides",
                "8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            cards_path = out / "DRIFT论文中文讲解_slide_cards.json"
            self.assertTrue(cards_path.exists())
            cards = json.loads(cards_path.read_text(encoding="utf-8"))
            self.assertEqual(cards["deckTitle"], "DRIFT论文中文讲解")
            self.assertEqual(len(cards["slides"]), 8)
            self.assertEqual(cards["slides"][0]["layoutFamily"], "cover")
            self.assertEqual(cards["slides"][1]["layoutFamily"], "directory")
            self.assertEqual(cards["slides"][-1]["layoutFamily"], "thanks")
            for slide in cards["slides"]:
                self.assertTrue(slide["purpose"])
                self.assertTrue(slide["claim"])
                self.assertTrue(slide["sourceEvidence"])
                self.assertEqual(slide["subtitle"], slide["subtitle"].replace("，", ""))
                self.assertNotIn("。", slide["subtitle"])

    def test_engine_writes_compact_script_and_qa_from_cards(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            tmp_path = Path(temp_dir)
            cards = {
                "deckTitle": "测试讲解",
                "theme": "论文讲解",
                "slides": [
                    {
                        "slideNo": 1,
                        "layoutFamily": "cover",
                        "section": "00",
                        "sectionTitle": "封面",
                        "title": "测试讲解",
                        "subtitle": "论文核心问题概览",
                        "purpose": "建立汇报主题",
                        "claim": "本文围绕风险约束生成展开",
                        "sourceEvidence": "source",
                        "body": ["介绍研究对象", "说明讲解路线"],
                        "visualAsset": "none",
                        "icon": "document",
                        "qaRisk": "none",
                    }
                ],
            }
            out = tmp_path / "out"
            out.mkdir()
            cards_path = out / "cards.json"
            cards_path.write_text(json.dumps(cards, ensure_ascii=False), encoding="utf-8")
            result = self.run_engine(
                "docs",
                "--cards",
                str(cards_path),
                "--output-dir",
                str(out),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            script = out / "测试讲解_讲稿.md"
            qa = out / "测试讲解_问答.md"
            self.assertTrue(script.exists())
            self.assertTrue(qa.exists())
            self.assertNotIn("\n\n\n", script.read_text(encoding="utf-8"))
            self.assertNotIn("\n\n\n", qa.read_text(encoding="utf-8"))
            self.assertIn("## 第01页", script.read_text(encoding="utf-8"))
            self.assertIn("## Q1", qa.read_text(encoding="utf-8"))

    def test_pdf_front_matter_is_removed_before_sentence_selection(self):
        raw = """
        IEEETRANSACTIONSONINTELLIGENTTRANSPORTATIONSYSTEMS 1
        DRIFT: Risk-Constrained Diffusion with Imitation
        Priors for Mixed-Autonomy Traffic Generation
        Yaoshen Yu, Minghui Liwang, Senior Member, IEEE, Wenbo Zhu, Xinlei Yi, Senior Member, IEEE
        Abstract〞Future intelligent transportation systems are envisioned to evolve toward a long-term mixed-autonomy paradigm.
        In this context, realistic microscopic behaviors are valuable only if they remain executable and induce plausible traffic evolution.
        """
        cleaned = engine.compact_text(raw)
        self.assertNotIn("IEEETRANSACTIONSONINTELLIGENTTRANSPORTATIONSYSTEMS", cleaned)
        self.assertNotIn("Yaoshen Yu", cleaned)
        self.assertNotIn("Senior Member", cleaned)
        self.assertNotIn("DRIFT: Risk-Constrained", cleaned)
        picked = engine.sentence_pick(cleaned, ["mixed-autonomy", "traffic"], "fallback", 180)
        self.assertIn("Future intelligent transportation systems", picked)
        self.assertNotIn("Yaoshen", picked)
        self.assertNotIn("IEEE", picked)

    def test_drift_cards_use_paper_specific_chinese_structure_without_front_matter(self):
        source = engine.SourceDoc(
            path=Path("DRIFT.pdf"),
            text=engine.compact_text(
                """
                IEEETRANSACTIONSONINTELLIGENTTRANSPORTATIONSYSTEMS 1
                DRIFT: Risk-Constrained Diffusion with Imitation Priors for Mixed-Autonomy Traffic Generation
                Yaoshen Yu, Minghui Liwang, Senior Member, IEEE
                Abstract—Future intelligent transportation systems are envisioned to evolve toward a long-term mixed-autonomy paradigm.
                In this context, it remains challenging to capture heterogeneous behavioral distribution shifts.
                III. KEY DEFINITIONS AND CORE MODELING Candidate and candidate set are generated over a planning window and executed over a short execution window.
                V. DESIGN OF DRIFT Module A learns a heterogeneous traffic representation. Module B generates candidate control sequences. Module C performs risk-aware distribution alignment.
                VI. EXPERIMENTS We evaluate DRIFT in closed-loop mixed-autonomy simulation, focusing on efficiency across AV penetration rates, safety under merging disturbances, and ablation contribution.
                VII. CONCLUSION Experiments show a competitive safety-efficiency-executability tradeoff.
                """
            ),
        )
        cards = engine.build_cards(source, "DRIFT论文中文讲解", 13)
        visible = json.dumps(cards["slides"], ensure_ascii=False)
        self.assertIn("建模分解", visible)
        self.assertIn("方法设计", visible)
        self.assertIn("闭环仿真", visible)
        self.assertNotIn("Yaoshen Yu", visible)
        self.assertNotIn("Senior Member", visible)
        self.assertNotIn("IEEETRANSACTIONSON", visible)
        self.assertNotIn("材料依据：To this end", visible)
        self.assertNotIn("nificantlycomplicate", visible)

    def test_slide_cards_require_real_visuals_captions_and_latex_slots_for_papers(self):
        source = engine.SourceDoc(
            path=Path("paper.pdf"),
            text=engine.compact_text(
                """
                Abstract—A paper about risk-constrained diffusion.
                Fig. 1. Illustration of temporal-window definitions in this work.
                Fig. 2. Overall workflow of DRIFT, separating offline training from online inference.
                Eq. (28) defines the closed-loop generation problem.
                VI. EXPERIMENTS We evaluate DRIFT in Flow/SUMO.
                Fig. 4. Closed-loop simulation protocol.
                """
            ),
            assets=[
                engine.SourceAsset("figure", "figure-01.png", "Fig. 1. Illustration of temporal-window definitions", 4),
                engine.SourceAsset("figure", "figure-02.png", "Fig. 2. Overall workflow of DRIFT", 8),
                engine.SourceAsset("figure", "figure-04.png", "Fig. 4. Closed-loop simulation protocol", 13),
            ],
        )
        cards = engine.build_cards(source, "论文讲解", 13)
        slides = cards["slides"]
        self.assertNotEqual(slides[0]["visualAsset"], "none")
        self.assertTrue(slides[0]["caption"])
        visual_slides = [s for s in slides if s["visualAsset"] != "none"]
        self.assertGreaterEqual(len(visual_slides), 3)
        self.assertTrue(all(s["caption"] for s in visual_slides))
        latex_slides = [s for s in slides if s.get("latex")]
        self.assertTrue(latex_slides)
        self.assertIn("P_0", latex_slides[0]["latex"][0]["source"])

    def test_project_folder_reading_collects_real_image_assets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("项目报告\n包含终端截图和实验结果图。", encoding="utf-8")
            image_path = root / "terminal-result.png"
            image_path.write_bytes(
                bytes.fromhex(
                    "89504E470D0A1A0A0000000D4948445200000001000000010802000000907753DE"
                    "0000000C4944415408D763F8FFFF3F0005FE02FEA7B5F81D0000000049454E44AE426082"
                )
            )
            doc = engine.read_source(root, root / "assets")
            self.assertIn("项目报告", doc.text)
            self.assertTrue(doc.assets)
            self.assertEqual(doc.assets[0].kind, "image")
            self.assertEqual(doc.assets[0].path, str(image_path))
            self.assertIn("terminal result", doc.assets[0].caption)

    def test_latex_cards_include_clean_display_text_for_renderer_fallback(self):
        source = engine.SourceDoc(
            path=Path("paper.pdf"),
            text="Eq. (28) defines the closed-loop generation problem.",
            assets=[
                engine.SourceAsset("figure", "figure-01.png", "Fig. 1", 1),
                engine.SourceAsset("figure", "figure-02.png", "Fig. 2", 2),
                engine.SourceAsset("figure", "figure-03.png", "Fig. 3", 3),
            ],
        )
        cards = engine.build_cards(source, "论文讲解", 13)
        latex_items = [item for slide in cards["slides"] for item in slide.get("latex", [])]
        self.assertTrue(latex_items)
        display = latex_items[0].get("display", "")
        self.assertTrue(display)
        self.assertNotIn("\\", display)
        self.assertNotIn("{", display)
        self.assertIn("P0", display)

    def test_paper_cards_include_multiple_formulas_and_experiment_table(self):
        source = engine.SourceDoc(
            path=Path("paper.pdf"),
            text=engine.compact_text(
                """
                Abstract—Risk-constrained diffusion for mixed autonomy traffic generation.
                The objective contains realism and long-tail risk penalties.
                The risk value is measured through collision risk, time headway, and time-to-collision.
                Experiments compare DRIFT against IDM, BC, GAIL, Social-GAN, Trajectron++, and diffusion baselines.
                Ring, Figure-eight, and Merge scenarios evaluate efficiency, safety, realism, and diversity.
                Ablation studies remove risk enhancement, imitation prior, and closed-loop selection.
                Fig. 1. Temporal window definition.
                Fig. 2. Overall workflow of DRIFT.
                Fig. 3. Experimental scenarios.
                """
            ),
            assets=[
                engine.SourceAsset("figure", "figure-01.png", "Fig. 1", 1),
                engine.SourceAsset("figure", "figure-02.png", "Fig. 2", 2),
                engine.SourceAsset("figure", "figure-03.png", "Fig. 3", 3),
            ],
        )
        cards = engine.build_cards(source, "论文讲解", 13)
        latex_items = [item for slide in cards["slides"] for item in slide.get("latex", [])]
        self.assertGreaterEqual(len(latex_items), 3)
        self.assertTrue(all(item.get("source") and item.get("display") for item in latex_items))
        table_slides = [slide for slide in cards["slides"] if slide.get("tables")]
        self.assertTrue(table_slides)
        table = table_slides[0]["tables"][0]
        self.assertEqual(table["kind"], "experiment-summary")
        self.assertIn("场景", table["headers"])
        self.assertIn("评价指标", table["headers"])
        self.assertGreaterEqual(len(table["rows"]), 4)
        visible = json.dumps(table, ensure_ascii=False)
        self.assertIn("Ring", visible)
        self.assertIn("Merge", visible)

if __name__ == "__main__":
    unittest.main()
