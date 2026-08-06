from pathlib import Path
import mkdocs_gen_files

root = Path(__file__).resolve().parents[1]
package_dir = root / "aiorocket2"

pages = {
    "api/index.md": "# API reference\n\nAuto-generated reference for aiorocket2.\n",
    "api/client.md": "::: aiorocket2.client\n",
    "api/models.md": "::: aiorocket2.models\n",
    "api/enums.md": "::: aiorocket2.enums\n",
    "api/exceptions.md": "::: aiorocket2.exceptions\n",
    "api/utils.md": "::: aiorocket2.utils\n",
    "api/tags.md": "::: aiorocket2.tags\n",
}

for path, content in pages.items():
    with mkdocs_gen_files.open(path, "w") as f:
        f.write(content)
