import sys

filepath = "tools/heartbeat.py"
with open(filepath, "r") as f:
    content = f.read()

old_code = 'src_path = Path(f"lab/{personas[0]}/published/{paper_name}")'
new_code = 'src_path = Path(f"lab/{author}/published/{paper_name}")'

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(filepath, "w") as f:
        f.write(content)
    print("Patched heartbeat.py successfully.")
else:
    print("Could not find the target code.")
