"""Build fresh archives from source and compiled binaries, excluding caches."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


root = Path(__file__).resolve().parents[1]
output = root / "b32_assets"
output.mkdir(exist_ok=True)
native = ["b32_tts.dll", "b32_wrapper.dll", "b32_helper.exe"]
notices = ["LICENSE", "deps.txt"]


def write_archive(name, entries):
    with ZipFile(output / name, "w", ZIP_DEFLATED) as archive:
        for source, destination in sorted(entries, key=lambda entry: entry[1]):
            archive.writestr(destination, source.read_bytes())


addon = root / "nvda"
entries = [
    (path, path.relative_to(addon).as_posix())
    for path in addon.rglob("*")
    if path.is_file()
    and path.relative_to(addon).as_posix() not in notices
    and "__pycache__" not in path.parts
    and path.suffix not in {".pyc", ".pyo", ".dll", ".exe"}
]
entries.extend((root / "bin" / name, "synthDrivers/" + name) for name in native)
entries.extend((root / name, name) for name in notices)
write_archive("bestspeech.nvda-addon", entries)
write_archive(
    "b32_bin.zip",
    [(root / "bin" / name, name) for name in native + ["b32_spk.exe"]]
    + [(root / name, name) for name in notices],
)
