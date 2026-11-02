"""Builds truth/NUMBERS from the manuscript: every number in the given .tex files is located
in the repository's source files (first file:line). Unmatched numbers are listed and make the
exit code non-zero. Decimal commas and the Unicode minus in sources are normalised.

Usage: python numbers_check.py <out.md> <tex> [<tex> ...]
"""

import re
import sys

SOURCES = [
    "results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.md",
    "results/TILLEGG_KHEPRI-TSFM_v1_2026-11-02.md",
    "results/REPRO-V15_KHEPRI-TSFM_v1_2026-11-02.md",
    "results/MDE_KHEPRI-TSFM_v1_2026-11-02.md",
    "results/RESULTATER_KHEPRI-TSFM_v1_2026-11-02.json",
    "results/LATENS_KHEPRI-TSFM_v1_2026-11-02.md",
    "data/CI_KHEPRI-TSFM_v1_2026-11-02.meta.json",
    "prereg/PREREG_KHEPRI-TSFM_v1_2026-11-02.md",
    "truth/DECISIONS_KHEPRI-TSFM_v1_2026-11-02.md",
    "truth/DEVIATIONS_KHEPRI-TSFM_v1_2026-11-02.md",
    "truth/KJENTGRUNNLAG_KHEPRI-TSFM_v1_2026-11-02.md",
    "truth/STATE_KHEPRI-TSFM_v1_2026-11-02.md",
    "truth/SOURCES_KHEPRI-TSFM_v1_2026-11-02.md",
]
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])")


def norm(s):
    s = s.replace("\u2212", "-").replace("\u2013", "-")
    s = re.sub(r"(?<=\d)[ \u00a0\u202f](?=\d{3}\b)", "", s)  # 32 768 -> 32768
    return re.sub(r"(?<=\d),(?=\d)", ".", s)


# not numbers of the study: identifiers, locators, section references, Unicode code points
SKIP = re.compile(r"doi:\S+|arXiv:\S+|10\.\d{4,}/\S+|\b\S+\.(?:md|py|json|tex|toml):\d+(?:[-,]\d+)*|"
                  r"\b(?:Section|Sections|§)\s*~?\\?(?:ref\{[^}]*\}|\d+(?:\.\d+)*)|\bS\d\d\b|"
                  r"\\DeclareUnicodeCharacter\{[0-9A-F]+\}")


NAMES = re.compile(r"Timestral-\d+M|Chronos-2|\b(?:NO|SE)\d(?:--(?:NO|SE)?\d)?|D-\d+|CO\$_2\$|"
                   r"\d{4}-\d{2}-\d{2}|v1\.5|\\texttt\{[^}]*\}|prereg-v1")


def strip_tex(line):
    line = re.sub(r"(?<!\\)%.*", "", line)
    line = re.sub(r"^#+\s+\d+(?:\.\d+)*", " ", line)  # Markdown heading numbers
    line = SKIP.sub(" ", norm(line))
    line = NAMES.sub(" ", line)
    line = re.sub(r"\\(label|ref|caption\{|begin|end|section|subsection|paragraph)\{[^}]*\}", " ", line)
    line = re.sub(r"\\[a-zA-Z]+", " ", line)
    return line.replace("\\", " ")


def find(n, src):
    """Exact match first; else a source value with more decimals that rounds to n."""
    exact = re.compile(r"(?<![\d.])-?" + re.escape(n) + r"(?![\d]|[.,]\d)")
    for fp, i, l in src:
        if exact.search(l):
            return fp, i
    if "." in n:
        nd = len(n.split(".")[1])
        longer = re.compile(r"(?<![\d.])-?(" + re.escape(n.split(".")[0]) + r"\.\d{" + str(nd + 1) + r",})")
        for fp, i, l in src:
            for m in longer.finditer(l):
                if f"{float(m.group(1)):.{nd}f}" == n:
                    return fp, i
    return None


def main(out, *tex):
    src = []
    for fp in SOURCES:
        for i, l in enumerate(open(fp, encoding="utf-8"), 1):
            src.append((fp, i, norm(l)))
    rows, missing = [], []
    for tf in tex:
        text = open(tf, encoding="utf-8").read()
        # drop HTML comments (source notes in the Markdown sections) but keep line numbers
        text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
        lines = text.splitlines()
        if lines and lines[0].startswith("Arkivnøkkel:") or lines and lines[0].startswith("% Arkivnøkkel:"):
            lines[0] = ""
        refs = next((i for i, l in enumerate(lines) if re.match(r"#+ References", l)), len(lines))
        for ln, line in enumerate(lines[:refs], 1):
            for m in NUM.finditer(strip_tex(line)):
                n = m.group(0).lstrip("-")
                hit = find(n, src)
                rec = (n, f"{tf}:{ln}", f"{hit[0]}:{hit[1]}" if hit else "IKKE FUNNET")
                rows.append(rec)
                if not hit:
                    missing.append(rec)
    seen, uniq = set(), []
    for r in rows:
        if (r[0], r[1]) not in seen:
            seen.add((r[0], r[1])); uniq.append(r)
    md = ["Arkivnøkkel: NUMBERS_KHEPRI-TSFM_v1_2026-11-02", "",
          "Hvert tall i manus med kilde fil:linje (generert av numbers_check.py; første treff i kildefilene).",
          "Står det ikke her, står det ikke i manus.", "",
          "| Tall | Manus (fil:linje) | Kilde (fil:linje) |", "|---|---|---|"]
    md += [f"| {n} | {m} | {s} |" for n, m, s in uniq]
    open(out, "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{len(uniq)} tall, {len(missing)} ikke funnet")
    for r in missing:
        print("IKKE FUNNET:", *r)
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main(*sys.argv[1:])
