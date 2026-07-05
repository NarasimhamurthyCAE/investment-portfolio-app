from advisor.rules.diversification_rule import (
    DiversificationRule,
)


class AdvisorEngine:

    def __init__(self):

        self.rules = [

            DiversificationRule(),

        ]

    def recommendations(

        self,

        portfolio

    ):

        result = []

        for rule in self.rules:

            result.extend(

                rule.evaluate(

                    portfolio

                )

            )

        return result