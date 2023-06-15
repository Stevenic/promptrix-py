from promptrix.TemplateSection import TemplateSection

class UserMessage(TemplateSection):
    """
    A user message.
    """
    def __init__(self, template: str, tokens: int = -1, user_prefix: str = 'user'):
        """
        Creates a new 'UserMessage' instance.
        :param template: Template to use for this section.
        :param tokens: Optional. Sizing strategy for this section. Defaults to `auto`.
        :param user_prefix: Optional. Prefix to use for user messages when rendering as text. Defaults to `user`.
        """
        super().__init__(template, user_prefix, tokens, True, '\n', text_prefix = user_prefix)
