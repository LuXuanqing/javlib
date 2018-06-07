import json


class Movie():
    def __init__(self,
                 id,
                 preview=None,
                 genres=None,
                 cast=None,
                 is_HD=None,
                 last_visit=None,
                 local_dir=None):
        self.id = id
        self.preview = preview
        self.genres = genres
        self.cast = cast
        self.is_HD = is_HD
        self.last_visit = last_visit
        self.local_dir = local_dir

    @property
    def preview(self):
        return json.dumps(self.preview)
    @property
    def genres(self):
        return json.dumps(self.genres)
    @property
    def cast(self):
        return json.dumps(self.cast)
