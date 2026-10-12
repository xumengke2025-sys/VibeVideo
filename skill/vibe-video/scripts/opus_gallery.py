#!/usr/bin/env python3
"""Bounded offline retrieval of the attributed Opus video prompt catalogue."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys

DEFAULT = Path(__file__).resolve().parents[1] / "assets" / "opus-gallery.json"
REPO = "https://github.com/yihui-dev/awesome-opus5-5-videos"
MECHANISMS = {
    "continuity": r"morph|same (?:shape|element|artwork)|continuous (?:take|camera|stream)|never cut|every scene is made",
    "portal": r"infinite zoom|portal|exponential zoom",
    "glass": r"liquid glass|refraction|caustic|displacement|fishbowl",
    "typography": r"kinetic typ|glyph|wordmark|typograph|letter.*mask",
    "audio-sync": r"beat grid|downbeat|sync|measured peak|sound design|music.*analy",
    "product-ui": r"product.*launch|actual assets|real website|capture.*pages|cursor|SaaS",
    "explainer": r"explain|educational|recipe|simulate|random walk",
    "shader": r"shader|GLSL|raymarch|OpenGL|WebGL",
}


def validate(entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError("Catalogue must contain a nonempty entry list")
    slugs = set()
    for x in entries:
        if not isinstance(x, dict):
            raise ValueError("Each entry must be an object")
        for key in ("slug", "author", "category", "prompt", "post_url", "skillry_url", "added"):
            if not isinstance(x.get(key), str) or not x[key].strip():
                raise ValueError(f"Missing string field: {key}")
        if not re.fullmatch(r"[a-z0-9-]+", x["slug"]) or x["slug"] in slugs:
            raise ValueError(f"Invalid or duplicate slug: {x['slug']}")
        slugs.add(x["slug"])
        if x["category"] not in {"motion", "explainer", "3d", "interactive"}:
            raise ValueError(f"Unknown category: {x['category']}")
        if type(x.get("prompt_partial")) is not bool:
            raise ValueError(f"Missing prompt completeness: {x['slug']}")
        if not isinstance(x.get("tech_tags"), list) or any(not isinstance(t, str) for t in x["tech_tags"]):
            raise ValueError(f"Invalid remake tech tags: {x['slug']}")
    return entries


def load(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return validate(data), {"source": str(path), "commit": None}
    if not isinstance(data, dict):
        raise ValueError("Expected upstream array or packaged catalogue")
    return validate(data.get("entries")), data.get("provenance", {})


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("stats")
    search = sub.add_parser("search")
    search.add_argument("--query", default="", help="Case-insensitive text; all words must match")
    search.add_argument("--category", choices=["motion", "explainer", "3d", "interactive"])
    search.add_argument("--tag", action="append", default=[], help="Repeat for AND filtering of remake tech tags")
    search.add_argument("--mechanism", choices=sorted(MECHANISMS))
    search.add_argument("--complete", action="store_true", help="Only prompt_partial=false; not a full-session guarantee")
    search.add_argument("--slug")
    search.add_argument("--limit", type=int, default=6)
    search.add_argument("--prompt", action="store_true", help="Include complete stored prompt; prefer a single slug")
    imp = sub.add_parser("import")
    imp.add_argument("source", type=Path)
    imp.add_argument("--out", type=Path, required=True)
    imp.add_argument("--commit", required=True, help="Verified 40-character repository commit")
    imp.add_argument("--checked", required=True, help="Research date, YYYY-MM-DD; not the works' publication date")
    args = parser.parse_args()
    if args.command == "import":
        if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
            parser.error("--commit must be a full repository commit hash")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.checked):
            parser.error("--checked must be YYYY-MM-DD")
        entries, _ = load(args.source)
        packaged = {"provenance": {
            "repository": REPO, "commit": args.commit, "checked": args.checked,
            "source_path": "data/videos.json", "license": "MIT; see opus-gallery-LICENSE.txt",
            "tech_tags_scope": "Skillry remake, not verified original implementation",
            "added_scope": "Catalogue addition date, not original publication date",
            "prompt_scope": "Public shared text; false prompt_partial does not prove the full creation session",
            "media_scope": "Media and original posts are separate sources; no media licence granted here",
        }, "entries": entries}
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(packaged, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        emit({"entries": len(entries), "saved": str(args.out), "commit": args.commit})
        return
    entries, provenance = load(args.data)
    if args.command == "stats":
        emit({"provenance": provenance, "entries": len(entries),
              "categories": dict(Counter(x["category"] for x in entries)),
              "remake_tech_tags": dict(Counter(t for x in entries for t in x["tech_tags"])),
              "partial_prompts": sum(x["prompt_partial"] for x in entries),
              "unique_exact_prompts": len({x["prompt"] for x in entries}),
              "added_dates": dict(Counter(x["added"] for x in entries))})
        return
    if not 1 <= args.limit <= 20:
        parser.error("--limit must be between 1 and 20")
    if args.prompt and args.limit > 3 and not args.slug:
        parser.error("Full prompt output requires --slug or --limit 1..3")
    tokens = args.query.casefold().split()
    found = []
    for x in entries:
        haystack = " ".join([x["slug"], x["author"], x["prompt"], *x["tech_tags"]]).casefold()
        if args.slug and x["slug"] != args.slug:
            continue
        if args.category and x["category"] != args.category:
            continue
        if args.complete and x["prompt_partial"]:
            continue
        if not all(t.casefold() in [tag.casefold() for tag in x["tech_tags"]] for t in args.tag):
            continue
        if not all(token in haystack for token in tokens):
            continue
        if args.mechanism and not re.search(MECHANISMS[args.mechanism], x["prompt"], re.I):
            continue
        found.append(x)
    found.sort(key=lambda x: (x["prompt_partial"], -sum(x["prompt"].casefold().count(t) for t in tokens), x["slug"]))
    results = []
    for x in found[:args.limit]:
        results.append({"slug": x["slug"], "category": x["category"], "remake_tech_tags": x["tech_tags"],
                        "prompt_partial": x["prompt_partial"], "original_post": x["post_url"],
                        "view_original_and_remake": x["skillry_url"],
                        "prompt_file": f"{REPO}/blob/{provenance.get('commit') or 'main'}/prompts/{x['slug']}.md",
                        "mechanism_hints": [k for k, p in MECHANISMS.items() if re.search(p, x["prompt"], re.I)],
                        "prompt" if args.prompt else "prompt_excerpt": x["prompt"] if args.prompt else re.sub(r"\s+", " ", x["prompt"])[:280]})
    emit({"provenance": provenance, "matches": len(found), "returned": len(results),
          "hint_scope": "Keyword candidates, not visual-quality or original-source verification", "results": results})


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as e:
        print(f"Catalogue error: {e}", file=sys.stderr)
        sys.exit(1)
