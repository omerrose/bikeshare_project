import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june','all']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday','all']
CITIES = list(CITY_DATA.keys())

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = None
    while city not in CITIES:
        city = input('Whould you like to see data for Chicago, New York City, or Washington? ').lower()
    print('We received your input: {}'.format(city))
        
# get user input for filtering the data
        
    set_filter = None
    month = None
    day = None
    option_list = ['month', 'day', 'both', 'none']
    while set_filter not in option_list:
        set_filter = input('How do you want to filter the data? Type one of the following options: month, day, both, none ').lower()
    print('Selected filter: {}'.format(set_filter))

# get user input for month (all, january, february, ... , june)
    
    if set_filter == 'month':
        while month not in MONTHS:
            month = input('Which month? January, February, March, April, May, or June? ' ).lower()
            day = 'all'
        print('Selected Month: {}'.format(month))  
        
# get user input for day of week (all, monday, tuesday, ... sunday)

    elif set_filter == 'day':
        while day not in DAYS:
            day = input('Which Day? ' ).lower()
            month = 'all'
        print('Selected Day: {}'.format(day))
        
# get user input for day of week (all, monday, tuesday, ... sunday) and month (all, january, february, ... , june)

    elif set_filter == 'both':
        while month not in MONTHS:
            month = input('Which month? January, February, March, April, May, or June? ' ).lower()
        print('Selected Month: {}'.format(month))  
        while day not in DAYS:
            day = input('Which Day? ' ).lower()
        print('Selected Day: {}'.format(day))
        
        
# no filtering        
        
    else: 
        month = 'all'
        day = 'all'
    
    

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Popular Month:', MONTHS[popular_month-1])

    #display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print('Most Popular Day Of Week:', popular_day_of_week)

    #display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station
    
    start_station = df['Start Station'].value_counts().index.tolist()[0]
    print('Most commonly used start station: {}'.format(start_station))

    #display most commonly used end station
    end_station = df['End Station'].value_counts().index.tolist()[0]
    print('Most commonly used end station: {}'.format(end_station))
    

    #display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print('Most frequent combination of start station and end station trip: {}'.format(most_frequent_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
 
    
    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum(), 2)
    a=str(int(total_travel_time//3600))
    b=str(int((total_travel_time%3600)//60))
    c=str(int((total_travel_time%3600)%60))
    print('Total travel time is: {} hours {} mins {} seconds'.format(a, b, c))
    
  

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean(), 2)
    a=str(int(mean_travel_time//3600))
    b=str(int((mean_travel_time%3600)//60))
    c=str(int((mean_travel_time%3600)%60))
    print('Mean travel time is: {} hours {} mins {} seconds'.format(a, b, c))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
          
          
               
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    subscriber = df.loc[:,'User Type'].value_counts()[0]
    customer = df.loc[:,'User Type'].value_counts()[1]
    print('Number of subscribers: {}, Number of customers: {}'.format(subscriber, customer))
    
    # Display counts of gender
    if 'Gender' in df.columns:
         
        male = df.loc[:,'Gender'].value_counts()[0]
        female = df.loc[:,'Gender'].value_counts()[1]
        print('Number of males: {}, Number of females: {}'.format(male, female))
    else:
         print('There are no Gender data in this table.')
    
    if 'Birth Year' in df.columns:
        # We drop any rows with NaN values
        df = df[pd.notnull(df['Birth Year'])]
        #Converting dtype to int
        df['Birth Year'] = df['Birth Year'].astype(int)
        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        print('Earliest year of birh: {}'.format(earliest_year_of_birth))
        most_recent_year_of_birth = df['Birth Year'].max()
        print('Most recent year of birh: {}'.format(most_recent_year_of_birth))  
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common year of birth: {}'.format(most_common_year))
    else:
         print('There are no Birth Year data in this table.')
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def display_output(df):
    """
    The user is asked if he would like to see five rows of output data.
    Each time, display 5 rows of data.
    """
    i = 0
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5
    


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_output(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
