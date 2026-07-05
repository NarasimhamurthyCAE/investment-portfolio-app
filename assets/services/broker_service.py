from __future__ import annotations

from assets.repositories.broker_repository import BrokerRepository


class BrokerService:

    def __init__(self):

        self.repository = BrokerRepository()

    def broker_names(self):

        return self.repository.names()