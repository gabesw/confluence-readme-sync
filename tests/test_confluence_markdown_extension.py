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
class TestCodeBlockPostprocessor(unittest.TestCase):
    def setUp(self):
        self.postprocessor = CodeBlockPostprocessor()
    def test_run(self):
        text = "<pre><code class=\"language-shell\">ping github.com/gabesw</code></pre>"
        processed_text = self.postprocessor.run(text)
        self.assertEqual(processed_text, "<ac:structured-macro ac:name=\"code\"><ac:parameter ac:name=\"language\">shell</ac:parameter><ac:plain-text-body><![CDATA[ping github.com/gabesw]]></ac:plain-text-body></ac:structured-macro>")

class TestConfluenceExtension(unittest.TestCase):
    def test_extend_markdown(self):
        md = Markdown()
        confluence_extension = ConfluenceExtension()
        confluence_extension.extendMarkdown(md)
        self.assertTrue(confluence_extension in md.registeredExtensions, "Extension is registered")
        self.assertTrue('confluence_section_links' in md.preprocessors, "Section links preprocessor is registered")
        self.assertTrue('confluence_code_block' in md.postprocessors, "Code block postprocessor is registered")

class TestMakeExtension(unittest.TestCase):
    def test_make_extension(self):
        extension = makeExtension()
        self.assertIsInstance(extension, ConfluenceExtension)