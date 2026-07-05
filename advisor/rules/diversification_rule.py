from advisor.base_rule import BaseRule


class DiversificationRule(BaseRule):

    def evaluate(
        self,
        portfolio
    ):

        recommendations = []

        if len(portfolio.investments) < 5:

            recommendations.append(

                {

                    "priority": "Medium",

                    "title": "Increase Diversification",

                    "message":

                        "Portfolio contains only a few investments."

                }

            )

        return recommendations