from pymongo import MongoClient
import csv
from operator import itemgetter


client = MongoClient()

db = client.twitter_data.tweets

# Used mongoimport to create my database named twitter_date and collection tweets

def main():
    terminated = False
    while (not terminated):
        print("Option 1: Search Content for Query")
        print("Option 2: Search Number of Right Troll/Left Troll tweets")
        print("Option 3: Find number of tweets on date (format of Month/Day/Year or Year)")
        print("Option 4: Tweets on 2016 debate days")
        print("Option 5: Tweets leading up to debates")
        print("Option 6: Number of tweets around some important dates")
        print("Option 7: Dates with the most/least tweets in 2016")
        print("Option 10: Terminate program")
        x = input("Select input: ")
        if (x == '1'):
            x = input("Search Query: ")
            tweet = db.aggregate([
                {'$match': {'content' : {'$regex': x}}},
                {'$sample': {'size' : 1}}
                ])
            for document in tweet:
                print('Random tweet of query (' + str(x) + '): ' + str(document.get('content')))
                print('Date: ' + str(document.get('publish_date')))
                print('Account Category: ' + str(document.get('account_category')))
            print('')

        elif (x == '2'):
            print('')
            tweet = db.count_documents({'account_category': 'RightTroll'})
            print('Number of Right Troll tweets: ' + str(tweet))
            tweet = db.count_documents({'account_category': 'LeftTroll'})
            print('Number of Left Troll tweets: ' + str(tweet))
            print('')
            print('In 2016: ')
            tweet = db.count_documents({'account_category': 'RightTroll', 'publish_date' : {'$regex' : '2016'}})
            print('Number of Right Troll tweets: ' + str(tweet))
            tweet = db.count_documents({'account_category': 'LeftTroll', 'publish_date' : {'$regex' : '2016'}})
            print('Number of Left Troll tweets: ' + str(tweet))
            print('')

        elif (x == '3'):
            print('')
            x = input("Search date (Month/Day/Year or Year): ")
            tweet = db.count_documents({'publish_date' : {'$regex' : x}})
            print('Number of tweets on (' + str(x) + '): ' + str(tweet))
            tweet = db.count_documents({'publish_date' : {'$regex' : x}, 'account_category': 'RightTroll'})
            print('Number of right troll tweets on (' + str(x) + '): ' + str(tweet))
            tweet = db.count_documents({'publish_date' : {'$regex' : x}, 'account_category': 'LeftTroll'})
            print('Number of left troll tweets on (' + str(x) + '): ' + str(tweet))
            print('')

        elif (x == '4'):
            print('')
            print('Number of tweets:')
            tweet = db.count_documents({'publish_date' : {'$regex' : '9/26/2016'}})
            print('First debate: ' + str(tweet))
            tweet = db.count_documents({'publish_date' : {'$regex' : '10/9/2016'}})
            print('Second debate: ' + str(tweet))
            tweet = db.count_documents({'publish_date' : {'$regex' : '10/19/2016'}})
            print('Third debate: ' + str(tweet))
            print('')

        elif (x == '5'):
            # 9/26, 10/9, 10/19 --> Debates
            print('')
            print('Number of tweets in database (from February 2012 to May 2018): ' + str(db.count_documents({})))
            print('Number of tweets in database during 2016: ' + str(db.count_documents({'publish_date': {'$regex' : '2016'}})))
            dates = ['9/25/2016', '10/8/2016', '10/18/2016']
            debate_dates = ['9/26/2016', '10/9/2016', '10/19/2016']
            for i in range(0, 3):
                tweet = db.count_documents({'publish_date' : {'$regex' : dates[i]}, 'account_category': 'RightTroll'})
                print('Leading up to the debate on ' + str(debate_dates[i]) + ', there were ' + str(tweet) + ' right troll tweets on ' + dates[i])
                tweet = db.count_documents({'publish_date' : {'$regex' : dates[i]}, 'account_category': 'LeftTroll'})
                print('Leading up to the debate on ' + str(debate_dates[i]) + ', there were ' + str(tweet) + ' left troll tweets on ' + dates[i])
            print('')

        elif (x == '6'):
            # 7/15 --> Trump running mate announcement
            # 7/22 --> Clinton running mate announcement
            # 7/23 --> Emails from DNC
            # 10/6 --> James Comey no punishment on Clinton's Emails
            # 10/8 --> Election date
            print('')
            print('Option 1: Trump announces running mate, Pence, 7/15')
            print('Option 2: Clinton announces running mate, Kaine, 7/22')
            print('Option 3: Email scandal from DNC revealed, 7/23')
            print("Option 4: James Comey, director of FBI, announces no wrongdoing from Clinton's emails, 10/6")
            print('Option 5: Election date, 10/8')
            print('Option 6: Input date of your choice')
            x = input("Select input: ")
            print('')
            month = 0
            day = 0
            year = 2016
            date = ''
            if (x == '1'):
                month = 7
                day = 15
            elif (x == '2'):
                month = 7
                day = 22
            elif (x == '3'):
                month = 7
                day = 24
            elif (x == '4'):
                month = 10
                day = 6
            elif (x == '5'):
                month = 10
                day = 8
            elif (x == '6'):
                date = input('Date(Month/Day/Year) or (Month/Day):')
                input_split = date.split('/')

                if (len(input_split) == 0):
                    break
                elif (len(input_split) == 1):
                    print('Invalid date')
                    break
                elif (len(input_split) == 2):
                    month = int(input_split[0])
                    if (month > 12 or month <= 0):
                        print('Invalid date')
                    day = int(input_split[1])
                    if (day > 31 or day <= 0):
                        print('Invalid date')
                        break
                elif (len(input_split) == 3):
                    month = int(input_split[0])
                    if (month > 12 or month <= 0):
                        print('Invalid date')
                    day = int(input_split[1])
                    if (day > 31 or day <= 0):
                        print('Invalid date')
                        break
                    year = int(input_split[2])
                    if (year > 2018 or year < 2012):
                        print('Invalid date')
                        break
            else:
                print('Invalid input')
                break

            right_tweets = 0
            left_tweets = 0


            for i in range(1, 8):
                if (day - (8 - i) > 0):
                    date = str(month) + '/' + str(day - (8 - i)) + '/' + str(year)
                    right_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'RightTroll'})
                    left_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'LeftTroll'})
                    print('On ' + date + ', Right Troll Tweets: ' + str(right_tweets) + ', Left Troll Tweets: ' + str(left_tweets))
            date = str(month) + '/' + str(day) + '/' + str(year)
            right_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'RightTroll'})
            left_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'LeftTroll'})
            print('Significant/Chosen ' + date + ', Right Troll Tweets: ' + str(right_tweets) + ', Left Troll Tweets: ' + str(left_tweets))
            for i in range(1, 8):
                date = str(month) + '/' + str(day + i) + '/' + str(year)
                right_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'RightTroll'})
                left_tweets = db.count_documents({'publish_date' : {'$regex' : date}, 'account_category': 'LeftTroll'})
                if (right_tweets != 0 and left_tweets != 0):
                    print('On ' + date + ', Right Troll Tweets: ' + str(right_tweets) + ', Left Troll Tweets: ' + str(left_tweets))
            print('')


        elif (x == '7'):
            print('')
            print("In 2016: ")
            Date_dictionary = {}
            tweet = db.aggregate([
                {'$match': {'publish_date' : {'$regex': '2016'}}}
            ])
            for documents in tweet:
                date = str(documents.get('publish_date')).split()
                if date[0] in Date_dictionary:
                    Date_dictionary[date[0]] = Date_dictionary[date[0]] + 1
                else:
                    Date_dictionary[date[0]] = 1
            most_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1), reverse = True)[:5])
            least_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1))[:5])
            print("Dates with most tweets:")
            for x in most_tweeted_dates.keys():
                print(x + ": " + str(most_tweeted_dates[x]))
            print("Dates with least tweets:")
            for x in least_tweeted_dates.keys():
                print(x + ": " + str(least_tweeted_dates[x]))
            print("")

            Date_dictionary = {}
            tweet = db.aggregate([
                {'$match': {'publish_date' : {'$regex': '2016'}, 'account_category' : 'LeftTroll'}}
            ])
            for documents in tweet:
                date = str(documents.get('publish_date')).split()
                if date[0] in Date_dictionary:
                    Date_dictionary[date[0]] = Date_dictionary[date[0]] + 1
                else:
                    Date_dictionary[date[0]] = 1
            most_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1), reverse = True)[:5])
            least_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1))[:5])
            print("Dates with most left troll tweets:")
            for x in most_tweeted_dates.keys():
                print(x + ": " + str(most_tweeted_dates[x]))
            print("Dates with least left troll tweets:")
            for x in least_tweeted_dates.keys():
                print(x + ": " + str(least_tweeted_dates[x]))
            print("")

            Date_dictionary = {}
            tweet = db.aggregate([
                {'$match': {'publish_date' : {'$regex': '2016'}, 'account_category' : 'RightTroll'}}
            ])
            for documents in tweet:
                date = str(documents.get('publish_date')).split()
                if date[0] in Date_dictionary:
                    Date_dictionary[date[0]] = Date_dictionary[date[0]] + 1
                else:
                    Date_dictionary[date[0]] = 1
            most_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1), reverse = True)[:5])
            least_tweeted_dates = dict(sorted(Date_dictionary.items(), key = itemgetter(1))[:5])
            print("Dates with most right troll tweets:")
            for x in most_tweeted_dates.keys():
                print(x + ": " + str(most_tweeted_dates[x]))
            print("Dates with least right troll tweets:")
            for x in least_tweeted_dates.keys():
                print(x + ": " + str(least_tweeted_dates[x]))
            print("")

        elif (x == '10'):
            terminated = True
        else:
            print('Invalid Input')

main()
