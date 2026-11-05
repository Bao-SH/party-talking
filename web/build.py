"""把 题库.md 解析成 JSON，注入 template.html，生成 index.html。用法：python3 web/build.py"""
import json, re, pathlib
root = pathlib.Path(__file__).resolve().parent
md = (root.parent / "题库.md").read_text(encoding="utf-8").splitlines()
DIRS = {"一": "family", "二": "love", "三": "work", "四": "life", "五": "self"}
LEVEL = {"🟢": 1, "🟡": 2, "🔴": 3}
qs, d, lv, couple = [], None, None, False
for i, line in enumerate(md):
    m = re.match(r"## ([一二三四五])、", line)
    if m: d, couple = DIRS[m.group(1)], False; continue
    if line.startswith("### 💑"): couple = True; continue
    m = re.match(r"(?:### |\*\*)(🟢|🟡|🔴)", line)
    if m: lv = LEVEL[m.group(1)]; continue
    m = re.match(r"\d+\. \*\*(.+?)\*\*(?:（(.+?)）)?\s*$", line)
    if m and d:
        follow = ""
        if i + 1 < len(md) and md[i+1].strip().startswith("→"):
            follow = md[i+1].strip()[1:].strip()
        qs.append({"d": "couple" if couple else d, "l": lv, "q": m.group(1),
                   "tag": m.group(2) or "", "f": follow})
html = (root / "template.html").read_text(encoding="utf-8")
(root / "index.html").write_text(html.replace("/*__DATA__*/[]", json.dumps(qs, ensure_ascii=False)), encoding="utf-8")
from collections import Counter
print(len(qs), "题", Counter((q["d"], q["l"]) for q in qs))
