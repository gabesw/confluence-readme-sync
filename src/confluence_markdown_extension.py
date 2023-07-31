import re
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension

class SectionLinkPreprocessor(Preprocessor):
    def run(self, lines):
        modified_lines = []
        for line in lines:
            # replace links to sections on the page with one hashtag instead of multiple to work in confluence urls
            modified_lines.append(re.sub(r'\]\(#+', r'](#', line, flags=re.DOTALL))
        return modified_lines
    
class CodeLanguagePreprocessor(Preprocessor):
    def run(self, lines):
        modified_lines = []
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
    def run(self, text):
        # replace code blocks with confluence code blocks
        processed_text = re.sub(
            r'<p><code>\$\$\$\$\$(\w+)\$\$\$\$\$\n?(.*?)</code></p>', 
            r'<ac:structured-macro ac:name="code"><ac:parameter ac:name="language">\1</ac:parameter><ac:plain-text-body><![CDATA[\2]]></ac:plain-text-body></ac:structured-macro>', 
            text,
            flags=re.DOTALL
        )
        return processed_text

class ConfluenceExtension(Extension):
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(SectionLinkPreprocessor(md), 'confluence_section_links', 0)
        md.preprocessors.register(CodeLanguagePreprocessor(md), 'confluence_section_links', 0)
        md.postprocessors.register(CodeBlockPostprocessor(md), 'confluence_code_block', 0)

def makeExtension(*args, **kwargs):
    return ConfluenceExtension(*args, **kwargs)
