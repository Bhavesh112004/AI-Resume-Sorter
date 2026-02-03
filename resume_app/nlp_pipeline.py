import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK resources (run once)
nltk.download('punkt')
nltk.download('stopwords')

# Function to tokenize and remove stopwords
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text)

    # Convert to lowercase and remove punctuation
    tokens = [re.sub(r'[^\w\s]', '', word.lower()) for word in tokens if word.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens
