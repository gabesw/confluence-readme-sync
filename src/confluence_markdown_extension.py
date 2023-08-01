"""
An extension for the `python-markdown <https://pypi.org/project/Markdown/>`_ package that formats certain elements for Confluence
pages in a nicer way than pure markdown.
"""

import re
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension
from markdown import Markdown

class SectionLinkPreprocessor(Preprocessor):
    """
    A preprocessor that removes extra hashtags before section links.
    """
    def run(self, lines: list[str]) -> list[str]:
        """
        Removes extra hashtags before section links such that they have only one hashtag.
        """
        modified_lines: list[str] = []
        for line in lines:
            # replace links to sections on the page with one hashtag instead of multiple to work in confluence urls
            modified_lines.append(re.sub(r'\]\(#+', r'](#', line, flags=re.DOTALL))
        return modified_lines
    
class CodeLanguagePreprocessor(Preprocessor):
    """
    A preprocessor that enables Confluence to receive the language of code blocks.
    """
    def run(self, lines: list[str]) -> list[str]:
        """
        First, wraps the language part of markdown code blocks to be grabbed by the :ref:`CodeBlockPostprocessor`. Then maps
        the language to a supported Confluence code snippet language, if available.
        """
        modified_lines: list[str] = []
        for line in lines:
            #replace language in codeblock with special language tag to be grabbed by the CodeBlockPostprocessor
            modified_line = re.sub(r'```(\w+)', r'```$$$$$\1$$$$$', line, flags=re.DOTALL)

            #the next line changes bash to shell to comply with the supported code snippet languages in confluence
            if modified_line != line: #line was changed
                modified_line = re.sub(r'bash', r'shell', modified_line, flags=re.DOTALL)
                #TODO: add replacements for other languages
            modified_lines.append(modified_line)
        return modified_lines

class CodeBlockPostprocessor(Postprocessor):
    """
    A postprocessor that reformats HTML code blocks to Confluence code snippet macros.
    """
    def run(self, text: str) -> str:
        """
        Replaces HTML code blocks with Confluence code snippet macros with language support.
        """
        # replace code blocks with confluence code blocks using the code snippets macro format
        processed_text = re.sub(
            r'<p><code>\$\$\$\$\$(\w+)\$\$\$\$\$\n?(.*?)</code></p>', 
            r'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">\1</ac:parameter><ac:plain-text-body><![CDATA[\2]]></ac:plain-text-body></ac:structured-macro>', 
            text,
            flags=re.DOTALL
        )
        return processed_text

class ConfluenceExtension(Extension):
    """
    The extension to be included in the `extensions` argument of the :ref:`Markdown.markdown` function.
    """
    def extendMarkdown(self, md: Markdown):
        md.registerExtension(self)
        md.preprocessors.register(SectionLinkPreprocessor(md), 'confluence_section_links', 0)
        md.preprocessors.register(CodeLanguagePreprocessor(md), 'confluence_section_links', 0)
        md.postprocessors.register(CodeBlockPostprocessor(md), 'confluence_code_block', 0)

def makeExtension(*args, **kwargs):
    return ConfluenceExtension(*args, **kwargs)
