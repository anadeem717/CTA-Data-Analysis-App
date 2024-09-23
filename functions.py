import sqlite3
import matplotlib.pyplot as figure

# set up sqlite
dbConn = sqlite3.connect("CTA2_L_daily_ridership.db")
dbCursor = dbConn.cursor()


def printGeneralStats():
    """
    Fetch and display general statistics about the database, including:
    - Number of stations
    - Number of stops
    - Total ride entries
    - Date range of the data
    - Total ridership count
    """

    # Get number of stations
    numStations_SQL = "SELECT COUNT(*) FROM Stations;"
    dbCursor.execute(numStations_SQL)
    row = dbCursor.fetchone()
    print("   # of stations:", row[0])

    # Get number of stops
    numStops_SQL = "SELECT COUNT(*) FROM Stops;"
    dbCursor.execute(numStops_SQL)
    row = dbCursor.fetchone()
    print("   # of stops:", row[0])

    # Get number of ride entries
    numEntries_SQL = "SELECT COUNT(*) FROM Ridership;"
    dbCursor.execute(numEntries_SQL)
    row = dbCursor.fetchone()
    print("   # of ride entries:", f"{row[0]:,d}")

    # Get the date range
    earliestDate_SQL = """
                       SELECT Date(Ride_Date) as Date FROM Ridership
                       GROUP BY Date
                       ORDER BY Date ASC;
                       """
    dbCursor.execute(earliestDate_SQL)
    row = dbCursor.fetchall()

    earliestDate = row[0][0] # first entry is earliest date
    latestDate = row[-1][0]  # last entry is the latest date

    print("   date range: " + earliestDate + " - " + latestDate)

    # Get total Ridership
    numRides_SQL = "SELECT SUM(Num_Riders) FROM Ridership;"
    dbCursor.execute(numRides_SQL)
    row = dbCursor.fetchone()
    print("   Total ridership:", f"{row[0]:,d}")


def findStations(stationName) -> bool:
    """
    Find and display station names matching the given stationName.

    Args:
    stationName (str): The name or partial name of the station to search for.
    
    Returns:
    bool: True if stations found, False otherwise.
    """

    # Query to find stations with a name similar to the user input
    findStations_SQL = """
                       SELECT Station_ID, Station_Name FROM Stations
                       WHERE Station_Name LIKE ?
                       GROUP BY Station_ID
                       ORDER BY Station_Name ASC;
                       """
    dbCursor.execute(findStations_SQL, [stationName])
    result = dbCursor.fetchall()

    if not result:
        return False

    # Display the matching stations
    for row in result:
        print(row[0], ":", row[1])


# Find number and percentage of riders for weekdays, Saturdays, and Sundays/holidays
def findPercentageRiders(stationName):
    """
    Fetch and display the percentage of ridership for weekdays, Saturdays, 
    and Sundays/holidays for a given station.
    
    Args:
    stationName (str): The name of the station to analyze.
    """

    # Query to find total riders for the station
    totalRiders_SQL = """
                      SELECT SUM(Num_Riders) as Total FROM Stations
                      JOIN Ridership 
                      ON Stations.Station_ID = Ridership.Station_ID
                      WHERE Station_Name = ?
                      """
    dbCursor.execute(totalRiders_SQL, [stationName])
    totalRiders = (dbCursor.fetchone())[0]

    if not totalRiders:
        print("**No data found...")
        return

    # Queries to find ridership for different days
    numRidersWeekday_SQL = """
                           SELECT SUM(Num_Riders) as Total FROM Stations
                           JOIN Ridership 
                           ON Stations.Station_ID = Ridership.Station_ID
                           WHERE Station_Name = ?
                           AND Type_of_Day = 'W'
                           """
    dbCursor.execute(numRidersWeekday_SQL, [stationName])
    weekdayRes = (dbCursor.fetchone())[0]

    numRidersSaturday_SQL = """
                            SELECT SUM(Num_Riders) as Total FROM Stations
                            JOIN Ridership 
                            ON Stations.Station_ID = Ridership.Station_ID
                            WHERE Station_Name = ?
                            AND Type_of_Day = 'A'
                            """
    dbCursor.execute(numRidersSaturday_SQL, [stationName])
    saturdayRes = (dbCursor.fetchone())[0]

    numRidersSunday_SQL = """
                          SELECT SUM(Num_Riders) as Total FROM Stations
                          JOIN Ridership 
                          ON Stations.Station_ID = Ridership.Station_ID
                          WHERE Station_Name = ?
                          AND Type_of_Day = 'U'
                          """
    dbCursor.execute(numRidersSunday_SQL, [stationName])
    sundayRes = (dbCursor.fetchone())[0]

    # Display percentage ridership for the station
    print(f"Percentage of ridership for the {stationName} station: ")
    print(
        "  Weekday ridership:",
        f"{weekdayRes:,}",
        f"({(weekdayRes/totalRiders)*100:.2f}%)",
    )
    print(
        "  Saturday ridership:",
        f"{saturdayRes:,}",
        f"({(saturdayRes/totalRiders)*100:.2f}%)",
    )
    print(
        "  Sunday/holiday ridership:",
        f"{sundayRes:,}",
        f"({(sundayRes/totalRiders)*100:.2f}%)",
    )
    print("  Total ridership:", f"{totalRiders:,}")


def stationRidershipWeekdays():
    """
    Fetch and display weekday ridership for all stations,
    along with the percentage of total weekday ridership.
    """

    # Query to find total weekday ridership
    numRidersWeekday_SQL = """
                           SELECT SUM(Num_Riders) as Total FROM Stations
                           JOIN Ridership 
                           ON Stations.Station_ID = Ridership.Station_ID
                           AND Type_of_Day = 'W'
                           """
    dbCursor.execute(numRidersWeekday_SQL)
    totalRidersWeekday = (dbCursor.fetchone())[0]

    # Query to find weekday ridership for each station
    weekdayRiderAllStations_SQL = """
                                  SELECT Station_Name, SUM(Num_Riders) as Total 
                                  FROM Stations JOIN Ridership 
                                  ON Stations.Station_ID = Ridership.Station_ID
                                  AND Type_of_Day = 'W'
                                  GROUP BY Station_Name
                                  ORDER BY Total DESC
                                  """
    dbCursor.execute(weekdayRiderAllStations_SQL)
    res = dbCursor.fetchall()

    # Display ridership for each station
    print("Ridership on Weekdays for Each Station")
    for row in res:
        print(row[0], ":", f"{row[1]:,d}", f"({(row[1]/totalRidersWeekday)*100:.2f}%)")



def checkIfLineExists(lineColor) -> bool:
    """
    Checks if a specific line exists in the Lines DB

    Args:
    lineColor (str): The color of the line.

    Returns:
    bool: True if line exists, false otherwise
    """
    
    checkLine_SQL = """
                    SELECT Color FROM Lines
                    WHERE Color LIKE ?
                    """
    dbCursor.execute(checkLine_SQL, [lineColor])
    res = dbCursor.fetchone()

    if res is None:
        return False


def lineStops(lineColor, direction) -> bool:
    """
    Fetch and display all stops for a given line color and direction,
    along with ADA information.

    Args:
    lineColor (str): The color of the line.
    direction (str): The direction of the line (N/S/W/E).

    Returns:
    bool: True if stops are found, False oth  erwise.
    """

    # SQL query to fetch stop names and ADA accessibility for the given line and direction
    lineStops_SQL = """
                    SELECT Stop_Name, ADA FROM Stops
                    JOIN StopDetails 
                    ON Stops.Stop_ID = StopDetails.Stop_ID
                    JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID
                    WHERE Color LIKE ?
                    AND Direction LIKE ?
                    GROUP BY Stop_Name
                    ORDER BY Stop_Name ASC
                    """
    
    # Execute the query with the specified line color and direction
    dbCursor.execute(lineStops_SQL, [lineColor, direction])
    res = dbCursor.fetchall()

    # Return False if no stops are found
    if not res:
        return False
    else:
        # Iterate through the results and print stop details with accessibility info
        for row in res:
            if row[1] == 1:
                print(
                    row[0], ": direction =", direction.upper(), "(handicap accessible)"
                )
            else:
                print(
                    row[0],
                    ": direction =",
                    direction.upper(),
                    "(not handicap accessible)",
                )



def numStopsEachLine():
    """
    Fetch and display the number of stops for each line color, organized by direction,
    and the percentage of total stops for each line color and direction combination.
    
    Returns:
    None
    """

    # SQL query to get the number of stops for each line color and direction
    numStopsLine_SQL = """
                       SELECT Color, Direction, COUNT(Stops.Stop_ID) AS NumStops 
                       FROM Stops
                       JOIN StopDetails 
                       ON Stops.Stop_ID = StopDetails.Stop_ID
                       JOIN Lines ON StopDetails.Line_ID = Lines.Line_ID
                       GROUP BY Color, Direction
                       ORDER BY Color ASC, Direction ASC
                       """
    
    # Execute the query to fetch the number of stops for each line and direction
    dbCursor.execute(numStopsLine_SQL)
    res = dbCursor.fetchall()

    # SQL query to get the total number of stops across all lines
    numStops_SQL = "SELECT COUNT(*) FROM Stops;"
    
    # Execute the query to fetch the total number of stops
    dbCursor.execute(numStops_SQL)
    stops = dbCursor.fetchone()

    # Output the number of stops for each color by direction
    print("Number of Stops For Each Color By Direction")
    for row in res:
        # Print color, direction, number of stops, and percentage of total stops
        print(row[0], "going", row[1], ":", row[2], f"({(row[2]/stops[0])*100:.2f}%)")


def totalRidershipYear(stationName):
    """
    Fetches and displays the total ridership per year for a specified station.
    Optionally plots the ridership trend over the years

    Parameters:
    stationName (str): The name of the station for which the ridership data is retrieved.

    Returns:
    None
    """

    # SQL query to get the total ridership by year for the given station
    yearlyRidership_SQL = """
                          SELECT strftime('%Y', Ride_Date) as Year, SUM(Num_Riders) as Total, Station_Name
                          FROM Stations JOIN Ridership
                          ON Stations.Station_ID = Ridership.Station_ID
                          WHERE Station_Name LIKE ?
                          GROUP BY Year
                          ORDER BY Year ASC
                          """
    
    # Execute the query with the provided station name
    dbCursor.execute(yearlyRidership_SQL, [stationName])
    res = dbCursor.fetchall()

    # Output yearly ridership for the station
    print(f"Yearly Ridership at {res[0][2]}")  # Access station name from query result
    for row in res:
        print(row[0], ":", f"{row[1]:,}")  # Print year and formatted ridership number

    # Ask user if they want to plot the data
    plot = input("Plot? (y/n) ")

    # If user chooses to plot, prepare data for plotting
    if plot == "y":
        x = []  # Years
        y = []  # Ridership counts

        # Populate x and y with the years and ridership values from the query result
        for row in res:
            x.append(row[0])
            y.append(row[1])

        # Set up the plot labels and title
        figure.xlabel("Year")
        figure.ylabel("Number of Riders")
        figure.title(f"Yearly Ridership at {res[0][2]} Station")
        
        # Plot the data and display the figure
        figure.ioff()
        figure.plot(x, y)
        figure.show()



def monthlyRidership(stationName, year):
    """
    Fetches and displays the total monthly ridership for a specified station in a given year.
    Optionally plots the monthly ridership trend if the user chooses to plot.

    Parameters:
    stationName (str): The name of the station for which the ridership data is retrieved.
    year (str): The year for which the monthly ridership data is retrieved.

    Returns:
    None
    """

    # SQL query to get the monthly ridership for the given station and year
    monthlyRidership_SQL = """
                           SELECT strftime('%m/%Y', Ride_Date) as Month, SUM(Num_Riders) as Total, Station_Name
                           FROM Stations JOIN Ridership
                           ON Stations.Station_ID = Ridership.Station_ID
                           WHERE Station_Name LIKE ?
                           AND strftime('%Y', Ride_Date) = ?
                           GROUP BY Month
                           ORDER BY Month ASC
                           """

    # Execute the query with station name and year as parameters
    dbCursor.execute(monthlyRidership_SQL, [stationName, year])
    res = dbCursor.fetchall()

    # If no results, display a message, otherwise show ridership data
    if not res:
        print(f"Monthly Ridership at {stationName} for {year}")
    else:
        print(f"Monthly Ridership at {res[0][2]} for {year}")  # Access station name from query result
        for row in res:
            print(row[0], ":", f"{row[1]:,}")  # Print month and formatted ridership number

    # Ask user if they want to plot the data
    plot = input("\nPlot? (y/n) ")

    # If user chooses to plot, prepare data for plotting
    if plot == "y":
        x = []  # Months
        y = []  # Ridership counts

        # Populate x and y with months and ridership values from query result
        for row in res:
            x.append(row[0][:2]) # only takes the month from the date str
            y.append(row[1])

        # Set up plot labels and title
        figure.xlabel("Month")
        figure.ylabel("Number of Riders")
        figure.title(f"Monthly Ridership at {res[0][2]} Station ({year})")

        # Plot the data and display the figure
        figure.ioff()
        figure.plot(x, y)
        figure.show()



def compareRidership(station1, station2, year):
    """
    Compares the daily ridership between two stations for a given year. 
    Displays the first and last five days of ridership data for both stations 
    and offers the option to plot the ridership trends.

    Parameters:
    station1 (str): The name of the first station for comparison.
    station2 (str): The name of the second station for comparison.
    year (str): The year for which the ridership data is retrieved.

    Returns:
    None
    """

    # SQL query to get daily ridership for a specific station in the given year
    stationRidership_SQL = """
                           SELECT strftime('%Y-%m-%d', Ride_Date) as Date, 
                           SUM(Num_Riders) as Total, Stations.Station_ID, Station_Name
                           FROM Stations JOIN Ridership
                           ON Stations.Station_ID = Ridership.Station_ID
                           WHERE Station_Name LIKE ?
                           AND strftime('%Y', Ride_Date) = ?
                           GROUP BY Date
                           ORDER BY Date ASC
                           """

    # Execute the SQL query for the first station
    dbCursor.execute(stationRidership_SQL, [station1, year])
    res1 = dbCursor.fetchall()

    # Execute the SQL query for the second station
    dbCursor.execute(stationRidership_SQL, [station2, year])
    res2 = dbCursor.fetchall()

    # Display station info and the first and last five days of ridership for station 1
    print("Station 1:", f"{res1[0][2]}", f"{res1[0][3]}")
    for row in res1[:5]:  # First 5 days
        print(row[0], f"{row[1]}")
    for row in res1[-5:]:  # Last 5 days
        print(row[0], f"{row[1]}")

    # Display station info and the first and last five days of ridership for station 2
    print("Station 2:", f"{res2[0][2]}", f"{res2[0][3]}")
    for row in res2[:5]:  # First 5 days
        print(row[0], f"{row[1]}")
    for row in res2[-5:]:  # Last 5 days
        print(row[0], f"{row[1]}")

    # Ask the user if they want to plot the ridership data
    plot = input("Plot? (y/n) ")

    # If user chooses to plot, prepare data for plotting
    if plot == "y":
        x = []   # Dates for station 1
        y = []   # Ridership counts for station 1
        x2 = []  # Dates for station 2
        y2 = []  # Ridership counts for station 2

        day = 1 # counter for what day we are appending to the figure
        # Populate x and y with data from station 1
        for row in res1:
            x.append(day)
            y.append(row[1])
            day += 1

        day = 1 # reset the day counter
        # Populate x2 and y2 with data from station 2
        for row in res2:
            x2.append(day)
            y2.append(row[1])
            day += 1

        # Set up plot labels, title, and legend
        figure.xlabel("Day")
        figure.ylabel("Number of Riders")
        figure.title(f"Ridership Each Day of {year}")
        figure.plot(x, y, label=res1[0][3])   # Plot for station 1
        figure.plot(x2, y2, label=res2[0][3]) # Plot for station 2
        figure.legend()  # Display the legend for station names
        

        # Show the plot
        figure.ioff()
        figure.show()



def checkIfStationExists(stationName) -> bool:
    """
    Helper function to check if a station exists in the database. 
    It verifies if there is exactly one matching station. 
    If multiple stations or none are found, it returns False and provides a message.
    
    Parameters:
    stationName (str): The name of the station to check.
    
    Returns:
    bool: True if exactly one station is found, False otherwise.
    """

    # SQL query to check if the station exists and is unique in the database
    checkStations_SQL = """
                        SELECT Station_Name FROM Stations
                        WHERE Station_Name LIKE ?
                        GROUP BY Station_Name
                        """
    
    # Execute the SQL query with the provided station name
    dbCursor.execute(checkStations_SQL, [stationName])
    res = dbCursor.fetchall()

    # If multiple stations are found, return False and notify the user
    if len(res) > 1:
        print("**Multiple stations found...")
        return False

    # If no station is found, return False and notify the user
    if not res:
        print("**No station found...")
        return False

    # If exactly one station is found, return True
    return True



def findNearbyStations(latitude, longitude):
    """
    Finds and displays stations within a mile of the specified latitude and longitude.
    Optionally plots the stations on a map if requested.
    
    Parameters:
    latitude (float): The latitude point.
    longitude (float): The longitude point.
    
    Returns:
    None
    """

    # Degrees of latitude and longitude corresponding to approximately one mile
    latitudeMin = round(latitude - 1 / 69, 3)
    latitudeMax = round(latitude + 1 / 69, 3)
    longitudeMin = round(longitude - 1 / 51, 3)
    longitudeMax = round(longitude + 1 / 51, 3)

    # SQL query to find nearby stations within the specified latitude and longitude bounds
    findNearbyStations_SQL = """
                             SELECT Station_Name, Latitude, Longitude
                             FROM Stations JOIN Stops
                             ON Stations.Station_ID = Stops.Station_ID
                             WHERE Latitude >= ? AND Latitude <= ?
                             AND Longitude >= ? AND Longitude <= ?
                             GROUP BY Station_Name, Latitude, Longitude
                             ORDER BY Station_Name ASC, Latitude DESC
                             """

    # Execute the SQL query with the calculated bounds
    dbCursor.execute(
        findNearbyStations_SQL, [latitudeMin, latitudeMax, longitudeMin, longitudeMax]
    )
    res = dbCursor.fetchall()

    # Check if any stations were found
    if not res:
        print("**No stations found...")
        return

    # Print the list of nearby stations
    print("\nList of Stations Within a Mile")
    for row in res:
        print(row[0], ":", f"({row[1]}, {row[2]})")

    # Prompt the user to plot the stations on a map
    plot = input("Plot? (y/n) ")

    if plot == "y":
        x = []  # List to store longitudes
        y = []  # List to store latitudes

        # Populate the lists with latitude and longitude of each station
        for row in res:
            x.append(row[2])
            y.append(row[1])

        # Load and display the map image
        image = figure.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
        figure.imshow(image, extent=xydims)

        figure.title("Stations Near You")

        # Plot the stations on the map
        figure.plot(x, y, 'o')

        # Annotate each point with the station name
        for row in res:
            figure.annotate(row[0], (row[2], row[1]))
            figure.xlim([-87.9277, -87.5569])
            figure.ylim([41.7012, 42.0868])

        # Show the plotted map
        figure.show()