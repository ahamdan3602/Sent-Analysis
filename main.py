"""
Abdul al-rahman Hamdan
Description: This Python file contains functions for sentiment analysis based on keywords in tweets. Responsible for performing sentiment analysis on tweets by the given functions. Functionalities include read keywords and tweets, clan tweets, calculate sentiment, classifying sentimen into categories, and writing the report to an output file.
"""

def read_keywords(keyword_file_name):
    # Function is responsible for reading keywords and return a dictionary.
    keyword_dict = {}
    file = None  # Initializes the file variable
    try:
        file = open(keyword_file_name, 'r')
        lines = [line.strip().split('\t') for line in file]

        for keyword, score in lines:
            keyword_dict[keyword] = int(score)

    except IOError:
        print(f"Could not open file {keyword_file_name}!")

    finally:
        if file:
            file.close()  # Ensures that the file is closed

    return keyword_dict

def clean_tweet_text(tweet_text):
    # Function is responsible for cleaning the given tweet text by removing non-alphabetic characters.
    cleaned_text = ""
    for char in tweet_text:
        if char.isalpha() or char.isspace():
            cleaned_text += char.lower()
    return cleaned_text

def calc_sentiment(tweet_text, keyword_dict):
    # Responsible for calculating the sentiment score for a given tweet text based on the provided keyword dictionary.
    # Splits the cleaned tweet text into words
    words = tweet_text.split()

    # Initializing the sentiment score
    sentiment_score = 0

    # This for statement is responsible for calculating sentiment score based on keyword dictionary
    for word in words:
        if word in keyword_dict:
            sentiment_score += keyword_dict[word]

    return sentiment_score

def classify(score):
    # This function is responsible for classifying the given sentiment score into a category.
    if score > 0: 
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral" #Classifies sentiment based on input scores

def read_tweets(tweet_file_name):
    # This function is responsible for reading tweets from a file and returns a list with a dictionary for each tweet.
    tweet_list = []
    file = None  # Initializes the file variable
    #Opens and attempts to pen and reada a file with tweet data and process each line.
    try:
        file = open(tweet_file_name, 'r')
        for line in file:
            fields = line.strip().split(',')
            # Creates a dictionary for each tweet with relevant information.
            tweet_dict = {
                'date': fields[0],
                'text': clean_tweet_text(fields[1]),
                'user': fields[2],
                'retweet': int(fields[3]),
                'favorite': int(fields[4]),
                'lang': fields[5],
                'country': fields[6],
                'state': fields[7],
                'city': fields[8],
                'lat': float(fields[9]) if fields[9] != 'NULL' else 'NULL',
                'lon': float(fields[10]) if fields[10] != 'NULL' else 'NULL',
            }
            # Adds the tweet dictionary to the tweet_list.
            tweet_list.append(tweet_dict)
    # IOError if the file can't be opened
    except IOError:
        print(f"Could not open file {tweet_file_name}!")

    #Makes sure the file is closed
    finally:
        if file:
            file.close()
    return tweet_list

# ...

def make_report(tweet_list, keyword_dict):
    # Creates a dictionary containing the sentiment report values.
    report = {
        'avg_favorite': "NAN",
        'avg_retweet': "NAN",
        'avg_sentiment': "NAN",
        'num_favorite': 0,
        'num_negative': 0,
        'num_neutral': 0,
        'num_positive': 0,
        'num_retweet': 0,
        'num_tweets': 0,
        'top_five': ""
    }

    total_sentiment = 0
    total_favorite_sentiment = 0
    total_retweet_sentiment = 0
    favorite_count = 0
    retweet_count = 0
    country_sentiments = {}

    for tweet in tweet_list:
        # Calculate the sentiments for the current tweet
        sentiment = calc_sentiment(tweet['text'], keyword_dict)

        # Collects the total sentiment for all tweets
        total_sentiment += sentiment

        # Responsibe for checking if the tweet has positive favorites.
        if tweet['favorite'] > 0:
            total_favorite_sentiment += sentiment
            favorite_count += 1

        #Responsible for checking if the tweet has positive retweets
        if tweet['retweet'] > 0:
            total_retweet_sentiment += sentiment
            retweet_count += 1
        
        if sentiment < 0:
            report['num_negative'] += 1
        elif sentiment == 0:
            report['num_neutral'] += 1
        else:
            report['num_positive'] += 1

        report['num_tweets'] += 1

        country = tweet['country']

        # Checks if the 'country' in the tweet dictionary is not 'NULL'
        if country != 'NULL':
            if country not in country_sentiments:
                country_sentiments[country] = [sentiment]
            else:
                country_sentiments[country].append(sentiment)

    report['avg_sentiment'] = round(total_sentiment / max(1, report['num_tweets']), 2)
    report['avg_favorite'] = round(total_favorite_sentiment / max(1, favorite_count), 2) if favorite_count > 0 else "NAN"
    report['avg_retweet'] = round(total_retweet_sentiment / max(1, retweet_count), 2) if retweet_count > 0 else "NAN"

    report['num_favorite'] = favorite_count
    report['num_retweet'] = retweet_count

    sorted_countries = sorted(country_sentiments.keys(), key=lambda country: sum(country_sentiments[country]) / len(country_sentiments[country]), reverse=True)

    top_five_countries = sorted_countries[:5]

    # Join the countries into a comma-separated string
    report['top_five'] = ', '.join(top_five_countries)

    return report

def write_report(report, output_file):
    # Function is responsible for writing the sentiment report to the output file.
    file = None  # Initializes the file variable
    try:
        # Opens the specified output file in write mode
        file = open(output_file, 'w')

        # Writes sentiment-related info to the file.
        file.write("Average Sentiment of all tweets: {}\n".format(report['avg_sentiment']))
        file.write("Total number of tweets: {}\n".format(report['num_tweets']))
        file.write("Number of positive tweets: {}\n".format(report['num_positive']))
        file.write("Number of negative tweets: {}\n".format(report['num_negative']))
        file.write("Number of neutral tweets: {}\n".format(report['num_neutral']))
        file.write("Number of favorited tweets: {}\n".format(report['num_favorite']))
        file.write("Average sentiment of favorited tweets: {}\n".format(report['avg_favorite']))
        file.write("Number of Retweeted Tweets: {}\n".format(report['num_retweet']))
        file.write("Average sentiment of retweeted tweets: {}\n".format(report['avg_retweet']))
        file.write("Top Five Countries: {}\n".format(report['top_five']))

    except IOError: 
        #IOError if the file can't be opened.
        print("Could not open file {}".format(output_file))

    finally:
        if file:
            file.close()
