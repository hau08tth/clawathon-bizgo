"""BizGro Multi-Agent Orchestrator"""
from .content_agent import ContentAgent
from .network_agent import NetworkAgent
from .idea_agent import IdeaAgent


class BizGroOrchestrator:
    """Routes tasks to the appropriate specialized agent."""

    def __init__(self):
        self._content_agent: ContentAgent | None = None
        self._network_agent: NetworkAgent | None = None
        self._idea_agent: IdeaAgent | None = None

    @property
    def content(self) -> ContentAgent:
        if not self._content_agent:
            self._content_agent = ContentAgent()
        return self._content_agent

    @property
    def network(self) -> NetworkAgent:
        if not self._network_agent:
            self._network_agent = NetworkAgent()
        return self._network_agent

    @property
    def idea(self) -> IdeaAgent:
        if not self._idea_agent:
            self._idea_agent = IdeaAgent()
        return self._idea_agent

    async def generate_content(self, **kwargs) -> dict:
        return await self.content.generate(**kwargs)

    async def match_network(self, **kwargs) -> dict:
        return await self.network.match_and_generate(**kwargs)

    async def process_idea(self, **kwargs) -> dict:
        return await self.idea.enhance_and_evaluate(**kwargs)


orchestrator = BizGroOrchestrator()
