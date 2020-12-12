class Document(object):
    def __init__(self, name):
        self.id = None
        self.name = name
        self.title = None
        self.body = None
        self.published = None
        self.updated = None
        self.content = None
        self.cleaned_article = None
        self.raw_cleaned_article = None
        self.prediction_class = None
        self.prediction_score = None

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_body(self, body):
        self.body = body

    def set_published(self, published):
        self.published = published

    def set_updated(self, updated):
        self.updated = updated

    def set_content(self, content):
        self.content = content

    def set_cleaned_article(self, cleaned_article):
        self.cleaned_article = cleaned_article

    def set_raw_cleaned_article(self, raw_cleaned_article):
        self.raw_cleaned_article = raw_cleaned_article

    def set_prediction_class(self, prediction_class):
        self.prediction_class = prediction_class

    def set_prediction_score(self, prediction_score):
        self.prediction_score = prediction_score

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

    def get_published(self):
        return self.published

    def get_updated(self):
        return self.updated

    def get_content(self):
        return self.content

    def get_name(self):
        return self.name

    def get_cleaned_article(self):
        return self.cleaned_article

    def get_raw_cleaned_article(self):
        return self.raw_cleaned_article

    def get_prediction_class(self):
        return self.prediction_class

    def get_prediction_score(self):
        return self.prediction_score

    def get_data(self):
        data = {}
        data["prediction_class"] = self.prediction_class
        data["prediction_score"] = self.prediction_score
        data["name"] = self.name
        data["title"] = self.title
        data["published"] = self.published
        data["updated"] = self.updated
        data["cleaned_article"] = self.cleaned_article
        data["raw_cleaned_article"] = self.raw_cleaned_article
        data["original_content"] = self.content
        return data

