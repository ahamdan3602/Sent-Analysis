"""
Abdul al-rahman Hamdan
251362860
ahamdan4
The Date
Description: This Python file is responible for taking input from the user and calls functions in sentiment.py.
"""

from sentiment_analysis import *

def main():
    # Responsible for taking input from .tsv file
    keyword_file_name = input("Input keyword filename (.tsv file): ")

    # Checks if the filename ends with '.tsv'
    if not keyword_file_name.endswith('.tsv'):
        raise Exception("Must have tsv file extension!")
    
    # Responsible for taking input from the .csv file
    tweet_file_name = input("Input tweet filename (.csv file): ")

    # Checks if the filename ends with '.csv'
    if not tweet_file_name.endswith('.csv'):
        raise Exception("Must have csv file extension!")

    # Takes input for from the .txt file.
    output_file_name = input("Input filename to output report in (.txt file): ")

    # Checks if the filename ensd with '.txt'
    if not output_file_name.endswith('.txt'):
        raise Exception("Must have txt file extension!")

    # Responsibe for reading keywords and tweets from the specific file.
    keyword_dict = read_keywords(keyword_file_name)
    tweet_list = read_tweets(tweet_file_name)

    # Responsible for generating a sentiment based on the keyword and tweets.
    report = make_report(tweet_list, keyword_dict)

    # Wrtes the sentiment report to the specific output file
    write_report(report, output_file_name)

    print(f"Wrote report to {output_file_name}")


if __name__ == "__main__":
    main()
