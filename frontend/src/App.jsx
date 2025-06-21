import React, { useState } from "react";
import './App.css'

function App() {
  const [username, setUsername] = useState("");
  const [info , setInfo] = useState({})
  const [cloud, setCloud] = useState("")
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showEmotion, setShowEmotion] = useState(false);
  const [displayError, setError] = useState(false)

  
  const fetchAnalysis = async () => {
    if (!username.trim()) return;
    
    setLoading(true);
    try {
    //  const res = await fetch(`http://localhost:8000/analyze/${username}`);
      const res = await fetch(`https://wesleeo--vibecheck-nlp-fastapi-app.modal.run/analyze/${username}`)
     // const res = await fetch(`https://vibecheck-tkk2.onrender.com/analyze/${username}`);
      const data = await res.json();
      setError(false)
      setInfo(data.info)
      setCloud(data.word_cloud)
      setResults(data.results.tweets);
      setShowEmotion(true)
    } catch (error) {
      setError(true)
      setResults([])
      setShowEmotion(false)
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white px-4 py-12">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between mb-12">
          <div>
            <h1 className="text-4xl font-bold text-indigo-800">VibeCheck</h1>
            <p className="text-gray-600 mt-2">Analyze sentiment across Twitter/X posts</p>
          </div>
          <div className="mt-4 md:mt-0">
            <span className="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
              Sentiment Analysis Tool
            </span>
          </div>
        </div>

        {/* Search Panel */}
        <div className="bg-white shadow-lg rounded-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center gap-4">
            <div className="flex-grow">
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                Twitter Username
              </label>
              <input
                id="username"
                type="text"
                placeholder="e.g. elonmusk"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full border border-gray-300 px-4 py-3 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
              />
            </div>
            <div className="md:self-end">
              <button
                onClick={fetchAnalysis}
                disabled={loading}
                className="w-full md:w-auto bg-indigo-600 text-black px-6 py-3 rounded-lg hover:bg-indigo-500 hover:shadow-md transition-all duration-200 font-medium disabled:opacity-70"
              >
                {loading ? "Analyzing..." : "Analyze 🔍"}
              </button>
            </div>
          </div>
        </div>
        {Object.keys(info).length > 0 && (
        <div className="max-w-sm mx-auto bg-white shadow-lg rounded-2xl p-6 flex flex-col items-center space-y-4 mb-6 hover:bg-indigo-500">
          <img 
            src={info.profile_picture.replace('_normal', '_400x400') || 'https://via.placeholder.com/150'} 
            alt="Profile"
            className="w-32 h-32 rounded-full object-cover shadow-md"
          />
          <h2 className="text-xl font-semibold text-gray-800">{info.name || 'Unknown User'}</h2>
          <p className="text-sm text-gray-600 text-center">{info.description || 'No description available.'}</p>
        </div>
      )}

    {cloud.length > 0 && (
      <div className="text-center">
        <p className="text-lg font-semibold mb-2">Most used words</p>
        <img
          src={cloud}
          alt="Word Cloud"
          className="mb-4 w-full max-w-2xl rounded shadow mx-auto"
        />
      </div>
    )}

        {results.length > 0 && (
        <button 
          onClick={() => setShowEmotion(!showEmotion)}
          className="mb-4 px-4 py-2 bg-indigo-600 text-black rounded-md text-sm"
        >
          {showEmotion ? 'Show Sentiment' : 'Show Emotion'}
        </button>
      )}
        {/* Results Section */}
        {results.length > 0  && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Analysis Results</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {results.map((result, idx) => (
                <div 
                  key={idx} 
                  className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start mb-2">
                    <p className="text-lg font-semibold text-indigo-700">{showEmotion ? result.emotion.emotion : result.sentiment.label}</p>
                    <p className='text-lg font-semibold text-black'>{result.date}</p>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      (showEmotion ? result.emotion.score : result.sentiment.score) > 0.7 ? "bg-green-100 text-green-800" : 
                      (showEmotion ? result.emotion.score : result.sentiment.score) > 0.4 ? "bg-yellow-100 text-yellow-800" : 
                      "bg-red-100 text-red-800"
                    }`}>
                      Score: {showEmotion ? result.emotion.score :  result.sentiment.score}
                    </span>
                  </div>
                  <p className="text-gray-600">{result.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}
        {displayError && (
          <p>Username not found</p>
        )}

        {/* Empty State */}
        {results.length === 0 && !loading && (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm">
            <p className="text-gray-500">Enter a Twitter username and click Analyze to see results</p>
          </div>
        )}

        {/* Footer */}
        <div className="mt-12 pt-4 border-t border-gray-200">
          <div className="flex justify-between items-center">
            <p className="text-sm text-gray-500">VibeCheck Sentiment Analysis</p>
            <div className="flex items-center">
              <span className="h-8 w-8 rounded-full bg-indigo-800 flex items-center justify-center text-white font-bold">
                VC
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;