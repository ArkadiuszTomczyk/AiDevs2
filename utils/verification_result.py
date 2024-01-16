class VerificationResult:
    def __init__(self, json):
        self.id = json['id']
        self.model = json['model']
        self.results = []
        for result in json['results']:
            self.results.append(result['flagged'])
