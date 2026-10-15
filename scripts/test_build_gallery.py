import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load_script("build-gallery")
watcher = load_script("watch-gallery")


class SpecialGalleryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.root_patch = patch.object(builder, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.temporary.cleanup)
        self.addCleanup(self.root_patch.stop)

    def write(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_no_works_hides_special_tab(self):
        self.assertIsNone(builder.scan_special_gallery(None))
        self.write("special/empty/content.txt", "title: Empty")
        self.assertIsNone(builder.scan_special_gallery(None))

    def test_cover_required(self):
        self.write("special/no-cover/left.jpg")
        self.assertIsNone(builder.scan_special_gallery(None))

    def test_views_metadata_and_story(self):
        for name in ("side.WEBP", "LEFT.jpg", "front.PNG", "right.jpeg"):
            self.write(f"special/ch2-special01/{name}")
        self.write(
            "special/ch2-special01/content.txt",
            'title: A "special" traveler\nchapter: Chapter 2\n---\nFirst line.\n\nLast line.',
        )
        gallery = builder.scan_special_gallery(None)
        self.assertEqual((gallery["id"], gallery["label"]), ("special", "Special"))
        work = gallery["works"][0]
        self.assertEqual(work["images"], [
            f"special/ch2-special01/{name}"
            for name in ("front.PNG", "right.jpeg", "LEFT.jpg", "side.WEBP")
        ])
        self.assertEqual(work["tag"], "Special 01")
        self.assertEqual(work["title"], 'A "special" traveler')
        self.assertEqual(work["context"], "Chapter 2 · Special")
        self.assertEqual(work["note"], "First line.\n\nLast line.")
        self.assertIn('title: "A \\"special\\" traveler"', builder.render([gallery], None))

    def test_missing_metadata_uses_folder_name(self):
        self.write("special/untitled/front.jpg")
        work = builder.scan_special_gallery(None)["works"][0]
        self.assertEqual(work["tag"], "Special 01")
        self.assertEqual(work["title"], "untitled")
        self.assertEqual(work["context"], "Special")
        self.assertEqual(work["note"], "")
        self.assertEqual(work["images"], ["special/untitled/front.jpg"])

    def test_multiple_chapters_and_companion_share_tab(self):
        for folder, chapter in (("ch3-special01", "Chapter 3"), ("ch2-special01", "Chapter 2")):
            self.write(f"special/{folder}/front.jpg")
            self.write(f"special/{folder}/content.txt", f"title: Special 01\nchapter: {chapter}\n---")
        self.write("companion/companion.jpg")
        self.write("companion/companion_img.jpg")
        self.write("companion/companion.txt", "A shared story.")
        companion = builder.scan_companion()
        works = builder.scan_special_gallery(companion)["works"]
        self.assertEqual([work["context"] for work in works], [
            "Chapter 1 · Special · Not for sale", "Chapter 2 · Special", "Chapter 3 · Special",
        ])
        self.assertEqual([work["tag"] for work in works], ["Special 01", "Special 02", "Special 03"])
        self.assertEqual(works[0]["title"], "Companion Feely")
        self.assertEqual(works[0]["images"], [companion["file"], companion["img"]])
        self.assertEqual(works[0]["note"], companion["note"])

    def test_companion_only_and_single_photo(self):
        for filename in ("companion.jpg", "companion_img.jpg"):
            with self.subTest(filename=filename):
                photo = self.write(f"companion/{filename}")
                companion = builder.scan_companion()
                works = builder.scan_special_gallery(companion)["works"]
                self.assertEqual(len(works), 1)
                self.assertEqual(works[0]["images"], [f"companion/{filename}"])
                self.assertEqual(works[0]["tag"], "Special 01")
                self.assertEqual(works[0]["title"], "Companion Feely")
                self.assertEqual(works[0]["context"], "Chapter 1 · Special · Not for sale")
                photo.unlink()

    def test_cdn_applies_to_special_and_companion(self):
        self.write("special/test/front.jpg")
        self.write("companion/companion.jpg")
        with patch.object(builder, "CDN_BASE_URL", "https://example.com/art/"):
            works = builder.scan_special_gallery(builder.scan_companion())["works"]
        self.assertEqual(works[0]["file"], "https://example.com/art/companion/companion.jpg")
        self.assertEqual(works[1]["file"], "https://example.com/art/special/test/front.jpg")

    def test_watcher_tracks_special_changes(self):
        photo = self.write("special/test/front.jpg")
        with patch.object(watcher, "ROOT", self.root):
            before = watcher.snapshot()
            note = self.write("special/test/content.txt", "title: Test")
            after = watcher.snapshot()
            self.assertNotEqual(before, after)
            self.assertIn(str(photo.relative_to(self.root)), after)
            self.assertIn(str(note.relative_to(self.root)), after)
            photo.unlink()
            self.assertNotEqual(after, watcher.snapshot())


if __name__ == "__main__":
    unittest.main()
