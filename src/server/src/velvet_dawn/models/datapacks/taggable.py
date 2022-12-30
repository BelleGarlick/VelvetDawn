

class Taggable:
    def __init__(self):
        self.tags = set()

    def tagged_with(self, tag: str) -> bool:
        return tag in self.tags

    def _load_tags(self, data: dict):
        from velvet_dawn.datapacks import tags

        given_tags = data.get("tags", [])

        # Update datapack tags
        for tag in given_tags:
            if tag not in tags: tags[tag] = []
            tags[tag].append(self)

        self.tags = set(given_tags)
