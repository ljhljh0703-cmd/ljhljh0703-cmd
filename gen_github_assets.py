#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════
# gen_github_assets.py — GitHub 프로필용 애니메이티드 SVG 생성기
# 소스: ../resume-data.yml (SSOT) — 수치·stage·jobLink·링크 전부 여기서.
# 산출: assets/banner-{light,dark}.svg + card-<slug>-{light,dark}.svg ×5
# 원리: GitHub README는 <style>·JS를 제거하지만, <img>로 임베드된 SVG "내부"의
#       CSS 애니메이션은 살아서 돈다. 이력서 시그니처 모션 문법(장면 7.2s·질감 2.4s·
#       transform/opacity/dashoffset만·정직 모티프)을 그대로 이식.
# 재생성: python3 gen_github_assets.py  (수치 바뀌면 resume-data.yml 수정 후 재실행)
# ═══════════════════════════════════════════════════════════════════
import re, sys, pathlib, xml.etree.ElementTree as ET
try:
    import yaml
except ImportError:
    sys.exit("PyYAML 필요: pip3 install pyyaml --break-system-packages")

HERE = pathlib.Path(__file__).parent
DATA = yaml.safe_load(open(HERE.parent / 'resume-data.yml', encoding='utf-8'))
OUT = HERE / 'assets'; OUT.mkdir(exist_ok=True)
P = {p['slug']: p for p in DATA['pieces']}

FONT = "'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Segoe UI',sans-serif"
MONO = "'SF Mono','JetBrains Mono',Consolas,monospace"

# 테마 토큰 (GitHub 라이트 #fff / 다크 #0d1117 배경 위 카드)
T = {
 'light': dict(bg='#ffffff', card='#ffffff', ink='#1f2328', muted='#656d76', rule='#d0d7de',
               warn='#b91c1c', ok='#15803d', gem='#1d4ed8', cla='#c2410c', accent='#7a1f2d'),
 'dark':  dict(bg='#0d1117', card='#161b22', ink='#e6edf3', muted='#8b949e', rule='#30363d',
               warn='#f87171', ok='#4ade80', gem='#60a5fa', cla='#fb923c', accent='#e0707f'),
}
# 카드별 시그니처 hue (이력서 팔레트와 동일)
HUE = {
 'bookmon':     dict(light='#0f766e', dark='#2dd4bf'),
 'starlink':    dict(light='#1d4ed8', dark='#60a5fa'),
 'medical-rag': dict(light='#15803d', dark='#4ade80'),
 'rocket-sim':  dict(light='#6d28d9', dark='#a78bfa'),
 'hyunsoo-bot': dict(light='#b45309', dark='#fbbf24'),
 'penelope':    dict(light='#4338ca', dark='#818cf8'),
}

# ── 시그니처 그래픽 (이력서 Resume_LeeJuHyeong.html의 sig SVG 이식 — 48² 무대)
# {c}=시그니처색 {warn}=차단·하락 {ok}=통과·상승 {accent}=브랜드
SIG_BODY = {
'bookmon': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <line x1="7" y1="8" x2="7" y2="40" opacity=".35"/>
  <rect x="11" y="9" width="26" height="4.5" rx="1"/><circle class="sb-dot" cx="41.5" cy="11.2" r="1.6" fill="{c}" stroke="none"/>
  <rect class="sb-b" x="11" y="17" width="21" height="4.5" rx="1" opacity=".8"/>
  <rect class="sb-c" x="11" y="25" width="16" height="4.5" rx="1" opacity=".55"/>
  <rect class="sb-bad" x="11" y="33" width="12" height="4.5" rx="1" opacity=".3" stroke="{warn}"/>
</g>''',
'starlink': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <path class="ss-in" pathLength="24" d="M3 24 C5 17,7 17,9 24 S13 32,15 24 S19 15,21 24" opacity=".85"/>
  <rect class="ss-node" x="22" y="20.5" width="7" height="7" rx="1" transform="rotate(45 25.5 24)" stroke="{accent}"/>
  <path class="ss-out" pathLength="24" d="M31 24 C32.5 20,34 20,35.5 24 S38.5 28,40 24 S43 20,44.5 24" opacity=".85"/>
  <circle class="ss-ear" cx="45.5" cy="24" r="1.7" fill="{c}" stroke="none"/>
</g>''',
'medical-rag': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <rect x="4" y="6" width="10" height="12" rx="1"/><line x1="6.5" y1="10" x2="11.5" y2="10" opacity=".5"/><line x1="6.5" y1="13" x2="10" y2="13" opacity=".5"/>
  <rect class="sm-doc3" x="4" y="18" width="10" height="12" rx="1" opacity=".5" stroke="{warn}"/>
  <rect x="4" y="30" width="10" height="12" rx="1" opacity=".85"/><line x1="6.5" y1="34" x2="11.5" y2="34" opacity=".5"/><line x1="6.5" y1="37" x2="10" y2="37" opacity=".5"/>
  <path class="sm-c1" pathLength="1" d="M14 12 C22 12,24 20,30 22"/>
  <path class="sm-c2" pathLength="1" d="M14 36 C22 36,24 28,30 26"/>
  <path class="sm-c3" pathLength="1" d="M14 24 L22 24" opacity=".7"/>
  <line class="sm-gate" x1="24" y1="19" x2="24" y2="29" opacity=".7" stroke="{warn}"/>
  <path class="sm-x" pathLength="1" d="M19.6 22.6 L22.4 25.4 M22.4 22.6 L19.6 25.4" stroke-width="1.3" stroke="{warn}"/>
  <rect x="30" y="16" width="14" height="16" rx="1"/>
  <line class="sm-a1" pathLength="1" x1="33" y1="21" x2="41" y2="21"/>
  <line class="sm-a2" pathLength="1" x1="33" y1="25" x2="39" y2="25"/>
  <path class="sm-chk" pathLength="1" d="M33 29.5 l2.2 2.2 l4.2 -4.2" stroke="{ok}"/>
</g>''',
'rocket-sim': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <circle cx="24" cy="8" r="2" fill="{c}" stroke="none"/>
  <circle cx="37.3" cy="14.4" r="2" fill="{c}" stroke="none" opacity=".8"/>
  <circle class="sr-sus" cx="40.6" cy="28.8" r="2.3" fill="{warn}" stroke="none"/>
  <circle cx="31.4" cy="40.3" r="2" fill="{c}" stroke="none" opacity=".8"/>
  <circle cx="16.6" cy="40.3" r="2" fill="{c}" stroke="none" opacity=".8"/>
  <circle cx="7.4" cy="28.8" r="2" fill="{c}" stroke="none" opacity=".8"/>
  <circle cx="10.7" cy="14.4" r="2" fill="{c}" stroke="none" opacity=".8"/>
  <line class="sr-e1" pathLength="1" x1="24" y1="8" x2="31.4" y2="40.3" opacity=".6"/>
  <line class="sr-e2" pathLength="1" x1="10.7" y1="14.4" x2="40.6" y2="28.8" opacity=".6"/>
  <line class="sr-e3" pathLength="1" x1="7.4" y1="28.8" x2="37.3" y2="14.4" opacity=".6"/>
  <line class="sr-e4" pathLength="1" x1="16.6" y1="40.3" x2="40.6" y2="28.8" opacity=".6"/>
  <line class="sr-e5" pathLength="1" x1="24" y1="8" x2="40.6" y2="28.8" opacity=".6"/>
  <circle class="sr-ring" cx="40.6" cy="28.8" r="4" opacity="0" stroke="{warn}"/>
</g>''',
'hyunsoo-bot': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <rect x="4" y="19" width="10" height="10" rx="1"/>
  <circle class="sh-dot" cx="9" cy="24" r="1.7" fill="{c}" stroke="none"/>
  <line x1="14" y1="24" x2="22" y2="24" opacity=".7"/>
  <line class="sh-g1" x1="24" y1="18" x2="24" y2="30"/>
  <line class="sh-g2" x1="27" y1="18" x2="27" y2="30"/>
  <circle class="sh-hitl" cx="25.5" cy="12.5" r="2" opacity=".6" stroke="{ok}"/><path d="M25.5 14.5 v2.5" opacity=".6" stroke="{ok}"/>
  <line x1="29" y1="24" x2="35" y2="24" stroke-dasharray="2.5 2.5" opacity=".8"/>
  <g class="sh-k1" stroke="{warn}"><line x1="38" y1="20" x2="38" y2="30" opacity=".5"/><rect x="36.8" y="22" width="2.4" height="4" fill="{warn}" stroke="none" opacity=".5"/></g>
  <g class="sh-k2" stroke="{ok}"><line x1="42" y1="18" x2="42" y2="28" opacity=".7"/><rect x="40.8" y="20" width="2.4" height="5" fill="{ok}" stroke="none" opacity=".7"/></g>
  <g class="sh-k3" stroke="{warn}"><line x1="46" y1="21" x2="46" y2="31" opacity=".5"/><rect x="44.8" y="24" width="2.4" height="4" fill="{warn}" stroke="none" opacity=".5"/></g>
</g>''',
'penelope': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <line class="sp-e1" pathLength="1" x1="9" y1="10" x2="20" y2="7" opacity=".55"/>
  <line class="sp-e2" pathLength="1" x1="20" y1="7" x2="31" y2="12" opacity=".55"/>
  <line class="sp-e3" pathLength="1" x1="9" y1="10" x2="16" y2="20" opacity=".55"/>
  <line class="sp-e4" pathLength="1" x1="31" y1="12" x2="24" y2="21" opacity=".55"/>
  <circle class="sp-n1" cx="9" cy="10" r="2.1" fill="{c}" stroke="none"/>
  <circle class="sp-n2" cx="20" cy="7" r="2.1" fill="{c}" stroke="none"/>
  <circle class="sp-n3" cx="31" cy="12" r="2.1" fill="{c}" stroke="none"/>
  <circle class="sp-n4" cx="16" cy="20" r="1.9" fill="{c}" stroke="none" opacity=".85"/>
  <circle class="sp-n5" cx="24" cy="21" r="1.9" fill="{c}" stroke="none" opacity=".85"/>
  <path class="sp-chk" pathLength="1" d="M34 15 l2 2.2 l4.5 -4.8" stroke="{ok}"/>
  <line x1="7" y1="27.5" x2="41" y2="27.5" opacity=".22" stroke-dasharray="2 2.5"/>
  <line class="sp-p1" pathLength="1" x1="8" y1="33" x2="40" y2="33" opacity=".8"/>
  <line class="sp-p2" pathLength="1" x1="8" y1="38" x2="34" y2="38" opacity=".6"/>
  <line class="sp-p3" pathLength="1" x1="8" y1="43" x2="27" y2="43" opacity=".45"/>
</g>'''}

# ── 애니메이션 CSS (이력서와 동일 문법 — 장면 7.2s / 질감 2.4s)
KEYFRAMES = '''
@keyframes sigPulse{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.22)}}
@keyframes sigSwapDn{0%,16%{transform:translateY(0)}30%,60%{transform:translateY(8px)}76%,100%{transform:translateY(0)}}
@keyframes sigSwapUp{0%,16%{transform:translateY(0)}30%,60%{transform:translateY(-8px)}76%,100%{transform:translateY(0)}}
@keyframes sigBadOut{0%,38%{transform:translateY(0);opacity:.3}54%,82%{transform:translateY(7px);opacity:0}94%,100%{transform:translateY(0);opacity:.3}}
@keyframes sigFlow{to{stroke-dashoffset:-24}}
@keyframes sigDrawC1{0%,4%{stroke-dashoffset:1}18%,88%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes sigDrawC2{0%,10%{stroke-dashoffset:1}24%,88%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes sigDrawC3{0%,12%{stroke-dashoffset:1;opacity:.7}22%,58%{stroke-dashoffset:0;opacity:.7}66%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes sigDrawA1{0%,26%{stroke-dashoffset:1}34%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes sigDrawA2{0%,30%{stroke-dashoffset:1}38%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes sigDrawChk{0%,40%{stroke-dashoffset:1}48%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes sigGate{0%,20%{opacity:.7}24%{opacity:1}28%{opacity:.5}32%{opacity:1}38%,100%{opacity:.7}}
@keyframes sigDrawX{0%,28%{stroke-dashoffset:1;opacity:1}36%,58%{stroke-dashoffset:0;opacity:1}66%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes sigSeg{0%{stroke-dashoffset:1}9%{stroke-dashoffset:0}76%{stroke-dashoffset:0}86%,100%{stroke-dashoffset:1}}
@keyframes sigRing{0%,44%{transform:scale(1);opacity:0}50%{opacity:.8}68%{transform:scale(2.1);opacity:0}100%{transform:scale(1);opacity:0}}
@keyframes sigSus{0%,42%{transform:scale(1)}52%{transform:scale(1.35)}62%,100%{transform:scale(1)}}
@keyframes sigDot{0%{transform:translateX(0);opacity:0}6%{opacity:1}26%,44%{transform:translateX(15px);opacity:1}58%{transform:translateX(22px);opacity:1}66%{transform:translateX(27px);opacity:0}100%{transform:translateX(0);opacity:0}}
@keyframes sigHitl{0%,26%{opacity:.6}30%{opacity:1}34%{opacity:.6}38%{opacity:1}44%,100%{opacity:.6}}
@keyframes sigGateHold{0%,26%{opacity:1}30%,44%{opacity:.45}48%,100%{opacity:1}}
@keyframes sigKFlick{0%,100%{opacity:.5}50%{opacity:.85}}
'''
BIND = {
'bookmon': '''.sb-b{animation:sigSwapDn 7.2s cubic-bezier(.4,0,.2,1) infinite}
.sb-c{animation:sigSwapUp 7.2s cubic-bezier(.4,0,.2,1) infinite}
.sb-bad{animation:sigBadOut 7.2s ease infinite}
.sb-dot{animation:sigPulse 2.4s ease-in-out infinite}''',
'starlink': '''.ss-in,.ss-out{stroke-dasharray:8 4;animation:sigFlow 2.4s linear infinite}
.ss-node{animation:sigPulse 2.4s ease-in-out infinite}
.ss-ear{animation:sigPulse 2.4s ease-in-out .6s infinite}''',
'medical-rag': '''.sm-c1{stroke-dasharray:1;animation:sigDrawC1 7.2s ease infinite}
.sm-c2{stroke-dasharray:1;animation:sigDrawC2 7.2s ease infinite}
.sm-c3{stroke-dasharray:1;animation:sigDrawC3 7.2s ease infinite}
.sm-a1{stroke-dasharray:1;animation:sigDrawA1 7.2s ease infinite}
.sm-a2{stroke-dasharray:1;animation:sigDrawA2 7.2s ease infinite}
.sm-chk{stroke-dasharray:1;animation:sigDrawChk 7.2s ease infinite}
.sm-gate{animation:sigGate 7.2s ease infinite}
.sm-x{stroke-dasharray:1;animation:sigDrawX 7.2s ease infinite}''',
'rocket-sim': '''.sr-e1{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite}
.sr-e2{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:.55s}
.sr-e3{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:1.1s}
.sr-e4{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:1.65s}
.sr-e5{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:2.2s}
.sr-ring{animation:sigRing 7.2s ease-out infinite}
.sr-sus{animation:sigSus 7.2s ease infinite}''',
'hyunsoo-bot': '''.sh-dot{animation:sigDot 7.2s cubic-bezier(.4,0,.2,1) infinite}
.sh-hitl{animation:sigHitl 7.2s ease infinite}
.sh-g1,.sh-g2{animation:sigGateHold 7.2s ease infinite}
.sh-k1{animation:sigKFlick 2.4s ease-in-out infinite}
.sh-k2{animation:sigKFlick 2.4s ease-in-out .5s infinite}
.sh-k3{animation:sigKFlick 2.4s ease-in-out 1s infinite}''',
'penelope': '''.sp-e1{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite}
.sp-e2{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:.2s}
.sp-e3{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:.4s}
.sp-e4{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:.6s}
.sp-n1{animation:sigPulse 2.4s ease-in-out infinite}
.sp-n2{animation:sigPulse 2.4s ease-in-out .3s infinite}
.sp-n3{animation:sigPulse 2.4s ease-in-out .6s infinite}
.sp-n4{animation:sigPulse 2.4s ease-in-out .9s infinite}
.sp-n5{animation:sigPulse 2.4s ease-in-out 1.2s infinite}
.sp-chk{stroke-dasharray:1;animation:sigDrawChk 7.2s ease infinite}
.sp-p1{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:1.9s}
.sp-p2{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:2.15s}
.sp-p3{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:2.4s}'''}

# 카드별 대표 칩 (수치 = resume-data.yml evidenceAxes 원문 실측만)
CHIPS = {
 'bookmon':     ['▲ 정확도 84.44→97.78% [실측]', '룰 ablation · 18쿼리 오프라인'],
 'starlink':    ['EN·JA·ZH → KO 3개 언어쌍', '디버깅 포스트모템 13편'],
 'medical-rag': ['EM 0.71 · BERTScore 0.73 [실측]', 'Mode A/B/C 3원 통제'],
 'rocket-sim':  ['N=20 · 시드 고정 하네스', 'raw/display 분리 · claim gate'],
 'hyunsoo-bot': ['dry-run eval 100% (모의)', '리스크 레이어 + HITL'],
 'penelope':    ['Vitest 893 통과 [실측]', '설정·표현 분리 하네스 · MIT'],
}

CARD_JL = {
 'penelope': ('서사의 일관성 붕괴를 세계 설정 분리로 통제한다.', 'AI 네이티브 제품·서사 하네스 설계'),
}
CARD_STAGE = {
 'penelope': 'OpenAI Build Week · 라이브 데모',
}

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def card_svg(slug, theme):
    t, hue = T[theme], HUE[slug][theme]
    p = P[slug]
    chips = CHIPS[slug]
    if slug in CARD_JL:
        jl_desc, jl_role = CARD_JL[slug]
    else:
        jl = p['jobLink'].split(' — ')
        jl_desc, jl_role = (jl[0], jl[1]) if len(jl) == 2 else (p['jobLink'], '')
    body = SIG_BODY[slug].format(c=hue, warn=t['warn'], ok=t['ok'], accent=t['accent'])
    bind = BIND[slug]
    title = esc(p['label'])
    sub = esc(p['subtitle'])
    stage = esc(CARD_STAGE.get(slug, p['stage']))
    return f'''<svg width="440" height="176" viewBox="0 0 440 176" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
text{{font-family:{FONT}}} .mono{{font-family:{MONO}}}
{KEYFRAMES}
{bind}
.sig *{{transform-box:fill-box;transform-origin:center}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<rect x="1" y="1" width="438" height="174" rx="10" fill="{t['card']}" stroke="{hue}" stroke-opacity=".38"/>
<rect x="1" y="1" width="438" height="174" rx="10" fill="{hue}" opacity="{'0.045' if theme=='light' else '0.07'}"/>
<g class="sig" transform="translate(22,50) scale(1.6)">{body}</g>
<text x="118" y="38" font-size="19" font-weight="700" fill="{t['ink']}">{title}</text>
<text x="118" y="57" font-size="12" fill="{t['muted']}">{sub}</text>
<text class="mono" x="118" y="84" font-size="12" font-weight="600" fill="{hue}">{esc(chips[0])}</text>
<text class="mono" x="118" y="103" font-size="11" fill="{t['muted']}">{esc(chips[1])}</text>
<text x="118" y="128" font-size="10.5" fill="{t['muted']}">{esc(jl_desc)}</text>
<text x="118" y="144" font-size="10.5" font-weight="600" fill="{t['ink']}">증명 역량 — {esc(jl_role)}</text>
<g class="mono" font-size="9">
  <rect x="116" y="153" width="{8+len(stage)*8.2:.0f}" height="16" rx="3" fill="none" stroke="{t['rule']}"/>
  <text x="122" y="164" fill="{t['muted']}">{stage}</text>
</g>
<text class="mono" x="424" y="165" font-size="10" font-weight="600" fill="{hue}" text-anchor="end">포트폴리오 →</text>
</svg>'''

def banner_svg(theme):
    t = T[theme]
    _h = esc(DATA['meta'].get('headline', ''))
    acc0 = t['accent']
    for kw in ('기획 역량', 'AI 엔지니어'):
        _h = _h.replace(kw, f'<tspan fill="{acc0}">{kw}</tspan>')
    hl = f'<text x="40" y="86" font-size="17" font-weight="600" fill="{t["ink"]}">{_h}</text>'
    rib = DATA['evidence_ribbon']
    acc = t['accent']
    net = SIG_BODY['rocket-sim'].format(c=t['muted'], warn=acc, ok=t['ok'], accent=acc)
    cells = ''
    xs = [40, 260, 480, 700]
    for i, (x, r) in enumerate(zip(xs, rib)):
        num = esc(str(r['num'])); unit = esc(str(r.get('unit', '')))
        l1, l2 = [esc(s) for s in (r['label'].split('<br>') + [''])[:2]]
        num_fill = acc
        num_size = 30 if len(num) < 8 else 21
        dir_svg = ''
        if num.startswith('▲'):
            num = num[1:]
            dir_svg = f'<text class="mono" x="{x}" y="150" font-size="14" font-weight="700" fill="{t["ok"]}">▲</text>'
            x_num = x + 16
        else:
            x_num = x
        cells += f'''{dir_svg}<text class="mono" x="{x_num}" y="152" font-size="{num_size}" font-weight="700" fill="{num_fill}">{num}<tspan font-size="13" fill="{t['muted']}"> {unit}</tspan></text>
<text class="mono" x="{x}" y="172" font-size="10" fill="{t['ink']}" opacity=".85">{l1}</text>
<text class="mono" x="{x}" y="186" font-size="9.5" fill="{t['muted']}">{l2}</text>
'''
    return f'''<svg width="920" height="210" viewBox="0 0 920 210" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
text{{font-family:{FONT}}} .mono{{font-family:{MONO}}}
{KEYFRAMES}
.ss-in,.ss-out{{stroke-dasharray:8 4;animation:sigFlow 2.4s linear infinite}}
.sr-e1{{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite}}
.sr-e2{{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:.55s}}
.sr-e3{{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:1.1s}}
.sr-e4{{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:1.65s}}
.sr-e5{{stroke-dasharray:1;animation:sigSeg 7.2s ease infinite;animation-delay:2.2s}}
.sr-ring{{animation:sigRing 7.2s ease-out infinite}}
.sr-sus{{animation:sigSus 7.2s ease infinite}}
.hl{{stroke-dasharray:1;animation:sigDrawC1 7.2s ease infinite}}
.sig *{{transform-box:fill-box;transform-origin:center}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<rect width="920" height="210" rx="12" fill="{t['card']}" stroke="{t['rule']}"/>
<g class="sig" transform="translate(846,18) scale(1.15)" opacity=".5">{net}</g>
<g class="sig" opacity=".45"><path class="ss-in" pathLength="24" stroke="{acc}" stroke-width="1.5" fill="none" d="M700 40 C710 24,720 24,730 40 S750 58,760 40 S780 22,790 40 S806 52,816 40"/></g>
<text x="40" y="52" font-size="26" font-weight="800" fill="{t['ink']}">이주형 <tspan font-size="14" font-weight="500" fill="{t['muted']}">Lee Ju Hyeong · AI Application Engineer</tspan></text>
{hl}
<line class="hl" pathLength="1" x1="40" y1="98" x2="424" y2="98" stroke="{acc}" stroke-width="2"/>
<text x="40" y="118" font-size="11.5" fill="{t['muted']}">측정하지 않은 것은 측정 전이라고 씁니다 — 수치는 원문 실측만, stage 라벨은 그대로.</text>
{cells}
</svg>'''

honesty_must = ['claim gate 미통과', '[실측]', '84.44→97.78']
made = []
for theme in ('light', 'dark'):
    b = banner_svg(theme)
    (OUT / f'banner-{theme}.svg').write_text(b, encoding='utf-8')
    made.append(f'banner-{theme}.svg')
    for slug in HUE:
        s = card_svg(slug, theme)
        (OUT / f'card-{slug}-{theme}.svg').write_text(s, encoding='utf-8')
        made.append(f'card-{slug}-{theme}.svg')

# ── QA: XML 파싱 + 정직 문자열 + 금지 요소(script/외부참조)
fails = 0
for f in made:
    txt = (OUT / f).read_text(encoding='utf-8')
    try:
        ET.fromstring(txt)
    except ET.ParseError as e:
        print(f'❌ {f}: XML 파스 실패 {e}'); fails += 1; continue
    if '<script' in txt or 'http://' in txt.replace('http://www.w3.org', '') or 'https://' in txt:
        print(f'❌ {f}: 외부 참조/script 금지 위반'); fails += 1
    if 'banner' in f:
        for h in honesty_must:
            if h not in txt:
                print(f'❌ {f}: 정직 문자열 누락 {h}'); fails += 1
print(('✅ QA 통과 — ' if not fails else '❌ 실패 — ') + f'{len(made)}개 생성: ' + ', '.join(made))
sys.exit(1 if fails else 0)
