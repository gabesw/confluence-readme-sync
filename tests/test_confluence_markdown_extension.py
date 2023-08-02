import unittest
from src.confluence_markdown_extension import *
from unittest.mock import patch

class TestSectionLinkPreprocessor(unittest.TestCase):
    def test_run(self):
        lines: list[str] = [
            " - [How to debug](##How-to-debug)",
            "  - [Deploy the app](###header3)",
            "- [Header](#header1)"
        ]
        processed_lines = SectionLinkPreprocessor().run(lines)
        self.assertEqual(processed_lines, [
            " - [How to debug](#How-to-debug)",
            "  - [Deploy the app](#header3)",
            "- [Header](#header1)"
        ])

class TestCodeLanguagePreprocessor(unittest.TestCase):
    def setUp(self):
        self.preprocessor = CodeLanguagePreprocessor()
    def test_run_with_bash(self):
        lines: list[str] = [
            "```bash",
            "ping github.com/gabesw",
            "```"
        ]
        processed_lines = self.preprocessor.run(lines)
        self.assertEqual(processed_lines, [
            "```$$$$$shell$$$$$",
            "ping github.com/gabesw",
            "```"
        ])
    def test_run_with_python(self):
        lines: list[str] = [
            "```python",
            "print('github.com/gabesw')",
            "```"
        ]
        processed_lines = self.preprocessor.run(lines)
        self.assertEqual(processed_lines, [
            "```$$$$$python$$$$$",
            "print('github.com/gabesw')",
            "```"
        ])

class TestCodeBlockPostprocessor(unittest.TestCase):
    def setUp(self):
        self.postprocessor = CodeBlockPostprocessor()
    def test_run(self):
        text = "<p><code>$$$$$shell$$$$$\nping github.com/gabesw</code></p>"
        processed_text = self.postprocessor.run(text)
        self.assertEqual(processed_text, "<ac:structured-macro ac:name=\"code\"><ac:parameter ac:name=\"language\">shell</ac:parameter><ac:plain-text-body><![CDATA[ping github.com/gabesw]]></ac:plain-text-body></ac:structured-macro>")

class TestConfluenceExtension(unittest.TestCase):
    def test_extend_markdown(self):
        md = Markdown()
        confluence_extension = ConfluenceExtension()
        confluence_extension.extendMarkdown(md)
        self.assertTrue(confluence_extension in md.registeredExtensions, "Extension is registered")
        self.assertTrue('confluence_section_links' in md.preprocessors, "Section links preprocessor is registered")
        self.assertTrue('confluence_code_language' in md.preprocessors, "Code language preprocessor is registered")
        self.assertTrue('confluence_code_block' in md.postprocessors, "Code block postprocessor is registered")

class TestMakeExtension(unittest.TestCase):
    def test_make_extension(self):
        extension = makeExtension()
        self.assertIsInstance(extension, ConfluenceExtension)