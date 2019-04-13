import db as db


class Movie():
    def __init__(self, id):
        self.id = id

    @property
    def exist(self):
        return db.exist(self.id)

    def create(self):
        db.insert_movie(self.id)

    @property
    def preview(self):
        return db.getone(self.id, 'preview')

    @preview.setter
    def preview(self, value):
        db.setone(self.id, 'preview', value)

    @property
    def genres(self):
        return db.getone(self.id, 'genres')

    @genres.setter
    def genres(self, value):
        db.setone(self.id, 'genres', value)

    @property
    def cast(self):
        return db.getone(self.id, '"cast"')

    @cast.setter
    def cast(self, value):
        db.setone(self.id, '"cast"', value)

    def log(self, domain):
        db.insert_log(self.id, domain)

    @property
    def last_visit(self):
        result = db.get_log(self.id)
        if result is None:
            return None
        return {
            'timestamp': result[0],
            'domain': result[1]
        }




if __name__ == '__main__':
    # ids = ['TEST-001', 'TEST-002', 'TEST-003', 'TEST-404']
    # for id in ids:
    #     av = Movie(id)
    #     av.create()
    av = Movie('ATID-298')
    print(av.last_visit)
    # help(av)