#!/usr/bin/env python3
#Navigate to CrowdStrike console - locate Sensor report in investigate tab and export out last 7 day host count
#Download the report as a CSV file and save locally
#Run Python Script and navigate to CSV File
#Select CSV and click open 


import pandas as pd
import tkinter as tk
from tkinter import filedialog


#create tkinter window with a display field
window = tk.Tk()
window.geometry('500x500')
window.title('Select CSV for parsing')

#define file open and store variable for later
def fileopen():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    return filename

#define a function to load a csv into pandas to be parsed
def load_csv():
    #open file
    filename = fileopen()
    #load csv into pandas
    df = pd.read_csv(filename)
    #remove duplicates based on Host Name
    #df.drop_duplicates(subset='Host Name', keep='first', inplace=True)
    #store values from First Seen (UTC) column and Last Seen (UTC) column in two seprate variables and end the function
    first_seen = df['First Seen (UTC)'].values
    last_seen = df['Last Seen (UTC)'].values
    return first_seen, last_seen

#create a tkinter label to display the results
def display_results():
    #load csv into pandas
    first_seen, last_seen = load_csv()
    #convert first_seen and last_seen to datetime objects
    first_seen = pd.to_datetime(first_seen)
    last_seen = pd.to_datetime(last_seen)
    #calculate the difference between first_seen and last_seen
    difference = last_seen - first_seen
    #convert difference to hours
    difference = difference.astype('timedelta64[h]')
    #extract the values into a list
    difference = difference.values.tolist()
    #count the amount of values in the list that are greater than or equal to 1
    count = 0
    for i in difference:
        if i >= 1:
            count += 1
    #count the amount of values in the list that are greater than or equal to 2
    count2 = 0
    for i in difference:
        if i >= 2:
            count2 += 1
    #count the amount of values in the list that are greater than or equal to 4
    count3 = 0
    for i in difference:
        if i >= 4:
            count3 += 1
    #count the amount of values in the list that are greater than or equal to 8
    count4 = 0
    for i in difference:
        if i >= 8:
            count4 += 1
    #count the amount of values in the list that are greater than or equal to 24
    count5 = 0
    for i in difference:
        if i >= 24:
            count5 += 1
    #count the amount of values in the list that are greater than or equal to 168 hours or 1 week.
    count6 = 0
    for i in difference:
        if i >= 168:
            count6 += 1
    #count the amount of values in the list that are greater than or equal to 720 hours or 1 month.
    count7 = 0
    for i in difference:
        if i >= 720:
            count7 += 1

    #create a tkinter label to display the results in large text
    label = tk.Label(window, text="""
    There are {} devices that have been online for more than 1 hour.
    There are {} devices that have been online for more than 2 hours.
    There are {} devices that have been online for more than 4 hours.
    There are {} devices that have been online for more than 8 hours.
    There are {} devices that have been online for more than 24 hours.
    There are {} devices that have been online for atleast a week.
    There are {} devices that have been online for atleast a month.
    """.format(count, count2, count3, count4, count5, count6, count7))
    label.pack()

#create a button to display results that is centered on the page
button = tk.Button(window, text="Display Results", command=display_results)
button.pack()


#close tkinter window
window.mainloop()
