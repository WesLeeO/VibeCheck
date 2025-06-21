from transformers import pipeline
from collections import defaultdict
import numpy as np
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from wordcloud import WordCloud
from io import BytesIO
import base64

class TweetAnalyzer:
    def __init__(self):
        # Lazy loading - don't initialize until needed
        self.sentiment_pipeline = None
        self.emotion_pipeline = None
        
    def _load_sentiment_model(self):
        if not self.sentiment_pipeline:
            # Consider using a smaller model like "distilbert-base-uncased-finetuned-sst-2-english"
            self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    def _load_emotion_model(self):
        if not self.emotion_pipeline:
            self.emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")
    
    def analyze_sentiment(self, tweets):
        """Batch sentiment analysis"""
        self._load_sentiment_model()
        results = self.sentiment_pipeline(tweets)
        return [{"label": result["label"], "score": round(result["score"], 3)} for result in results]
    
    def analyze_emotion(self, tweets):
        """Batch emotion analysis"""
        self._load_emotion_model()
        results = self.emotion_pipeline(tweets)
        return [{"emotion": result["label"], "score": round(result["score"], 3)} for result in results]
    
    def analyze_tweets(self, tweets):
        """Comprehensive analysis of a batch of tweets"""
        if not tweets:
            return None
            
        results = {
            "tweets": [],
            "sentiment_counts": defaultdict(int),
            "emotion_counts": defaultdict(int),
            "sentiment_scores": [],
            "emotion_scores": defaultdict(list)
        }
        
        # Extract just the tweet texts for batch processing
        texts = [tweet for tweet, _ in tweets]
        
        # Batch process sentiment and emotion
        sentiment_results = self.analyze_sentiment(texts)
        emotion_results = self.analyze_emotion(texts)
        
        for i, (tweet, date) in enumerate(tweets):
            try:
                analysis = {
                    "text": tweet,
                    "date": datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y").strftime("%A, %B %d, %Y at %H:%M %Z"),
                    "sentiment": sentiment_results[i],
                    "emotion": emotion_results[i],
                }
                
                results["tweets"].append(analysis)
                
                # Aggregate sentiment data
                results["sentiment_counts"][analysis["sentiment"]["label"]] += 1
                results["sentiment_scores"].append(analysis["sentiment"]["score"])
                
                # Aggregate emotion data
                emotion_label = analysis["emotion"]["emotion"]
                results["emotion_counts"][emotion_label] += 1
                results["emotion_scores"][emotion_label].append(analysis["emotion"]["score"])
            except Exception as e:
                print(f"Error analyzing tweet: {e}")
                continue
        
        # Calculate averages and percentages
        total_tweets = len(results["tweets"])
        if total_tweets > 0:
            results["sentiment_percentages"] = {
                k: round((v/total_tweets)*100, 1)
                for k, v in results["sentiment_counts"].items()
            }
            results["emotion_percentages"] = {
                k: round((v/total_tweets)*100, 1)
                for k, v in results["emotion_counts"].items()
            }
            
        return results
    
    # Implement your word cloud method here...
    def word_cloud(self, tweets):
        """Generate word cloud and return as base64 string"""
        print('entered')
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(tweets))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        wordcloud_img = self.plot_to_base64(fig)
        return wordcloud_img
    

    def plot_to_base64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)
        return img_base64