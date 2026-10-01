#!/usr/bin/env python3
"""Validate source links, transcription sections, and rajah crops for batches 41–60.

Default mode is strict and exits non-zero until the requested edition is genuinely
complete. `--structure-only` checks document/page coverage and available source
links, but is not an acceptance check for a completed translation.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "terjemahan"
ASSETS = TRANSLATIONS / "assets"
RAJAH = ROOT / "rajah"
EXPECTED_CROPS = 57

BATCHES: list[tuple[int, int, int]] = [
    *((batch, 200 + (batch - 41) * 5, 204 + (batch - 41) * 5) for batch in range(41, 59)),
    (59, 290, 292),
    (60, 293, 297),
]

VERIFIED_CROPS = {
    201: "rajah-hal-201-01.png",
    215: "rajah-hal-215-01.png",
    248: "rajah-hal-248-01.png",
}
MISSING_SOURCE_PAGES = {210, 211}
BLACK_BOX_GLYPHS = {"\u25a0", "\u25fc", "\u2588"}
PENDING_MARKERS = (
    "belum ditransliterasi",
    "belum diterjemahkan",
    "belum diinventarisasi",
    "belum dikerjakan",
    "belum lengkap",
    "[todo]",
    "tulis latin disini",
    "tulis terjemah disini",
)
PAGE_HEADING = re.compile(r"(?m)^## Hal\s+(\d{3})\b[^\n]*$")


def filename_for(batch: int, start: int, end: int) -> Path:
    return TRANSLATIONS / f"BATCH-{batch}-Hal-{start:03d}-{end:03d}.md"


def source_picture(page: int) -> int | None:
    """Return the verified scan number for this printed page, if present."""
    if 200 <= page <= 209:
        return 102 + (page - 200) // 2
    if 212 <= page <= 297:
        return 107 + (page - 212) // 2
    return None


def parse_corner(pixel: str) -> list[float]:
    values = re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", pixel)
    return [float(value) for value in values]


def inspect_crop(path: Path, identify: str) -> list[str]:
    issues: list[str] = []
    fmt = (
        "%x|%y|%U|%[pixel:p{0,0}]|%[pixel:p{w-1,0}]|"
        "%[pixel:p{0,h-1}]|%[pixel:p{w-1,h-1}]"
    )
    result = subprocess.run(
        [identify, "-format", fmt, str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return [f"{path.relative_to(ROOT)}: ImageMagick identify failed: {result.stderr.strip()}"]

    fields = result.stdout.split("|")
    if len(fields) != 7:
        return [f"{path.relative_to(ROOT)}: could not read DPI/corner metadata"]
    try:
        x_density = float(fields[0])
        y_density = float(fields[1])
    except ValueError:
        return [f"{path.relative_to(ROOT)}: invalid density metadata"]

    units = fields[2].lower()
    if "centimeter" in units:
        x_dpi, y_dpi = x_density * 2.54, y_density * 2.54
    elif "inch" in units:
        x_dpi, y_dpi = x_density, y_density
    else:
        issues.append(f"{path.relative_to(ROOT)}: density has no inch/cm unit ({fields[2]})")
        x_dpi = y_dpi = 0.0
    if abs(x_dpi - 300) > 1 or abs(y_dpi - 300) > 1:
        issues.append(
            f"{path.relative_to(ROOT)}: expected 300 DPI, got {x_dpi:.1f}×{y_dpi:.1f} DPI"
        )

    for corner, pixel in zip(("top-left", "top-right", "bottom-left", "bottom-right"), fields[3:]):
        channels = parse_corner(pixel)
        if not channels or min(channels[:3]) < 245:
            issues.append(f"{path.relative_to(ROOT)}: {corner} background is not white ({pixel})")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help="check batch/page/source structure only; does not certify translation or crops",
    )
    args = parser.parse_args()

    structural_errors: list[str] = []
    completeness_errors: list[str] = []
    warnings: list[str] = []
    expected_pages: list[int] = []
    linked_pages: set[int] = set()
    page_headings_seen: list[int] = []
    incomplete_text_pages: set[int] = set()
    unreviewed_rajah_pages: set[int] = set()
    marker_files: list[str] = []

    for batch, start, end in BATCHES:
        path = filename_for(batch, start, end)
        expected_pages.extend(range(start, end + 1))
        if not path.is_file():
            structural_errors.append(f"missing batch file: {path.relative_to(ROOT)}")
            continue

        text = path.read_text(encoding="utf-8")
        if f"BATCH-{batch:02d}" not in text:
            structural_errors.append(f"{path.relative_to(ROOT)}: batch heading does not match filename")

        headings = list(PAGE_HEADING.finditer(text))
        actual_pages = [int(match.group(1)) for match in headings]
        page_headings_seen.extend(actual_pages)
        expected_batch_pages = list(range(start, end + 1))
        if actual_pages != expected_batch_pages:
            structural_errors.append(
                f"{path.relative_to(ROOT)}: page sections {actual_pages} do not match {expected_batch_pages}"
            )

        for index, match in enumerate(headings):
            page = int(match.group(1))
            block_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            block = text[match.start():block_end]
            for required_heading in (
                "### Arab Gundul (Scan Asli):",
                "### Latin Arab:",
                "### Terjemah Pesantren:",
                "### Rajah:",
            ):
                if required_heading not in block:
                    structural_errors.append(
                        f"{path.relative_to(ROOT)} page {page}: missing section {required_heading}"
                    )

            picture = source_picture(page)
            if picture is None:
                if page not in MISSING_SOURCE_PAGES:
                    structural_errors.append(f"page {page}: no source mapping is defined")
                if "tidak ada scan" not in block.lower() and "tidak ditemukan" not in block.lower():
                    structural_errors.append(f"page {page}: missing scan is not disclosed in the page section")
                if "assets/Picture%20" in block:
                    structural_errors.append(f"page {page}: links a scan despite having no matching source")
            else:
                link = f"assets/Picture%20{picture}.jpg"
                source_file = ASSETS / f"Picture {picture}.jpg"
                if link not in block:
                    structural_errors.append(f"page {page}: missing source link {link}")
                elif not source_file.is_file():
                    structural_errors.append(f"page {page}: source asset is absent: {source_file.relative_to(ROOT)}")
                else:
                    linked_pages.add(page)

            lower_block = block.lower()
            if any(marker in lower_block for marker in PENDING_MARKERS):
                incomplete_text_pages.add(page)
            if "belum diinventarisasi" in lower_block:
                unreviewed_rajah_pages.add(page)

            crop = VERIFIED_CROPS.get(page)
            if crop and crop not in block:
                structural_errors.append(f"page {page}: verified crop is not linked: {crop}")

        if any(glyph in text for glyph in BLACK_BOX_GLYPHS):
            marker_files.append(str(path.relative_to(ROOT)))

    # The old final filenames overlapped pages 293–294; they must not remain beside
    # the explicit 290–292 / 293–297 ranges.
    for stale in (
        TRANSLATIONS / "BATCH-59-Hal-290-294.md",
        TRANSLATIONS / "BATCH-60-Hal-295-297.md",
    ):
        if stale.exists():
            structural_errors.append(f"stale overlapping range remains: {stale.relative_to(ROOT)}")

    all_pages = sorted(page_headings_seen)
    expected_sorted = list(range(200, 298))
    if all_pages != expected_sorted:
        structural_errors.append("combined page headings do not cover pages 200–297 exactly once")

    crops = sorted(
        path for path in RAJAH.iterdir()
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    ) if RAJAH.is_dir() else []
    if len(crops) != EXPECTED_CROPS:
        completeness_errors.append(f"rajah crop count is {len(crops)}/{EXPECTED_CROPS}")

    image_issues: list[str] = []
    identify = shutil.which("identify")
    if crops and not identify:
        image_issues.append("ImageMagick `identify` is required to verify crop DPI and white corners")
    elif identify:
        for crop in crops:
            image_issues.extend(inspect_crop(crop, identify))

    missing_pages = sorted(MISSING_SOURCE_PAGES)
    if missing_pages:
        completeness_errors.append(
            "source scans are missing for printed pages " + ", ".join(map(str, missing_pages))
        )
    if incomplete_text_pages:
        completeness_errors.append(
            f"Arabic/transliteration/translation still pending on {len(incomplete_text_pages)} pages"
        )
    if unreviewed_rajah_pages:
        completeness_errors.append(
            f"rajah inventory remains unreviewed on {len(unreviewed_rajah_pages)} pages"
        )
    if marker_files:
        completeness_errors.append("black-box glyph(s) found in: " + ", ".join(marker_files))
    if image_issues:
        completeness_errors.extend(image_issues)

    print("Batch 41–60 validation")
    print(f"  Batch documents: {sum(filename_for(*item).is_file() for item in BATCHES)}/20")
    print(f"  Page headings:   {len(set(page_headings_seen))}/98 unique")
    print(f"  Scan links:      {len(linked_pages)}/98 pages ({len(MISSING_SOURCE_PAGES)} source pages absent)")
    print(f"  Text complete:   {98 - len(incomplete_text_pages)}/98 pages")
    print(f"  Rajah crops:     {len(crops)}/{EXPECTED_CROPS}")
    if identify and crops:
        print(f"  Crop checks:     {len(crops) - sum(1 for issue in image_issues if issue.startswith('rajah/'))}/{len(crops)} passed DPI/corner checks")
    print(f"  Black-box glyphs: {'found' if marker_files else 'none in batch Markdown'}")

    if structural_errors:
        print("\nSTRUCTURE ERRORS:")
        for error in structural_errors:
            print(f"  - {error}")
    if completeness_errors:
        print("\nCOMPLETENESS BLOCKERS:")
        for error in completeness_errors:
            print(f"  - {error}")

    if args.structure_only:
        if structural_errors:
            print("\nRESULT: FAIL (structure/source links need repair)")
            return 1
        print("\nRESULT: PASS — structure only; this is NOT a completed-content acceptance.")
        return 0

    if structural_errors or completeness_errors:
        print("\nRESULT: FAIL — do not report Batch 41–60 as complete.")
        return 1
    print("\nRESULT: PASS — all strict checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
