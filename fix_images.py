# fix_images.py — batch convert images in ./faces to true RGB JPEG
from pathlib import Path
from PIL import Image

# Optional HEIC support; won't crash if missing
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:
    pass

faces = Path(__file__).parent / "faces"
faces.mkdir(exist_ok=True)

for p in faces.iterdir():
    if p.suffix.lower() not in {".jpg", ".jpeg", ".png", ".heic", ".webp"}:
        continue
    try:
        with Image.open(p) as im:
            im = im.convert("RGB")  # force 8-bit RGB
            out = p.with_suffix(".jpg")  # save as real JPEG
            im.save(out, "JPEG", quality=95)
            if out != p and p.suffix.lower() != ".jpg":
                print(f"[converted] {p.name} -> {out.name}")
    except Exception as e:
        print(f"[skip] {p.name}: {e}")
