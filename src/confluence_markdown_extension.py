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

class CodeBlockPostprocessor(Postprocessor):
    """
    A postprocessor that reformats HTML code blocks to Confluence code snippet macros.
    """
    def run(self, text: str) -> str:
        """
        Replaces HTML code blocks with Confluence code snippet macros with language support.
        """
        # replace code blocks with confluence code blocks using the code snippets macro format
        #TODO: add if statement to check for the language tag and if it doesnt exist set language to none
        processed_text = re.sub(
            r'<pre><code class="language-(\w+)">(.*?)\n?</code></pre>', 
            r'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">\1</ac:parameter><ac:plain-text-body><![CDATA[\2]]></ac:plain-text-body></ac:structured-macro>', 
            text,
            flags=re.DOTALL
        )
        #map certain languages to supported confluence languages
        if processed_text != text: #text was changed
            #<ac:parameter ac:name="language">\1</ac:parameter>
            processed_text = re.sub(
                r'<ac:parameter ac:name="language">bash</ac:parameter>', 
                r'<ac:parameter ac:name="language">shell</ac:parameter>', 
                processed_text,
                flags=re.DOTALL
            )
        return processed_text

class ConfluenceExtension(Extension):
    """
    The extension to be included in the `extensions` argument of the :ref:`Markdown.markdown` function.
    """
    def extendMarkdown(self, md: Markdown):
        """
        Adds the processors to the extension.
        """
        md.registerExtension(self)
        md.preprocessors.register(SectionLinkPreprocessor(md), 'confluence_section_links', 0)
        md.postprocessors.register(CodeBlockPostprocessor(md), 'confluence_code_block', 0)

def makeExtension(*args, **kwargs):
    """
    Initializes the Confluence extension.
    """
    return ConfluenceExtension(*args, **kwargs)
