import time
from numpy.lib import index_tricks
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO:[done] get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter city:").lower()
    
    # TO DO:[done] get user input for month (all, january, february, ... , june)
    month = input("Enter month:").lower()

    # TO DO:[done] get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day:").lower()


    print('-'*40)
    return city, month, day


def load_data(city, month, dayofweek):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df.drop(["Unnamed: 0"],inplace=True ,axis=1) #drop id column
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if dayofweek != 'all':
        days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',"friday"]
        dayofweek = days.index(dayofweek) 
        # filter by day of week to create the new dataframe
        df = df[df['dayofweek'] == dayofweek]
    
    return df


def time_stats(city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """ ignore filters and load data based on the city"""
    df=load_data(city, "all", "all")

    # TO DO: display the most common month
    most_common_month= df['month'].mode()[0]
    print("the the most common month",most_common_month)



    # TO DO: display the most common day of week
    most_common_day= df['dayofweek'].mode()[0]
    print("the the most common day of week",most_common_day)


    # TO DO: display the most common start hour
    
    most_common_start= df['hour'].mode()[0]
    print("the the most common start hour",most_common_start)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_Start_Station= df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_Start_Station)


    # TO DO: display most commonly used end station
    popular_End_Station= df['End Station'].mode()[0]
    print('Most Popular end Station:', popular_End_Station)


    # TO DO: display most frequent combination of start station and end station trip
    start_end_station=(df['Start Station'] + "||" + df['End Station']).mode()[0]
    print('Most frequent combination of start station and end station trip:',start_end_station.split("||"))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time= df['Trip Duration'].sum()
    print(" the total travel time:",total_travel_time)


    # TO DO: display mean travel time
    mean_travel_time= df['Trip Duration'].mean()
    print(" the mean travel time:",round(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    counts_of_user_types= df['User Type'].value_counts()
    print(" the counts of user types:",counts_of_user_types)
    #if data city is  washington do not aggregate the gender or birth
    if(city !=list(CITY_DATA.items())[2][0]): #got <washington> city as  key from CITY_DATA dictionary
        # TO DO: Display counts of gender
        counts_of_user_gender= df['Gender'].value_counts()
        print(" the counts of user gender:",counts_of_user_gender)


        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print(" the earliest year of birth:",int(earliest_birth_year))
        most_recent_birth_year = df['Birth Year'].max()
        print(" the most recent year of birth:",int(most_recent_birth_year))
        common_year_of_birth= df['Birth Year'].mode()[0]
        print(" the common year of birth:",int(common_year_of_birth))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    
    """ print raw data based on user request """

    print('\nRaw data is available to check... \n')
    start_loc = 0
    while True:
        View_raw = input('To View the availbale raw data in chuncks of 5 rows type Yes:').lower()
        if View_raw not in ['yes', 'no']:
            print('That\'s invalid choice, pleas type yes or no')

        elif View_raw == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc+=5

        elif View_raw == 'no':
            print('\nExiting...')
            break
    

#  chicago
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city,month ,day )
        time_stats(city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
