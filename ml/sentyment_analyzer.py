import joblib
import os


class SentimentAnalyzer:
    _model = None

    def __init__(self, model_path='logreg_model.pkl'):
        self.model_path = model_path
        self._load_model()

    def _load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f'Модель {self.model_path} не найдена')

        self._model = joblib.load(self.model_path)

    def predict(self, text: str) -> dict:
        if not text:
            return {'sentiment': 'neutral', 'score': 0.5}

        probas = self._model.predict_proba([text])[0]

        neg = probas[0]
        pos = probas[1]

        if pos > 0.6:
            return {'sentiment': 'positive', 'score': round(pos, 4)}
        elif neg > 0.6:
            return {'sentiment': 'negative', 'score': round(neg, 4)}
        else:
            return {'sentiment': 'neutral', 'score': 0.5}


# Singleton
analyzer = SentimentAnalyzer()
