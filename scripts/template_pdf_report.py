#!/usr/bin/env python3
"""客户版微信头像评估报告 - PDF温馨简明版
用reportlab直接生成PDF，含头像分析 + 多版对比 + 最终推荐
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage

# ============================================================
# 字体注册
# ============================================================
try:
    pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
    FONT_CN = 'STSong-Light'
except:
    try:
        pdfmetrics.registerFont(TTFont('PingFang', '/System/Library/Fonts/PingFang.ttc', subfontIndex=0))
        FONT_CN = 'PingFang'
    except:
        FONT_CN = 'Helvetica'

FONT_BOLD = FONT_CN  # CID字体本身支持bold

# ============================================================
# 颜色定义
# ============================================================
C_PRIMARY = HexColor('#8B4513')   # 深棕
C_ACCENT  = HexColor('#C0392B')   # 红
C_SOFT    = HexColor('#D4A576')   # 暖金
C_TEXT    = HexColor('#3E3E3E')   # 正文灰
C_LIGHT   = HexColor('#7A6A5A')   # 浅灰
C_GREEN   = HexColor('#4A7C59')   # 绿
C_BLUE    = HexColor('#336699')   # 蓝
C_WHITE   = white

BG_SOFT   = HexColor('#FAF3E8')
BG_WARM   = HexColor('#FFF5EE')
BG_GREEN  = HexColor('#F0F7F4')
BG_GOLD   = HexColor('#FDF6E3')
BG_BLUE   = HexColor('#E8F0F8')
BG_RED    = HexColor('#FDE8E6')

# ============================================================
# CONFIG — 生成前修改此处
# ============================================================
NAME       = "客户姓名"          # 客户称呼（用于封面、图注、祝福语）
IMG_NEW    = ""                  # 当前/推荐头像路径（如 "/path/to/avatar.jpg"）
IMG_WARM   = ""                  # 备选方案一图片路径（可留空）
IMG_COOL   = ""                  # 备选方案二图片路径（可留空）
OUT_PATH   = os.path.expanduser(f"~/Desktop/微信头像调整/{NAME}-客户版报告.pdf")

# ============================================================
# 样式定义
# ============================================================
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'CTitle', parent=styles['Title'],
    fontName=FONT_CN, fontSize=22, leading=30,
    textColor=C_PRIMARY, alignment=TA_CENTER,
    spaceAfter=10
)

style_subtitle = ParagraphStyle(
    'CSubtitle', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=12, leading=18,
    textColor=C_LIGHT, alignment=TA_CENTER,
    spaceAfter=16
)

style_h1 = ParagraphStyle(
    'CH1', parent=styles['Heading1'],
    fontName=FONT_CN, fontSize=16, leading=24,
    textColor=C_PRIMARY, alignment=TA_LEFT,
    spaceBefore=16, spaceAfter=10
)

style_h2 = ParagraphStyle(
    'CH2', parent=styles['Heading2'],
    fontName=FONT_CN, fontSize=13, leading=20,
    textColor=C_ACCENT, alignment=TA_LEFT,
    spaceBefore=10, spaceAfter=6
)

style_body = ParagraphStyle(
    'CBody', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=10.5, leading=18,
    textColor=C_TEXT, alignment=TA_JUSTIFY,
    firstLineIndent=20, spaceAfter=6
)

style_body_center = ParagraphStyle(
    'CBodyC', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=10.5, leading=18,
    textColor=C_TEXT, alignment=TA_CENTER,
    spaceAfter=6
)

style_bullet = ParagraphStyle(
    'CBullet', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=10, leading=17,
    textColor=C_TEXT, alignment=TA_LEFT,
    leftIndent=30, spaceAfter=4
)

style_small = ParagraphStyle(
    'CSmall', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=9, leading=14,
    textColor=C_LIGHT, alignment=TA_CENTER,
    spaceAfter=4
)

style_blessing = ParagraphStyle(
    'CBlessing', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=11, leading=20,
    textColor=C_PRIMARY, alignment=TA_CENTER,
    spaceBefore=6, spaceAfter=6
)

style_blessing_bold = ParagraphStyle(
    'CBlessingB', parent=styles['Normal'],
    fontName=FONT_CN, fontSize=13, leading=22,
    textColor=C_ACCENT, alignment=TA_CENTER,
    spaceBefore=8, spaceAfter=8
)

# ============================================================
# 辅助函数
# ============================================================

def get_img_size(path, max_width=280):
    """获取图片按比例缩放后的尺寸"""
    try:
        img = PILImage.open(path)
        w, h = img.size
        ratio = h / w
        return max_width, int(max_width * ratio)
    except:
        return max_width, 200

def add_image(path, max_width=280, caption=None):
    """添加居中图片及可选图注"""
    flowables = []
    if os.path.exists(path):
        w, h = get_img_size(path, max_width)
        img = Image(path, width=w, height=h)
        img.hAlign = 'CENTER'
        flowables.append(img)
        if caption:
            flowables.append(Spacer(1, 4))
            flowables.append(Paragraph(caption, style_small))
    else:
        flowables.append(Paragraph(f'[图片未找到: {path}]', style_small))
    flowables.append(Spacer(1, 10))
    return flowables

def make_card(title, items, bg_color=BG_SOFT, border_color=C_SOFT):
    """创建卡片式表格"""
    data = [[Paragraph(f'<b>{title}</b>', ParagraphStyle(
        'CardTitle', fontName=FONT_CN, fontSize=12, leading=18,
        textColor=C_PRIMARY, alignment=TA_LEFT
    ))]]
    for item in items:
        data.append([Paragraph(item, ParagraphStyle(
            'CardItem', fontName=FONT_CN, fontSize=10, leading=16,
            textColor=C_TEXT, alignment=TA_LEFT,
            leftIndent=10
        ))])
    
    tbl = Table(data, colWidths=[15*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg_color),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, border_color),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return tbl

def make_score_table(score_data):
    """创建评分表"""
    header = ['维度', '得分', '说明']
    data = [header] + score_data
    tbl = Table(data, colWidths=[5*cm, 3*cm, 7*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_GOLD),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_PRIMARY),
        ('FONTNAME', (0, 0), (-1, -1), FONT_CN),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('FONTNAME', (0, 0), (-1, 0), FONT_CN),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_SOFT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_SOFT]),
    ]))
    return tbl

def make_compare_table():
    """创建两版花卉对比表"""
    header = ['对比项', '暖橙红版（图1）', '白紫绿版（图2）']
    rows = [
        ['主导花色', '橙红、黄色、暖色', '白色、紫蓝、绿色'],
        ['五行调性', '火、土主导', '金、水、木主导'],
        ['用神契合度', '极高', '偏弱'],
        ['情感传递', '温暖、喜庆、桃花旺', '清雅、文艺、稍冷'],
        ['健康友好', '暖色入脾胃', '白紫偏寒'],
        ['长期使用', '适合所有场景', '偏春夏季'],
        ['综合评分', '9.4/10', '7.2/10'],
    ]
    data = [header] + rows
    tbl = Table(data, colWidths=[4*cm, 5.5*cm, 5.5*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_GOLD),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_PRIMARY),
        ('FONTNAME', (0, 0), (-1, -1), FONT_CN),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_SOFT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BG_WARM, white]),
        ('BACKGROUND', (0, -1), (-1, -1), BG_GOLD),
        ('FONTNAME', (0, -1), (-1, -1), FONT_CN),
    ]))
    return tbl


# ============================================================
# 构建PDF内容
# ============================================================

def build_pdf():
    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=A4,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=2.8*cm,
        rightMargin=2.8*cm,
        title=f'{NAME}-微信头像分析报告',
        author='微信头像五行分析'
    )

    story = []

    # ============================================================
    # 封面
    # ============================================================
    story.append(Spacer(1, 60))
    story.append(Paragraph('微信头像专属分析报告', style_title))
    story.append(Paragraph(f'——  {NAME}  ——', style_subtitle))
    story.append(Spacer(1, 20))
    story.append(Paragraph('每一张头像，都在悄悄影响着您的人缘与运势。', 
                          ParagraphStyle('SubI', fontName=FONT_CN, fontSize=11, leading=18,
                                         textColor=C_LIGHT, alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph('愿这份报告，帮您找到最适合自己的那一张。', 
                          ParagraphStyle('SubI2', fontName=FONT_CN, fontSize=11, leading=18,
                                         textColor=C_LIGHT, alignment=TA_CENTER, spaceAfter=16)))
    story.append(Spacer(1, 10))
    story.append(Paragraph('&#10024;  &#10024;  &#10024;', 
                          ParagraphStyle('Star', fontName=FONT_CN, fontSize=14,
                                         textColor=C_SOFT, alignment=TA_CENTER)))
    story.append(Spacer(1, 30))
    
    # 新头像展示在封面
    story.extend(add_image(IMG_NEW, max_width=220, caption=f'{NAME} 微信头像'))
    
    story.append(Spacer(1, 20))
    story.append(Paragraph('专属定制', style_small))
    story.append(Paragraph('报告日期：2026年8月8日', style_small))

    story.append(PageBreak())

    # ============================================================
    # 一、关于您
    # ============================================================
    story.append(Paragraph('一、关于您', style_h1))
    story.append(Paragraph(
        '您属于「戊土」日主——戊土是厚重的城墙之土，代表稳重、信义、包容、踏实。'
        '您天生是一个值得信赖的人，给人的感觉是可靠、有担当。',
        style_body))
    story.append(Paragraph(
        '您生于冬季亥月，八字中水旺木旺，就像一片被大雪覆盖的土地——'
        '虽然底蕴深厚，但太冷太湿，需要「火」来温暖、「土」来帮身。'
        '一旦有了足够的阳光和温暖，您的才华和福气就会充分展现。',
        style_body))

    story.append(make_card('您的五行特质', [
        '<b>日主</b>：戊土（城墙之土）—— 稳重、信义、包容',
        '<b>需要</b>：火（温暖、活力、贵人）+ 土（帮身、固财、稳根基）',
        '<b>注意</b>：避免水太多（水多土荡、财来财去）、避免金太多（金泄土气）',
        '<b>旺桃花方向</b>：温暖、端庄、有生活气息、让人想靠近'
    ], bg_color=BG_GOLD, border_color=C_SOFT))
    story.append(Spacer(1, 10))

    # ============================================================
    # 二、旧头像回顾
    # ============================================================
    story.append(Paragraph('二、旧头像回顾', style_h1))
    story.append(Paragraph(
        '在之前的分析中，您旧头像评分为 <b>4/10</b>，主要存在以下问题：',
        style_body))

    story.append(make_card('旧头像七大问题', [
        '<b>问题1</b>：水太旺——黑色衣服+深色背景，水元素占近一半，财来财去',
        '<b>问题2</b>：火太弱——仅有一抹红唇，远不足以暖局',
        '<b>问题3</b>：背景封闭压抑——深色书架、奖杯包围，气场封闭',
        '<b>问题4</b>：吊带背心不利正缘——随意感容易招烂桃花',
        '<b>问题5</b>：多人头像大忌——背景多个人物照片，能量分散',
        '<b>问题6</b>：金泄土气——银色奖杯消耗而非助力',
        '<b>问题7</b>：情感偏冷——黑色冷调疏离，缺少女性温柔'
    ], bg_color=BG_WARM, border_color=C_ACCENT))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '核心原则：<b>身弱戊土，要的是「暖、亮、开阔」，不是「冷、暗、封闭」。</b>',
        style_body))

    story.append(PageBreak())

    # ============================================================
    # 三、新头像分析
    # ============================================================
    story.append(Paragraph('三、新头像分析', style_h1))
    story.append(Paragraph(
        '您更换后的新头像，是一张在绿植花园中手持花篮的人物照。'
        '画面明亮、自然、温柔——从五行角度看，<b>这是一次质的飞跃。</b>',
        style_body))

    story.extend(add_image(IMG_NEW, max_width=300, caption=f'{NAME} 头像'))

    story.append(Paragraph('新头像五行拆解', style_h2))
    story.append(make_card('五行占比', [
        '<b>木（50%）</b>：大量绿植背景 + 花篮绿叶——旺，但有火泄',
        '<b>土（18%）</b>：米白连衣裙 + 藤编花篮——吉，帮身固本',
        '<b>金（12%）</b>：白色花 + 米白裙——中性，提亮不抢',
        '<b>火（10%）</b>：暖肤色 + 黄色花朵——吉，暖局调候',
        '<b>水（10%）</b>：少量蓝紫花 + 黑发——小忌，但面积可控'
    ], bg_color=BG_GREEN, border_color=C_GREEN))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<b>核心流通链：木 \u2192 火 \u2192 土</b>，三用神俱全，水被压制。'
        '与旧头像（水占50%、火极弱）形成鲜明对比。',
        style_body))

    # 四象限分析
    story.append(Paragraph('四象限分析', style_h2))
    quad_data = [
        ['方位', '呈现', '判断'],
        ['上方（朱雀/火）', '绿叶顶端', '木生火可解，中性'],
        ['下方（玄武/水）', '白裙+草地+藤篮', '大吉，水气被压制'],
        ['左方（青龙/木）', '茂密绿植', '吉，事业位得木气'],
        ['右方（白虎/金）', '绿植+白花', '中吉，气场平衡'],
        ['中央（太极/土）', '人物+花篮居中', '大吉，太极点清晰'],
    ]
    tbl = Table(quad_data, colWidths=[4*cm, 5*cm, 6*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_GOLD),
        ('FONTNAME', (0, 0), (-1, -1), FONT_CN),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_SOFT),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, BG_SOFT]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 10))

    # 综合评分
    story.append(Paragraph('综合评分', style_h2))
    score_data = [
        ['太极点清晰度', '5/5', '人物居中、单人、花篮在怀'],
        ['四象限五行平衡', '4/5', '木极旺但有火土金平衡'],
        ['用神补益度', '4/5', '火暖局、土帮身（旧1/5）'],
        ['情感与人物特质', '5/5', '温柔、亲和、端庄贤淑'],
        ['健康暗示', '4/5', '户外绿植+暖肤色'],
        ['总分', '22/25', '约 8.8/10（旧4/10）'],
    ]
    story.append(make_score_table(score_data))

    story.append(Spacer(1, 10))
    story.append(Paragraph(
        '从旧头像的 <b>4/10</b> 跃升到 <b>8.8/10</b>，提升一倍以上——'
        '旧头像的七大问题在新头像中被逐一修正。',
        style_body))

    story.append(PageBreak())

    # ============================================================
    # 四、花卉调整两版对比
    # ============================================================
    story.append(Paragraph('四、花卉调整两版对比', style_h1))
    story.append(Paragraph(
        '在新头像基础上，对花篮中的花卉配色做了两版调整方案。以下逐一分析：',
        style_body))

    # 图1暖橙红版
    story.append(Paragraph('方案一：暖橙红花卉版', style_h2))
    story.extend(add_image(IMG_WARM, max_width=280, caption='暖橙红花卉版'))

    story.append(make_card('五行分析', [
        '<b>火（30%）</b>：橙红玫瑰、康乃馨——大吉，桃花之火',
        '<b>木（30%）</b>：绿叶背景——适度，生火之源',
        '<b>土（20%）</b>：黄花、米白裙、藤篮——吉，帮身固财',
        '<b>金（15%）</b>：白色小雏菊——中性，提亮',
        '<b>水（5%）</b>：极少——大吉，忌神被压制',
        '<b>流通链</b>：木 \u2192 火 \u2192 土，三用神俱全'
    ], bg_color=BG_WARM, border_color=C_ACCENT))

    story.append(Spacer(1, 6))
    story.append(make_card('优势', [
        '火土双补，完美契合戊土用神',
        '暖色花朵为「桃花之火」，最利正缘桃花',
        '暖色入脾胃，对消化、宫寒有改善',
        '喜庆而不俗气，工作、社交、节日皆宜'
    ], bg_color=BG_GOLD, border_color=C_SOFT))

    story.append(Spacer(1, 6))
    score_warm = [
        ['太极点清晰度', '5/5', '人物居中，单人主体'],
        ['四象限平衡', '4.5/5', '木火土协调'],
        ['用神补益度', '5/5', '火土双补'],
        ['情感与人物特质', '5/5', '温暖贤淑、桃花最旺'],
        ['健康暗示', '4/5', '暖色入脾胃'],
        ['总分', '23.5/25', '约 9.4/10'],
    ]
    story.append(make_score_table(score_warm))

    story.append(PageBreak())

    # 图2白紫绿版
    story.append(Paragraph('方案二：白紫绿花卉版', style_h2))
    story.extend(add_image(IMG_COOL, max_width=280, caption='白紫绿花卉版'))

    story.append(make_card('五行分析', [
        '<b>木（35%）</b>：绿叶、绣球——旺但火不足',
        '<b>金（20%）</b>：白花、米白裙——中性偏多',
        '<b>水（15%）</b>：紫蓝鸢尾——小忌，水气回升',
        '<b>土（15%）</b>：藤篮、少量黄花——偏弱',
        '<b>火（15%）</b>：暖肤色——不足，缺调候',
        '<b>问题</b>：缺火土，水气回升，金多耗火'
    ], bg_color=BG_BLUE, border_color=C_BLUE))

    story.append(Spacer(1, 6))
    story.append(make_card('不足之处', [
        '紫蓝色鸢尾多——水气上升，与戊土忌水相悖',
        '缺少橙红黄花——调候火力不足，桃花磁场弱',
        '绿色偏冷调——木多火塞之象',
        '白色多——金泄土气，对身弱不利'
    ], bg_color=BG_RED, border_color=C_ACCENT))

    story.append(Spacer(1, 6))
    score_cool = [
        ['太极点清晰度', '5/5', '人物居中'],
        ['四象限平衡', '3.5/5', '白虎位见水'],
        ['用神补益度', '2.5/5', '缺火土、水气回升'],
        ['情感与人物特质', '4/5', '清雅但偏冷'],
        ['健康暗示', '3/5', '水气回升不利脾胃'],
        ['总分', '18/25', '约 7.2/10'],
    ]
    story.append(make_score_table(score_cool))

    story.append(PageBreak())

    # 对比总表
    story.append(Paragraph('两版花卉对比总览', style_h2))
    story.append(make_compare_table())
    story.append(Spacer(1, 12))

    # ============================================================
    # 五、最终推荐
    # ============================================================
    story.append(Paragraph('五、最终推荐', style_h1))
    story.append(Paragraph(
        '<b>强烈推荐采用暖橙红花卉版作为最终头像。</b>',
        style_body))
    story.append(Paragraph('推荐理由：', style_h2))

    story.append(make_card('五大推荐理由', [
        '<b>1. 火土双补</b>：橙红玫瑰、黄花完美契合戊土日主喜火土用神',
        '<b>2. 桃花最旺</b>：暖色花束在风水上是「桃花之火」，对正缘最有利',
        '<b>3. 健康友好</b>：暖色入心脾，对脾胃虚寒、宫寒、湿气重有改善',
        '<b>4. 百搭场合</b>：喜庆而不俗气，工作、社交、节日皆宜',
        '<b>5. 能量流通</b>：绿叶（木）生橙红花（火），火暖米白裙（土），五行流通无阻'
    ], bg_color=BG_GOLD, border_color=C_SOFT))

    story.append(Spacer(1, 8))
    story.append(Paragraph('微调建议（精益求精）', style_h2))
    story.append(make_card('可微调之处', [
        '在花束中再加1-2朵向日葵（黄+棕），强化土气',
        '点缀一枝金黄色麦穗（火土+财气），可达满分10/10',
        '避免大面积蓝紫色花',
        '可加一抹暖阳透光，从绿叶缝隙洒下'
    ], bg_color=BG_GREEN, border_color=C_GREEN))

    # ============================================================
    # 六、用色建议
    # ============================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph('六、用色建议', style_h1))

    story.append(make_card('宜用色', [
        '<b>橙红、珊瑚红、暖红</b>——补火暖身，增加活力，最旺桃花',
        '<b>暖黄、卡其、米棕、土黄</b>——补土固财，最利根基',
        '<b>米白、奶油白</b>——补金但不过量，提亮画面',
        '<b>暖绿色（适量）</b>——绿叶生火，适度使用'
    ], bg_color=BG_SOFT, border_color=C_SOFT))

    story.append(Spacer(1, 8))
    story.append(make_card('忌用色', [
        '<b>大面积纯黑、深蓝</b>——水太旺，根基不稳、财来财去',
        '<b>大面积深紫、蓝紫</b>——水气回升，不利脾胃和妇科',
        '<b>大面积冷灰色调</b>——缺少温暖，不利人际关系',
        '<b>银色、金属冷感</b>——金泄土气，消耗而非助力'
    ], bg_color=BG_WARM, border_color=C_ACCENT))

    story.append(PageBreak())

    # ============================================================
    # 七、健康小贴士
    # ============================================================
    story.append(Paragraph('七、健康小贴士', style_h1))
    story.append(Paragraph(
        '您的五行水木偏旺，平时可以多注意以下几个方面：',
        style_body))

    story.append(make_card('需重点关注的身体部位', [
        '<b>脾胃</b>——木旺容易克土，注意消化不良、胃胀、食欲问题',
        '<b>心脏和小肠</b>——水旺容易克火，注意心悸、手脚冰凉、睡眠',
        '<b>肾脏和泌尿</b>——水虽多但寒水不养肾，注意腰膝酸软',
        '<b>眼睛</b>——肝开窍于目，木旺需注意眼睛干涩、视疲劳'
    ], bg_color=BG_GOLD, border_color=C_SOFT))

    story.append(Spacer(1, 8))
    story.append(Paragraph('日常调养小建议：', style_h2))
    story.append(Paragraph('\u2022 多吃黄色食物健脾胃：小米、南瓜、山药、红薯', style_bullet))
    story.append(Paragraph('\u2022 适量吃红色食物养心：红枣、枸杞、红豆、番茄', style_bullet))
    story.append(Paragraph('\u2022 多晒太阳，补充阳气，改善水寒体质', style_bullet))
    story.append(Paragraph('\u2022 少食生冷，注意腹部保暖', style_bullet))
    story.append(Paragraph('\u2022 早睡早起，避免熬夜伤心阳', style_bullet))
    story.append(Paragraph('\u2022 用眼40分钟后远眺休息，养护肝目', style_bullet))
    story.append(Paragraph('\u2022 多做舒缓运动，如瑜伽、太极、快走', style_bullet))
    story.append(Paragraph('\u2022 培养书法、园艺、冥想等静心习惯', style_bullet))

    story.append(PageBreak())

    # ============================================================
    # 八、新旧头像对比总结
    # ============================================================
    story.append(Paragraph('八、新旧头像对比总结', style_h1))

    compare_data = [
        ['对比项', '旧头像', '新头像（暖橙红版）'],
        ['水占比', '50%（极旺）', '5%（被压制）'],
        ['火占比', '极弱（仅红唇）', '30%（暖橙红花）'],
        ['土占比', '弱（无暖色）', '20%（黄花+米白裙）'],
        ['太极点', '多人头像', '单人居中'],
        ['服装', '吊带背心', '有袖蕾丝裙'],
        ['情感传递', '冷感疏离', '温柔贤淑'],
        ['桃花磁场', '招烂桃花', '旺正缘桃花'],
        ['评分', '4/10', '9.4/10'],
    ]
    tbl = Table(compare_data, colWidths=[4*cm, 5.5*cm, 5.5*cm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), BG_GOLD),
        ('FONTNAME', (0, 0), (-1, -1), FONT_CN),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, C_SOFT),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BG_WARM, white]),
        ('BACKGROUND', (0, -1), (-1, -1), BG_GOLD),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 16))

    # ============================================================
    # 九、温馨祝福
    # ============================================================
    story.append(Paragraph('温馨祝福', style_h1))

    story.append(Paragraph(f'亲爱的{NAME}，', style_blessing))
    story.append(Paragraph(
        '感谢您让我为您的头像把关。',
        style_body_center))
    story.append(Paragraph(
        '从旧头像的黑色冷调，到新头像的暖橙红花园——'
        '这不只是换了一张照片，更是为自己选了一个温暖的方向。',
        style_body_center))
    story.append(Paragraph(
        '您换掉的不只是「水多土荡」的旧气场，'
        '更是迎来了「木生火、火暖土」的新能量。',
        style_body_center))
    story.append(Paragraph(
        '当您手持暖橙红花束，笑容温柔地面对镜头时，'
        '您向世界传递的信号是：<br/>'
        '「我温柔而有力量，我扎根大地，我值得信赖，我也能留住福气。」',
        style_body_center))
    story.append(Paragraph(
        '愿您如戊土般厚重有福，亦如暖阳般温柔有光。<br/>'
        '事业顺遂，财源稳固，正缘到来，身心康泰，喜乐常伴。',
        style_body_center))

    story.append(Spacer(1, 16))
    story.append(Paragraph('愿您万事顺遂，福慧双修', style_blessing_bold))

    story.append(Spacer(1, 30))
    story.append(Paragraph('报告日期：2026年8月8日', style_small))
    story.append(Paragraph('——  本报告为您专属定制，请妥善保管  ——', style_small))
    story.append(Paragraph('专属定制', style_small))

    # ============================================================
    # 构建PDF
    # ============================================================
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    doc.build(story)
    print(f"PDF报告已生成：{OUT_PATH}")

if __name__ == '__main__':
    build_pdf()
