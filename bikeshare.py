import time
import pandas as pd

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

    # get user input for city (chicago, new york city, washington). 
    while True:
        cities = ['chicago','new york city', 'washington']
        city= input("\nWhich city would you like to analyze? please pick from (Chicago, New York City and Washington)\n").lower()
        if city in cities:
            break
        else:
            print("\n Oops! Seems like you made a mistake. \n Please enter a valid city name")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['January', 'February', 'March', 'April', 'May', 'June','All']
        month= input("\nWhat month would you like to consider? You can pick from January, February, March, April, May and June. Or type 'All\' to view all \n").title()
        if month in months:
            break
        else:
            print("\n Oops! Seems like you made a mistake. \n Please enter a valid month")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days =['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','All']
        day = input("\nWhat day of the week would you like to consider? you can pick any day from Monday to Sunday. Or type 'All\' to view all\n").title()
        if day in days:
            break
        else:
            print("\n Oops! Seems like you made a mistake. \n Please enter a valid day")
    
    
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
    # load datafile into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of the week from Start Time column to create individual columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filtering by month when applied
    if month != 'All':
        #using index of the position of the months in the list to get the corresponding integer
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month)+1

        #filter by month to create new filtered DataFrame
        df = df[df['month'] == month]

    #fitering by day of week when applied
    if day != 'All':
        #filter by day to create new filtered DataFrame
        df =df[df['day_of_week']== day]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    if month == 'All':
        popular_month = df['month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = months[popular_month-1]
        print("The most common month is {}".format(popular_month))


    # display the most common day of week
    if day == 'All':
        popular_day = df['day_of_week'].mode()[0]
        print("The most common day is {}".format(popular_day))


    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print("The most common hour is {}:00 hours".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popularular stations and trip."""

    print('\nCalculating The Most popularular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station =df['Start Station'].mode()[0]
    print("The most commonly used Start Station is {}".format(popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most commonly used End Station is {}".format(popular_end_station))

    # display most frequent combination of start station and end station trip
    #new column combination
    df['Combination']= df['Start Station'] + " "+ "to"+" "+ df['End Station']
    popular_comb = df['Combination'].mode()[0]
    print("The most frequent combination of Start station and end station is {}".format(popular_comb))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum()
    minute,seconds =divmod(total_travel_duration,60)
    hour,minute=divmod(minute,60)
    days,hour =divmod(hour,24)
    print("The Total travel time: {} day(s) {} hour(s) {} minutes {} secs".format(days,hour,minute,seconds))

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    m,sec = divmod(mean_travel_time,60)
    h,m = divmod(m,60)
    if m>60:
        h,m = divmod(m,60)
        print("The average trip duration: {} hour(s) {} minutes {} secs".format(h,m,sec))
    else:
        print("The average trip duration: {} minutes {} secs". format(m,sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # Display counts of user types
    User_counts= df.groupby(['User Type'])['User Type'].count()
    print("\nCounts of User Types are:{}\n".format(User_counts))
    if city.title() == 'Chicago' or city.title() == 'New York City':
    # Display counts of gender
        Gender_count = df.groupby(['Gender'])['Gender'].count()
        print("\nCount of Gender is: {}\n".format(Gender_count))

    # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        popular_year =int(df['Birth Year'].mode()[0])
        print("The earliest year of birth is {} \nThe most recent is {} \nThe most common year of birth is {}".format(earliest,most_recent,popular_year))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """ Displays 5 lines of raw data at each iteration when prompted by user"""
    while True:
        response= ['Yes','No']
        choice = input ("\nWould you like to view individual trip data (5 entries)? Type 'Yes\' or 'No\' \n").title()
        if choice in response:
            if choice == 'Yes':
                start = 0
                end =5
                data =df.iloc[start:end,:9]
                print (data)
            break
        else:
            print("Oops! Seems like you made a mistake. Please enter a valid response")
    if choice == 'Yes':
        while True:
            choice_2= input("\n Would you like to see more trip data? Type 'Yes\' or 'No\' \n").title()
            if choice_2 in response:
                if choice_2 == 'Yes':
                    start += 5
                    end +=5
                    data =df.iloc[start:end,:9]
                    pd.set_option('display.max_columns',9)
                    print (data)
                else:
                    break
            else:
                print("Oops! Seems like you made a mistake. Please enter a valid response")

def main():
    Y = True
    while Y:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        X =True
        while X:
            restart = input('\nWould you like to restart? Enter Yes or No.\n').title()
            if restart.title() == 'No':
                X =False
                Y =False
            elif restart.title() == 'Yes':
                X = False
            else:
                print("Oops! Seems like you made a mistake. Please enter a valid response")
                X= True
                

           
                
if __name__ == "__main__":
	    main()
