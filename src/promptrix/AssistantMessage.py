from typing import Optional
import promptrix.TemplateSection as TemplateSection

class AssistantMessage(TemplateSection.TemplateSection):
    """
    A message sent by the assistant.
    """
    def __init__(self, template: str, tokens: Optional[int] = -1, assistant_prefix: Optional[str] = 'assistant: '):
        """
        Creates a new 'AssistantMessage' instance.
        :param template: Template to use for this section.
        :param tokens: Optional. Sizing strategy for this section. Defaults to `auto`.
        :param assistant_prefix: Optional. Prefix to use for assistant messages when rendering as text. Defaults to `assistant: `.
        """
        super().__init__(template, assistant_prefix, tokens, True, '\n', text_prefix=assistant_prefix)

