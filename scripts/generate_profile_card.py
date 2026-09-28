"""Build the self-contained animated terminal card used in the profile README."""

from html import escape
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets" / "st-basil-ascii.txt"
OUTPUT = Path(os.environ.get("PROFILE_CARD_OUTPUT", ROOT / "assets" / "terminal-profile.svg"))
STATIC = os.environ.get("PROFILE_CARD_STATIC") == "1"

WIDTH = 1100
HEIGHT = 675
ART_X = 30
ART_Y = 151
ROW_HEIGHT = 17
ART_WIDTH = 480


def text(x: int, y: int, value: str, color: str, size: int = 14, extra: str = "") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'{extra}>{escape(value)}</text>'
    )


def main() -> None:
    rows = ART.read_text(encoding="utf-8").splitlines()
    if len(rows) != 28 or max(map(len, rows)) > 49:
        raise ValueError("The cathedral art must fit the 49×28 terminal canvas")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        'aria-label="Animated ASCII Saint Basil cathedral and ran9all terminal profile" '
        'font-family="Menlo, Consolas, monospace">',
        '<defs><linearGradient id="bg" x2="0" y2="1">'
        '<stop stop-color="#111928"/><stop offset="1" stop-color="#090e17"/>'
        '</linearGradient></defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="16" fill="url(#bg)"/>',
        f'<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}" rx="15" '
        'fill="none" stroke="#334155" stroke-width="2"/>',
        '<path d="M0 38H1100" stroke="#334155"/>',
    ]
    for x, color in ((22, "#ff5f56"), (42, "#ffbd2e"), (62, "#27c93f")):
        parts.append(f'<circle cx="{x}" cy="19" r="6" fill="{color}"/>')
    parts += [
        text(407, 25, "ran9all@github:~ / red-square", "#94a3b8", 13),
        text(30, 71, "ran9all@github:~$ whoami", "#74d7e8", 16),
        text(30, 97, "ran9all", "#e2e8f0", 17),
        text(30, 132, "ran9all@github:~$ ./red-square.sh", "#74d7e8", 16),
        '<path d="M530 116V589" stroke="#334155"/>',
    ]

    for index, row in enumerate(rows):
        y = ART_Y + index * ROW_HEIGHT
        delay = 0.55 + index * 0.105
        line = (f'<text x="{ART_X}" y="{y}" xml:space="preserve" '
                f'fill="#c8e5eb" font-size="15">{escape(row)}</text>')
        if STATIC:
            parts.append(line)
        else:
            parts.append(
                f'<clipPath id="row{index}"><rect x="{ART_X}" y="{y-15}" '
                f'width="0" height="{ROW_HEIGHT}">'
                f'<animate attributeName="width" from="0" to="{ART_WIDTH}" '
                f'begin="{delay:.3f}s" dur="0.105s" fill="freeze"/>'
                '</rect></clipPath>'
            )
            parts.append(f'<g clip-path="url(#row{index})">{line}</g>')

    profile_rows = [
        ("name", "Randall"),
        ("host", "github.com/ran9all"),
        ("location", "Moscow, Russia"),
        ("education", "MPEI"),
        ("focus", "Cybersecurity / Backend"),
        ("builds", "Bots / APIs / Automation"),
        ("languages", "Python / TS / JS / Go / C++"),
        ("tools", "Docker / Linux / Git"),
    ]
    parts.append(text(570, 178, "ran9all@github", "#7dd3fc", 22, 'font-weight="bold"'))
    parts.append('<path d="M570 191H1060" stroke="#334155"/>')
    for index, (key, value) in enumerate(profile_rows):
        y = 224 + index * 39
        delay = 0.5 + index * 0.16
        content = text(570, y, key, "#a78bfa", 15) + text(710, y, value, "#e2e8f0", 15)
        if STATIC:
            parts.append(content)
        else:
            parts.append(
                f'<g opacity="0">{content}'
                f'<animate attributeName="opacity" from="0" to="1" '
                f'begin="{delay:.2f}s" dur="0.4s" fill="freeze"/></g>'
            )
    parts += [
        text(570, 566, "BUILD THINGS THAT MATTER", "#74d7e8", 14),
        '<path d="M30 611H1070" stroke="#334155"/>',
        text(30, 643, "ran9all@github:~$", "#74d7e8", 15),
        '<rect x="190" y="629" width="9" height="17" fill="#c8e5eb">'
        '<animate attributeName="opacity" values="1;1;0;0" '
        'keyTimes="0;0.5;0.51;1" dur="1s" repeatCount="indefinite"/></rect>',
        '</svg>',
    ]
    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
