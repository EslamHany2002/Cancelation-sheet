import re
import importlib.metadata

# اسم الملف اللي فيه الكود
file_path = "dashboard.py"

# استخراج المكتبات من import
libraries = set()
with open(file_path, "r") as f:
    for line in f:
        match = re.match(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", line)
        if match:
            libraries.add(match.group(1))

# نكتب المكتبات مع الإصدار
with open("requirements.txt", "w") as req_file:
    for lib in sorted(libraries):
        try:
            version = importlib.metadata.version(lib)
            req_file.write(f"{lib}=={version}\n")
        except importlib.metadata.PackageNotFoundError:
            # لو المكتبة مش متسطبة
            req_file.write(f"{lib}\n")
