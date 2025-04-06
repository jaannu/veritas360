from transformers import pipeline

class SentimentAgent:
    def __init__(self, tools, db):
        self.tools = tools
        self.db = db

    def think(self, feedbacks):
        negative_keywords = ['issue', 'problem', 'bad', 'poor', 'slow', 'delay', 'confusing']
        negative_phrases = ['not resolved', 'not helpful', 'did not work', 'no response', 'never received']

        results = []
        for fb in feedbacks:
            fb_lower = fb.lower().strip()
            # Combine phrase + keyword checks
            if any(phrase in fb_lower for phrase in negative_phrases):
                sentiment = "Negative"
            elif any(word in fb_lower for word in negative_keywords):
                sentiment = "Negative"
            else:
                sentiment = "Positive"
            results.append(f"{fb} → {sentiment}")
        return "\n".join(results)
