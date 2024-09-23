# Areesh Nadeem
# CTA Database Analysis App
# 9/18/2024
# Summary: Console based program that outputs data from the CTA2 L ridership
#          database. Users can also plot data to view trends. 


import functions


def main():
    """
    Main function to run the CTA L analysis application.
    Provides a menu for users 
    
    Commands:
    1 - Find stations by partial name.
    2 - Analyze ridership percentage for a station.
    3 - View ridership statistics for weekdays.
    4 - List stops for a specific line color and direction.
    5 - Output the number of stops for each line color and direction.
    6 - Output yearly ridership for a specific station.
    7 - Output monthly ridership for a specific year and station.
    8 - Compare daily ridership between two stations for a specific year.
    9 - Find nearby stations within a mile of given latitude and longitude.
    x - Exit the program.
    
    Returns:
    None
    """
    
    print("** Welcome to CTA L analysis app **")

    # Display general statistics
    print("\nGeneral Statistics:")
    functions.printGeneralStats()

    # Loop to handle user commands
    while True:
        # Prompt user for input
        choice = input("\nPlease enter a command (1-9, x to exit): ")

        # Match user input to corresponding case
        match choice:

            case "1":
                print()
                
                # Get partial station name from user and find stations
                stationName = input("Enter partial station name (wildcards _ and %): ")
                if functions.findStations(stationName) == False:
                    print("**No stations found...")

            case "2":
                print()
                
                # Get station name from user and analyze ridership percentage
                stationName = input("Enter the name of the station you would like to analyze: ")
                functions.findPercentageRiders(stationName)

            case "3":
                # Display ridership statistics for weekdays
                functions.stationRidershipWeekdays()

            case "4":
                print()
                
                # Get line color and direction from user, and list stops
                lineColor = input("Enter a line color (e.g. Red or Yellow): ")
                if functions.checkIfLineExists(lineColor) == False:
                    print("**No such line...")
                    continue

                direction = input("Enter a direction (N/S/W/E): ")
                if functions.lineStops(lineColor, direction) == False:
                    print("**That line does not run in the direction chosen...")

            case "5":
                # Output number of stops for each line color and direction
                functions.numStopsEachLine()

            case "6":
                print()
                
                # Get station name from user and output yearly ridership
                stationName = input("Enter a station name (wildcards _ and %): ")
                if functions.checkIfStationExists(stationName) == False:
                    continue
                functions.totalRidershipYear(stationName)

            case "7":
                print()
                
                # Get station name and year from user and output monthly ridership
                stationName = input("Enter a station name (wildcards _ and %): ")
                if functions.checkIfStationExists(stationName) == False:
                    continue
                year = input("Enter a year: ")
                functions.monthlyRidership(stationName, year)

            case "8":
                print()
                
                # Get year and two station names from user, and compare ridership
                year = input("Year to compare against? ")
                print() 

                station1 = input("Enter station 1 (wildcards _ and %): ")
                if functions.checkIfStationExists(station1) == False:
                    continue

                print()

                station2 = input("Enter station 2 (wildcards _ and %): ")
                if functions.checkIfStationExists(station2) == False:
                    continue

                functions.compareRidership(station1, station2, year)

            case "9":
                print()
                
                # Get latitude and longitude from user and find nearby stations
                latitude = float(input("Enter a latitude: "))
                if latitude < 40 or latitude > 43:
                    print("**Latitude entered is out of bounds...")
                    continue

                longitude = float(input("Enter a longitude: "))
                if longitude < -88 or longitude > -87:
                    print("**Longitude entered is out of bounds...")
                    continue

                functions.findNearbyStations(latitude, longitude)

            case "x":
                # Exit the program
                break

            case _:
                # Handle unknown commands
                print("**Error, unknown command, try again...")

# run the program
main()