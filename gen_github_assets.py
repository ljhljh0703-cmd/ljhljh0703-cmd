#!/usr/bin/env python3
# GitHub 프로필 그림(배너 1장 + 대표 카드 6장) 생성기. 2026-10-21 작품 모음과 같은 종이 인쇄물 결로 다시 만듦.
# 글과 숫자는 작품 모음 curation.json · 각 작품 페이지 첫 화면 · 이력서 재료에 있는 값만 쓴다. 바뀌면 아래 CARDS·FACTS를 고치고 다시 돌린다.
#   cd "/Users/godju/Claude/Projects/포트폴리오 리뉴얼/깃허브-프로필" && python3 gen_github_assets.py
# GitHub README는 <style>·JS를 지우지만, <img>로 넣은 SVG 안의 CSS 움직임은 돈다. 바깥 글꼴·바깥 주소는 쓰지 않는다.
import sys, pathlib, xml.etree.ElementTree as ET

HERE = pathlib.Path(__file__).parent
OUT = HERE / 'assets'; OUT.mkdir(exist_ok=True)

FONT = "'Apple SD Gothic Neo','Malgun Gothic','Noto Sans KR','Segoe UI',sans-serif"
PAPER, INK, INK2, LINE = '#f1e9d8', '#1b1a17', '#5e5647', '#cfc4ad'
RED, BLUE, TEAL, OK = '#c0412a', '#4b4ad1', '#207878', '#2f7d3a'
ON = '#fff4e8'

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def textw(s, fs):
    """글자 폭 어림: 한글 1em, 그 밖 0.6em."""
    return sum(fs if ord(ch) > 0x2E80 else fs * 0.6 for ch in s)

# ── 대표 카드 6장 (순서 = README 표 순서). 출처: 작품 모음 curation.json items · 작품 페이지 첫 화면
CARDS = [
 dict(slug='game-ops', ink=TEAL, title='게임 운영 플랫폼', sub='플레이어 제보가 그대로 개발 지시서가 됨',
      result='실제 플레이어 제보 6건 → 개발 지시서 1건', line2='고친 PR이 합쳐지면 제보자에게 답장', stage='작동 데모 · 개인'),
 dict(slug='bookmon', ink=BLUE, title='북켓몬 · AI 도서 검색·추천', sub='질문의 뜻에 맞는 책만 위로 올리는 추천 순위',
      result='엉뚱한 추천 90권 중 14권 → 2권', line2='18개 질의 상위 5권 · 팀원 4명 채점', stage='데모 · 4인 팀 팀장'),
 dict(slug='jelly-panic', ink=TEAL, title='지켜줘! 젤리 패닉', sub='재미 규칙을 먼저 정하고 500판으로 증명한 퍼즐',
      result='무작위 500판, 막을 수 없는 위협 0건', line2='규칙이 없던 방식이면 막을 수 없는 칸 18.2%', stage='웹 플레이 · 개인'),
 dict(slug='starlink', ink=TEAL, title='StarLink · 실시간 통역', sub='주변 외국어를 한국어로, 보청기로 바로',
      result='20초 뒤 멈추던 통역 → 계속 이어짐', line2='EN·JA·ZH → KO · 실기기 데모', stage='작동 프로토타입 · 개인'),
 dict(slug='medical-rag', ink=RED, title='알려줄고양 · 내과 자문 챗봇', sub='위험한 질문은 모델 앞에서 거름',
      result='응급 문구 13가지 → 바로 119 안내', line2='경고 단어 37개는 경고 뒤 답변', stage='데모 · 4인 팀 팀장'),
 dict(slug='penelope', ink=BLUE, title='Penelope · 이야기 생성 엔진', sub='선택 하나에 세계 속 인물이 모두 반응하는 엔진',
      result='자동 시험 893개 모두 통과', line2='장면 밖 인물 반응 · 이야기 가드레일 4개', stage='공개 라이브 데모 · OpenAI Build Week 제출'),
]

# ── 카드 왼쪽 그림(48칸 무대). {c}=작품 색 {w}=차단 {ok}=통과
SIG = {
'game-ops': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <rect x="3" y="10" width="15" height="11" rx="2"/><path d="M7 21 l-2 4 l5 -4"/>
  <circle class="go-d1" cx="7.5" cy="15.5" r="1.1" fill="{c}" stroke="none"/><circle class="go-d2" cx="10.5" cy="15.5" r="1.1" fill="{c}" stroke="none"/><circle class="go-d3" cx="13.5" cy="15.5" r="1.1" fill="{c}" stroke="none"/>
  <path class="go-f" d="M19 15.5 L27 15.5"/>
  <rect x="28" y="8" width="17" height="15" rx="1.5"/><line x1="31" y1="12.5" x2="42" y2="12.5" opacity=".6"/><line x1="31" y1="16" x2="39" y2="16" opacity=".6"/><line x1="31" y1="19.5" x2="36" y2="19.5" opacity=".6"/>
  <path class="go-r" pathLength="1" d="M36.5 24 C36.5 38, 10.5 38, 10.5 27"/>
  <path class="go-chk" pathLength="1" d="M19.5 35.5 l2.4 2.4 l4.6 -4.8" stroke="{ok}"/>
</g>''',
'bookmon': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <line x1="7" y1="8" x2="7" y2="40" opacity=".35"/>
  <rect x="11" y="9" width="26" height="4.5" rx="1"/><circle class="bk-dot" cx="41.5" cy="11.2" r="1.6" fill="{c}" stroke="none"/>
  <rect class="bk-b" x="11" y="17" width="21" height="4.5" rx="1" opacity=".8"/>
  <rect class="bk-c" x="11" y="25" width="16" height="4.5" rx="1" opacity=".55"/>
  <rect class="bk-bad" x="11" y="33" width="12" height="4.5" rx="1" opacity=".3" stroke="{w}"/>
</g>''',
'jelly-panic': '''<g stroke="{c}" stroke-width="1.3" stroke-linecap="round" fill="none">
  <rect x="6" y="6" width="36" height="36" rx="1" opacity=".5"/>
  <line x1="18" y1="6" x2="18" y2="42" opacity=".35"/><line x1="30" y1="6" x2="30" y2="42" opacity=".35"/>
  <line x1="6" y1="18" x2="42" y2="18" opacity=".35"/><line x1="6" y1="30" x2="42" y2="30" opacity=".35"/>
  <rect x="20.5" y="20.5" width="7" height="7" rx="2.2" fill="{c}" stroke="none" opacity=".85"/>
  <g class="jp-th" stroke="{w}"><circle cx="36" cy="12" r="3.6"/><line x1="36" y1="10" x2="36" y2="12.4"/><circle cx="36" cy="14.1" r=".5" fill="{w}"/></g>
  <rect class="jp-cov" x="31.5" y="19.5" width="9" height="9" rx="1" fill="{ok}" stroke="none"/>
</g>''',
'starlink': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" fill="none">
  <path class="sl-in" pathLength="24" d="M3 24 C5 17,7 17,9 24 S13 32,15 24 S19 15,21 24" opacity=".85"/>
  <rect class="sl-node" x="22" y="20.5" width="7" height="7" rx="1" transform="rotate(45 25.5 24)" stroke="{w}"/>
  <path class="sl-out" pathLength="24" d="M31 24 C32.5 20,34 20,35.5 24 S38.5 28,40 24 S43 20,44.5 24" opacity=".85"/>
  <circle class="sl-ear" cx="45.5" cy="24" r="1.7" fill="{c}" stroke="none"/>
</g>''',
'medical-rag': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <rect x="4" y="6" width="10" height="12" rx="1"/><line x1="6.5" y1="10" x2="11.5" y2="10" opacity=".5"/><line x1="6.5" y1="13" x2="10" y2="13" opacity=".5"/>
  <rect x="4" y="18" width="10" height="12" rx="1" opacity=".5" stroke="{w}"/>
  <rect x="4" y="30" width="10" height="12" rx="1" opacity=".85"/><line x1="6.5" y1="34" x2="11.5" y2="34" opacity=".5"/><line x1="6.5" y1="37" x2="10" y2="37" opacity=".5"/>
  <path class="md-c1" pathLength="1" d="M14 12 C22 12,24 20,30 22"/>
  <path class="md-c2" pathLength="1" d="M14 36 C22 36,24 28,30 26"/>
  <path class="md-c3" pathLength="1" d="M14 24 L22 24" opacity=".7"/>
  <line class="md-gate" x1="24" y1="19" x2="24" y2="29" opacity=".7" stroke="{w}"/>
  <path class="md-x" pathLength="1" d="M19.6 22.6 L22.4 25.4 M22.4 22.6 L19.6 25.4" stroke-width="1.3" stroke="{w}"/>
  <rect x="30" y="16" width="14" height="16" rx="1"/>
  <line class="md-a1" pathLength="1" x1="33" y1="21" x2="41" y2="21"/>
  <line class="md-a2" pathLength="1" x1="33" y1="25" x2="39" y2="25"/>
  <path class="md-chk" pathLength="1" d="M33 29.5 l2.2 2.2 l4.2 -4.2" stroke="{ok}"/>
</g>''',
'penelope': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <line class="pn-e1" pathLength="1" x1="9" y1="10" x2="20" y2="7" opacity=".55"/>
  <line class="pn-e2" pathLength="1" x1="20" y1="7" x2="31" y2="12" opacity=".55"/>
  <line class="pn-e3" pathLength="1" x1="9" y1="10" x2="16" y2="20" opacity=".55"/>
  <line class="pn-e4" pathLength="1" x1="31" y1="12" x2="24" y2="21" opacity=".55"/>
  <circle class="pn-n1" cx="9" cy="10" r="2.1" fill="{c}" stroke="none"/>
  <circle class="pn-n2" cx="20" cy="7" r="2.1" fill="{c}" stroke="none"/>
  <circle class="pn-n3" cx="31" cy="12" r="2.1" fill="{c}" stroke="none"/>
  <circle cx="16" cy="20" r="1.9" fill="{c}" stroke="none" opacity=".85"/>
  <circle cx="24" cy="21" r="1.9" fill="{c}" stroke="none" opacity=".85"/>
  <path class="pn-chk" pathLength="1" d="M34 15 l2 2.2 l4.5 -4.8" stroke="{ok}"/>
  <line x1="7" y1="27.5" x2="41" y2="27.5" opacity=".22" stroke-dasharray="2 2.5"/>
  <line class="pn-p1" pathLength="1" x1="8" y1="33" x2="40" y2="33" opacity=".8"/>
  <line class="pn-p2" pathLength="1" x1="8" y1="38" x2="34" y2="38" opacity=".6"/>
  <line class="pn-p3" pathLength="1" x1="8" y1="43" x2="27" y2="43" opacity=".45"/>
</g>''',
'agent-forge': '''<g stroke="{c}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">
  <rect x="2" y="14" width="8" height="8" rx="1"/><rect x="14" y="14" width="8" height="8" rx="1"/><rect x="26" y="14" width="8" height="8" rx="1"/><rect x="38" y="14" width="8" height="8" rx="1" stroke="{ok}"/>
  <line x1="10" y1="18" x2="14" y2="18" opacity=".6"/><line x1="22" y1="18" x2="26" y2="18" opacity=".6"/><line x1="34" y1="18" x2="38" y2="18" opacity=".6"/>
  <circle class="af-dot" cx="6" cy="18" r="1.7" fill="{c}" stroke="none"/>
  <g class="af-bad" stroke="{w}"><rect x="26" y="30" width="8" height="8" rx="1"/><path d="M28 32 L32 36 M32 32 L28 36"/></g>
  <path class="af-chk" pathLength="1" d="M39 30 l2.2 2.2 l4.4 -4.6" stroke="{ok}"/>
</g>''',
}

KEYFRAMES = '''
@keyframes pulse{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.22)}}
@keyframes swapDn{0%,16%{transform:translateY(0)}30%,60%{transform:translateY(8px)}76%,100%{transform:translateY(0)}}
@keyframes swapUp{0%,16%{transform:translateY(0)}30%,60%{transform:translateY(-8px)}76%,100%{transform:translateY(0)}}
@keyframes badOut{0%,38%{transform:translateY(0);opacity:.3}54%,82%{transform:translateY(7px);opacity:0}94%,100%{transform:translateY(0);opacity:.3}}
@keyframes flow{to{stroke-dashoffset:-24}}
@keyframes drawA{0%,4%{stroke-dashoffset:1}18%,88%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes drawB{0%,10%{stroke-dashoffset:1}24%,88%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes drawC{0%,12%{stroke-dashoffset:1;opacity:.7}22%,58%{stroke-dashoffset:0;opacity:.7}66%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes drawD{0%,26%{stroke-dashoffset:1}34%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes drawE{0%,30%{stroke-dashoffset:1}38%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes drawChk{0%,40%{stroke-dashoffset:1}48%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes drawLate{0%,56%{stroke-dashoffset:1}64%,90%{stroke-dashoffset:0}98%,100%{stroke-dashoffset:1}}
@keyframes gate{0%,20%{opacity:.7}24%{opacity:1}28%{opacity:.5}32%{opacity:1}38%,100%{opacity:.7}}
@keyframes drawX{0%,28%{stroke-dashoffset:1;opacity:1}36%,58%{stroke-dashoffset:0;opacity:1}66%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes cover{0%,30%{opacity:0;transform:translateY(-5px)}44%,84%{opacity:.75;transform:translateY(0)}96%,100%{opacity:0;transform:translateY(0)}}
@keyframes threat{0%,30%{opacity:1}44%,84%{opacity:.25}96%,100%{opacity:1}}
@keyframes travel{0%{transform:translateX(0);opacity:0}6%{opacity:1}60%{transform:translateX(36px);opacity:1}70%,100%{transform:translateX(36px);opacity:0}}
@keyframes drop{0%,30%{transform:translateY(-12px);opacity:0}40%,60%{transform:translateY(0);opacity:1}76%,100%{transform:translateY(6px);opacity:0}}
'''
BIND = {
'game-ops': '''.go-d1{animation:pulse 2.4s ease-in-out infinite}.go-d2{animation:pulse 2.4s ease-in-out .3s infinite}.go-d3{animation:pulse 2.4s ease-in-out .6s infinite}
.go-f{stroke-dasharray:4 3;animation:flow 2.4s linear infinite}
.go-r{stroke-dasharray:1;animation:drawE 7.2s ease infinite}
.go-chk{stroke-dasharray:1;animation:drawLate 7.2s ease infinite}''',
'bookmon': '''.bk-b{animation:swapDn 7.2s cubic-bezier(.4,0,.2,1) infinite}
.bk-c{animation:swapUp 7.2s cubic-bezier(.4,0,.2,1) infinite}
.bk-bad{animation:badOut 7.2s ease infinite}
.bk-dot{animation:pulse 2.4s ease-in-out infinite}''',
'jelly-panic': '''.jp-cov{animation:cover 7.2s ease infinite}
.jp-th{animation:threat 7.2s ease infinite}''',
'starlink': '''.sl-in,.sl-out{stroke-dasharray:8 4;animation:flow 2.4s linear infinite}
.sl-node{animation:pulse 2.4s ease-in-out infinite}
.sl-ear{animation:pulse 2.4s ease-in-out .6s infinite}''',
'medical-rag': '''.md-c1{stroke-dasharray:1;animation:drawA 7.2s ease infinite}
.md-c2{stroke-dasharray:1;animation:drawB 7.2s ease infinite}
.md-c3{stroke-dasharray:1;animation:drawC 7.2s ease infinite}
.md-a1{stroke-dasharray:1;animation:drawD 7.2s ease infinite}
.md-a2{stroke-dasharray:1;animation:drawE 7.2s ease infinite}
.md-chk{stroke-dasharray:1;animation:drawChk 7.2s ease infinite}
.md-gate{animation:gate 7.2s ease infinite}
.md-x{stroke-dasharray:1;animation:drawX 7.2s ease infinite}''',
'penelope': '''.pn-e1,.pn-e2,.pn-e3,.pn-e4{stroke-dasharray:1;animation:drawA 7.2s ease infinite}
.pn-e2{animation-delay:.2s}.pn-e3{animation-delay:.4s}.pn-e4{animation-delay:.6s}
.pn-n1{animation:pulse 2.4s ease-in-out infinite}.pn-n2{animation:pulse 2.4s ease-in-out .3s infinite}.pn-n3{animation:pulse 2.4s ease-in-out .6s infinite}
.pn-chk{stroke-dasharray:1;animation:drawChk 7.2s ease infinite}
.pn-p1,.pn-p2,.pn-p3{stroke-dasharray:1;animation:drawLate 7.2s ease infinite}
.pn-p2{animation-delay:.25s}.pn-p3{animation-delay:.5s}''',
'agent-forge': '''.af-dot{animation:travel 7.2s cubic-bezier(.4,0,.2,1) infinite}
.af-bad{animation:drop 7.2s ease infinite}
.af-chk{stroke-dasharray:1;animation:drawLate 7.2s ease infinite}''',
}

STYLE_BASE = f'''text{{font-family:{FONT}}}
{KEYFRAMES}
.sig *{{transform-box:fill-box;transform-origin:center}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}'''

def card_svg(c):
    ink = c['ink']
    body = SIG[c['slug']].format(c=ink, w=RED if ink != RED else '#8a2f1f', ok=OK)
    return f'''<svg width="440" height="176" viewBox="0 0 440 176" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
{STYLE_BASE}
{BIND[c['slug']]}
</style>
<rect x="1" y="1" width="438" height="174" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>
<rect x="16" y="-4" width="56" height="16" fill="{ink}" opacity=".55" transform="rotate(-6 44 4)"/>
<g class="sig" transform="translate(20,50) scale(1.55)">{body}</g>
<text x="112" y="38" font-size="19" font-weight="800" fill="{INK}">{esc(c['title'])}</text>
<text x="112" y="58" font-size="12" fill="{INK2}">{esc(c['sub'])}</text>
<rect x="108" y="72" width="4" height="22" fill="{ink}"/>
<text x="119" y="88.5" font-size="14" font-weight="800" fill="{ink}">{esc(c['result'])}</text>
<text x="112" y="117" font-size="11.5" fill="{INK2}">{esc(c['line2'])}</text>
<line x1="112" y1="131" x2="424" y2="131" stroke="{LINE}" stroke-width="1"/>
<text x="112" y="152" font-size="11" font-weight="700" fill="{INK}">{esc(c['stage'])}</text>
<text x="422" y="152" font-size="11.5" font-weight="800" fill="{ink}" text-anchor="end">사례 보기</text>
</svg>'''

# ── 배너. 출처: 이력서 재료 evidence_ribbon(17.18억은 「2년 6개월 재직 동안 누적 매출」(작가 10-22 정의: 재직 기간 총 성과)) · 이력서 한 줄
FACTS = [
 ('최우수 수상', 'Cofathon 2026', 'KRAFTON FDE 트랙'),
 ('17.18억 원', '2년 6개월 재직 동안', '누적 매출 · B2B 제안 PM'),
 ('5일 → 2일', '제안서 완성 기간 단축', '제안 PM 시절'),
 ('AI 엔지니어 인턴', '위메이드엑스알', '2026.08 – 재직 중'),
]

def banner_svg():
    cells = ''
    for i, (num, l1, l2) in enumerate(FACTS):
        x = 40 + i * 215
        fs = 26 if textw(num, 26) < 190 else 20
        cells += f'''<text x="{x}" y="152" font-size="{fs}" font-weight="800" fill="{RED}">{esc(num)}</text>
<text x="{x}" y="174" font-size="11.5" font-weight="700" fill="{INK}">{esc(l1)}</text>
<text x="{x}" y="190" font-size="11" fill="{INK2}">{esc(l2)}</text>
'''
    head1, head2 = '현장의 문제를 정의하고 ', 'AI로 해결하는 엔지니어'
    return f'''<svg width="920" height="210" viewBox="0 0 920 210" fill="none" xmlns="http://www.w3.org/2000/svg">
<style>
{STYLE_BASE}
.ul{{animation:pulse 4.8s ease-in-out infinite}}
.sc1{{animation:pulse 4.8s ease-in-out infinite}}
</style>
<rect x="1" y="1" width="918" height="208" rx="3" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>
<g opacity=".9">
  <rect x="806" y="22" width="70" height="44" fill="{BLUE}" opacity=".75" transform="rotate(8 841 44)"/>
  <rect x="770" y="40" width="58" height="38" fill="{TEAL}" opacity=".7" transform="rotate(-10 799 59)"/>
  <rect class="sc1" x="838" y="62" width="40" height="28" fill="{RED}" opacity=".8" transform="rotate(4 858 76)"/>
  <rect x="790" y="14" width="64" height="14" fill="#e3d2a8" opacity=".9" transform="rotate(-4 822 21)"/>
</g>
<rect class="ul" x="40" y="24" width="44" height="5" fill="{RED}"/>
<text x="40" y="52" font-size="15" font-weight="800" fill="{INK2}">이주형 <tspan font-size="12" font-weight="600">Lee Ju Hyeong</tspan></text>
<text x="40" y="96" font-size="30" font-weight="800" fill="{INK}">{esc(head1)}<tspan fill="{RED}">{esc(head2)}</tspan></text>
{cells}
</svg>'''

made = []
(OUT / 'banner.svg').write_text(banner_svg(), encoding='utf-8'); made.append('banner.svg')
for c in CARDS:
    (OUT / f"card-{c['slug']}.svg").write_text(card_svg(c), encoding='utf-8'); made.append(f"card-{c['slug']}.svg")

fails = 0
for f in made:
    txt = (OUT / f).read_text(encoding='utf-8')
    try:
        ET.fromstring(txt)
    except ET.ParseError as e:
        print(f'❌ {f}: XML 파스 실패 {e}'); fails += 1; continue
    if '<script' in txt or 'https://' in txt or 'http://' in txt.replace('http://www.w3.org', ''):
        print(f'❌ {f}: 바깥 주소·script 금지'); fails += 1
for c in CARDS:
    for k, fs, lim in (('title', 19, 312), ('sub', 12, 312), ('result', 13.5, 300), ('line2', 11.5, 312)):
        if textw(c[k], fs) > lim: print(f"❌ {c['slug']}: {k} 너무 김"); fails += 1
print(('✅ 통과 — ' if not fails else '❌ 실패 — ') + f'{len(made)}개: ' + ', '.join(made))
sys.exit(1 if fails else 0)
