# wechat-avatar-wuxing 微信头像五行分析技能

基于原创《五行微信头像设计实操手册》的 WorkBuddy Agent Skill。启用后，Agent 可根据客户生辰八字排盘定五行命格与喜用神，对微信头像进行专业五行分析与调整建议，**并自动输出四象限五行落位示意图**。

## 功能

- 🔮 **八字排盘**：日主五行（子平正宗）+ 纳音年命（古法）双法并用，判断身旺身弱、喜用神
- 🧩 **头像五行拆解**：逐元素归属五行，含特殊判定规则（流动之物皆属水、取象优先等）
- 🧭 **四象限分析**：上朱雀火 / 下玄武水 / 左青龙木 / 右白虎金 / 中央土 + 太极点判断 + 五大方位吉格
- 🖼️ **自动配图**：每次分析自动生成「四象限五行落位示意图」（按元素布局重绘 + 方位吉凶标注），多张头像逐张配图并出汇总对比表
- 🏥 **健康分析**：五行过旺克伐疾患速查 + 五脏开窍对应
- 💰 **财位分析**：年命 / 日命 / 时命 / 八宅四维财位
- ⭐ **综合评分**：5 维度 × 5 分制（太极点 / 四象限平衡 / 用神补益 / 情感特质 / 健康暗示）
- 📄 **报告产出**：即时分析、多图对比选优、专业版 Word 报告、客户版温馨报告（Word / PDF）、换头像复评

## 安装

将本仓库克隆到 WorkBuddy 用户级技能目录：

```bash
git clone https://github.com/20091229F/wechat-avatar-wuxing.git ~/.workbuddy/skills/wechat-avatar-wuxing
```
或下载 zip 解压到 `~/.workbuddy/skills/wechat-avatar-wuxing/`，重启 WorkBuddy 会话即可。

## 使用示例

启用 skill 后，直接对 Agent 说：

- 「分析一下这个微信头像，女性，阳历 1984 年 11 月 17 日 20:45 出生」（附头像图片）
- 「这几张头像帮我对比选一个分数最高的」
- 「形成分析报告和给客户的简单报告」
- 「客户换了新头像，复评打分」

## 目录结构

```
wechat-avatar-wuxing/
├── SKILL.md                        # 主工作流（10 步分析流程）
├── references/
│   ├── manual.md                   # 实操手册完整内容
│   └── scoring-and-workflow.md     # 评分标准与分析深度等级
└── scripts/
    ├── template_pro_report.py      # 专业版 Word 报告模板
    ├── template_client_report.py   # 客户版温馨 Word 报告模板
    └── template_pdf_report.py      # 客户版 PDF 报告模板（reportlab）
```

## 依赖

- python-docx（Word 报告）
- reportlab + Pillow（PDF 报告）

## 免责声明

本技能基于传统阴阳五行与易学理论，仅供传统文化参考与日常指导，不构成医疗建议。健康问题请及时就医，以专业医疗诊断为准。

## License

MIT
