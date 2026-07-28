from app.llm.llm_factory import LLMFactory


class BidEvaluationAgent:

    def __init__(self):

        self.llm = LLMFactory.create()

    def evaluate(
        self,
        criterion,
        bidder_text
    ):

        pass