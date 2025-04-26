from transformers import pipeline
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from datetime import datetime


class TweetAnalyzer:
    def __init__(self):
        # Initialize multiple NLP pipelines
        self.sentiment_pipeline = pipeline("sentiment-analysis")
        self.emotion_pipeline = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")
    

    def analyze_sentiment(self, tweet):
        """Basic sentiment analysis"""
        result = self.sentiment_pipeline(tweet)[0]
        return {
            "label": result["label"],
            "score": round(result["score"], 3)
        }
    
    def analyze_emotion(self, tweet):
        """More granular emotion analysis"""
        result = self.emotion_pipeline(tweet)[0]
        return {
            "emotion": result["label"],
            "score": round(result["score"], 3)
        }
    
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
        
        for tweet, date in tweets:
            try:
                analysis = {
                    "text": tweet,
                    "date": datetime.strptime(date, "%a %b %d %H:%M:%S %z %Y").strftime("%A, %B %d, %Y at %H:%M %Z"),
                    "sentiment": self.analyze_sentiment(tweet),
                    "emotion": self.analyze_emotion(tweet),
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
            #results["average_sentiment_score"] = round(np.mean(results["sentiment_scores"]), 2)
            #results["average_emotion_scores"] = {
            #    k: round(np.mean(v), 2)
            #    for k, v in results["emotion_scores"].items()
            #}
        
        return results
    
    def generate_word_cloud(self, tweets):
        """Generate word cloud and return as base64 string"""
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(texts))
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        wordcloud_img = self.plot_to_base64(fig)
        return wordcloud_img