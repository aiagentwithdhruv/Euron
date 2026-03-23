"""Tests for security module — filename sanitization."""

from app.security import safe_filename


class TestSafeFilename:
    def test_normal_filename(self):
        assert safe_filename("report.pdf") == "report.pdf"

    def test_path_traversal_unix(self):
        result = safe_filename("../../etc/passwd")
        assert "/" not in result
        assert ".." not in result

    def test_path_traversal_windows(self):
        result = safe_filename("..\\..\\windows\\system32\\config")
        assert "\\" not in result

    def test_special_characters(self):
        result = safe_filename("; rm -rf /.mp4")
        assert ";" not in result
        assert result.endswith(".mp4") or result.startswith("upload_")

    def test_empty_string(self):
        result = safe_filename("")
        assert result.startswith("upload_")
        assert len(result) > 0

    def test_dot_file(self):
        result = safe_filename(".hidden")
        assert result.startswith("upload_")

    def test_long_filename(self):
        result = safe_filename("a" * 300 + ".pdf")
        assert len(result) <= 204  # 200 + .pdf

    def test_preserves_extension(self):
        result = safe_filename("my document (2).pdf")
        assert result.endswith(".pdf")

    def test_unicode_characters(self):
        result = safe_filename("日本語ファイル.pdf")
        assert len(result) > 0
