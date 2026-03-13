import re
with open("tools/heartbeat.py", "r") as f:
    code = f.read()

search = """            dest_path = published_dir / paper_name
            if not dest_path.exists():
                src_path = Path(f"lab/{author}/published/{paper_name}")
                print(f"  Graduating {paper_name} (co-signed by {', '.join(personas)})")
                shutil.copy2(src_path, dest_path)

                # Record graduation in STATE.md
                state_file = Path("lab/STATE.md")
                if state_file.exists():
                    content = state_file.read_text(encoding="utf-8")
                    if "## Graduated Papers" not in content:
                        content += "\\n## Graduated Papers\\n"

                    # Prevent duplicate entries
                    if f"- {paper_name}" not in content:
                        content += f"- {paper_name} (Co-signed by: {', '.join(personas)})\\n"
                        state_file.write_text(content, encoding="utf-8")

                # Track file for git commit
                subprocess.run(["git", "add", str(dest_path)], check=False)
                subprocess.run(["git", "add", str(state_file)], check=False)
                graduated_count += 1"""

replace = """            dest_path = published_dir / paper_name
            if not dest_path.exists():
                src_path = Path(f"lab/{author}/published/{paper_name}")
                print(f"  Graduating {paper_name} (co-signed by {', '.join(personas)})")
                shutil.copy2(src_path, dest_path)
                subprocess.run(["git", "add", str(dest_path)], check=False)

            # Record graduation in STATE.md
            state_file = Path("lab/STATE.md")
            if state_file.exists():
                content = state_file.read_text(encoding="utf-8")
                if "## Graduated Papers" not in content:
                    content += "\\n## Graduated Papers\\n"

                # Prevent duplicate entries
                if f"- {paper_name}" not in content:
                    content += f"- {paper_name} (Co-signed by: {', '.join(personas)})\\n"
                    state_file.write_text(content, encoding="utf-8")
                    subprocess.run(["git", "add", str(state_file)], check=False)
                    graduated_count += 1"""

code = code.replace(search, replace)
with open("tools/heartbeat.py", "w") as f:
    f.write(code)
