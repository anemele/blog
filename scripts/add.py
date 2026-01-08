#!/usr/bin/python3
"""Add new post."""

import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from textwrap import dedent
from zoneinfo import ZoneInfo


@dataclass
class Config:
    edit: bool = False


def interactive_add(config: Config):
    post_name = input("post name: ").strip()
    if post_name == "":
        print("abort.")
        return

    this_path = Path(__file__).parent.parent
    zone = ZoneInfo("Asia/Shanghai")
    now = datetime.now(zone)
    target_path = this_path / "content/post" / now.strftime("%Y/%m")
    # print(target_path)

    if post_name.endswith("/"):
        post_path = target_path / post_name
        if post_path.parent != target_path:
            print("invalid post name!")
            return
        post_name = "index.md"
    else:
        post_path = target_path
        if not post_name.endswith(".md"):
            post_name = f"{post_name}.md"

    post_path.mkdir(parents=True, exist_ok=True)
    post_path = post_path / post_name
    if post_path.exists():
        confirm = input("this post exists. overwrite? (y/N)").strip()
        if confirm.lower() != "y":
            print("abort.")
            return

    # now = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    now = now.replace(microsecond=0).isoformat()
    title_tmpl = dedent(f"""\
    ---
    title:
    description:
    date: {now}
    lastmod: {now}
    draft: true
    tags:
    -
    categories:
    ---
    \n
    """)

    rel_path = post_path.relative_to(this_path)

    try:
        post_path.write_text(title_tmpl)
    except OSError as e:
        print(e)

    if not config.edit:
        print(f"edit file: {rel_path}")
        return

    editor = os.getenv("EDITOR", default="nvim")
    try:
        subprocess.run([editor, str(post_path)])
    except OSError as e:
        print(e)
        print(f"cannot open post, edit it manually: {rel_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--edit", action="store_true")

    args = parser.parse_args()

    interactive_add(
        config=Config(
            edit=args.edit,
        )
    )


if __name__ == "__main__":
    main()
