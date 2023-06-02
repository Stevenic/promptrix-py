from promptrix.TemplateSection import TemplateSection

class SystemMessage(TemplateSection):
    """
    A system message.
    """
    def __init__(self, template: str, tokens: int = -1):
        """
        Creates a new 'SystemMessage' instance.
        :param template: Template to use for this section.
        :param tokens: Optional. Sizing strategy for this section. Defaults to `auto`.
        """
        super().__init__(template, 'system', tokens, True, '\n', '')
