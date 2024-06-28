from api.domain.entity import Entity
import logging

logger = logging.getLogger(__name__)


class Repository:
    def __init__(self) -> None:
        self.entities = {}

    def add(self, entity: Entity) -> Entity:
        self.entities[entity.id] = entity
        return entity

    def remove(self, id) -> Entity:
        return self.entities.pop(id)

    def find_by_id(self, id) -> Entity:
        return self.entities[id]
