import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

name_of_months ={"january":1,"february":2,
                    "march":3,"april":4,"may":5,
                    "june":6}

name_of_day = {"monday":1,"tuesday":2,
                   "wednesday":3,"thursday":4,
                   "friday":5,"saturday":6,"sunday":7}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    months ={"all","january","february",
            "march","april","may","june"}

    days = {"all", "monday","tuesday",
            "wednesday","thursday",
            "friday","saturday","sunday"}

    print('Hello! Let\'s explore some US bikeshare data!')

    city = input("Enter name of city: ").lower()

    while city not in ["chicago", "new york city", "washington"]:
        city = input("Invalid name of city.Try again:").lower()

    month = input("Enter name of month: ").lower()

    while month not in months:
        month = input("Invalid name of month.Try again:")

    day = input("Enter name of day: ").lower()

    while day not in days:
        day = input("Invalid name of day.Try again:")

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
    
    keys = CITY_DATA.keys()

    for key in keys:
        if key == city:
            df = pd.read_csv(CITY_DATA[key])
            break
            
    
    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df["month"] = pd.to_datetime(df['Start Time'], format='%MMMM').dt.month
    df["day"] = df['Start Time'].dt.dayofweek
    df["hour"] = pd.to_datetime(df['Start Time'], format='%H').dt.hour

    if month !="all":
        df = df.loc[df['month'] ==  name_of_months[month]]
    if day !="all":
        df = df.loc[df['day'] ==  name_of_day[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months =["january","february",
            "march","april","may","june"]

    days = ["monday","tuesday",
            "wednesday","thursday",
            "friday","saturday","sunday"]
    
    count = df.groupby('month')["month"].count().sort_values(ascending=False).index[0]
    print("The most popular month is:",months[count-1].capitalize())
    
    count = df.groupby('day')["day"].count().sort_values(ascending=False).index[0]
    print("The most popular day of week is:",days[count-1].capitalize())
 
    count = df.groupby('hour')["hour"].count().sort_values(ascending=False).index[0]
    print("The most popular hour is:",count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    sstation = df.groupby('Start Station')["Start Station"].count().sort_values(ascending=False).index[0]
    print("Most commonly used start station is: ",sstation)

    estation = df.groupby('End Station')["End Station"].count().sort_values(ascending=False).index[0]
    print("Most commonly used end station is: ",estation)

    df["Combine station"] = df["Start Station"] +"-" + df["End Station"]
    cstation = df.groupby('Combine station')["Combine station"].count().sort_values(ascending=False).index[0]
    print("Most frequent combination of start station and end station trip is: ",cstation)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: {}s".format(df["Trip Duration"].sum()))

    # TO DO: display mean travel time
    print("Mean travel time: {}s".format(df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user type:")
    print(df['User Type'].value_counts())

    try:
        print("Counts of gender:",df['Gender'].value_counts())
        print("Earliest year of birth: ",df["Birth Year"].max())
        print("Most recent year of birth: ",df["Birth Year"].min())
        year = df.groupby('Birth Year')["Birth Year"].count().sort_values(ascending=False).index[0]
        print("Most common year of birth is: ",year)
    except:
        print("No data about gender or year of birth")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
if __name__ == "__main__":
	main()
