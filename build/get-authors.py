import json

class Authors:
    def __init__(self):
        self.json_object = {}
        with open('./site/docs/statics/authors/authors.json', 'r') as file:
            self.json_object = json.load(file)
        
    def author_exists(self, id):
        return self.get_author(id) is not None
    
    def get_author(self, id):
        return self.json_object.get(id, None)
    
    def get_author_display_name(self, id):
        author = self.get_author(id)
        if author is not None:
            name = author.get('display_name')
            if name is not None:
                return name
        return self.get_author_display_name('@unknown')
    
    def get_author_avatar(self, id):
        author = self.get_author(id)
        if author is not None:
            avatar = author.get('avatar')
            if avatar is not None:
                return avatar
        return self.get_author_avatar('@unknown')
    
    def get_author_href(self, id):
        author = self.get_author(id)
        if author is not None:
            href = author.get('href')
            if href is not None:
                return href
        return self.get_author_href('@unknown')