LogFile = "/Users/israndy/Desktop/Superchargers.csv"
username = 'elon@tesla.com'         # Tesla's login, Tesla will prompt for it's password

#
# SuperchargerLog.py  -Randy Spencer 2022   Still crashes daily with TeslaPy connection error
# Script to log the usage at the four Superchargers local to your car.
# Every 5 minutes it wakes your car and queries your closest Superchargers
# and then writes that info to a file on your computer
#

print("\nWaking your car and logging local Superchargers every 5 minutes\n")
import datetime
from time import sleep
from os.path import exists

charge=[]       # List of average Battery Levels to prevent spurious outputs
samples=3       # Number of samples to average
lastcharge=0    # Check and see if we should print the new battery level

# Python3 -m pip install teslapy
print ("Starting connection to Tesla...")
import teslapy
with teslapy.Tesla( username ) as tesla:
    vehicles = tesla.vehicle_list()
    try : car = vehicles[0].get_vehicle_summary()
    except teslapy.HTTPError as e:
        print( "Failed to connect\n", str(e).split("}")[0], "}" )
        sleep(10)
    else :
        print(car['display_name'], "is", car['state'])

    while (True):
        try :
            car = vehicles[0].get_vehicle_summary()
        except teslapy.HTTPError as e:
            print( "Failed to get summary\n", str(e).split("}")[0], "}" )
            sleep( 10 )
            continue
            
        if car['state'] != 'online' :
            print("Waking...")
            try :
                vehicles[0].sync_wake_up()  # Keep car awake for Supercharger logging
            except teslapy.VehicleError as e:
                print( "Wake Timeout\n", str(e).split("}")[0], "}" )
            except teslapy.HTTPError as e:
                print( "Failed to wake\n", str(e).split("}")[0], "}" )
                sleep( 10 )
                continue
                
        try :
            cardata = vehicles[0].get_vehicle_data()
        except teslapy.HTTPError as e:
            print( "Failed to communicate\n", str(e).split("}")[0], "}" )
            sleep( 60 )
            continue
            
        if cardata['charge_state']['battery_level'] < 20 :
            exit("Low Battery, exiting...")
            
        charge.append(cardata['charge_state']['battery_level'])
        if len(charge) == samples + 1 :
            charge.pop(0)
            if lastcharge != int(sum(charge)/samples) :
                lastcharge = int(sum(charge)/samples)
                print("\n", lastcharge, "%\n", sep="")
        elif len(charge) > samples + 1 : charge.clear() # Incase of overrun condition

        output = []
        output.append( str( datetime.datetime.now().strftime( "%Y-%m-%d %H:%M" ) ) )
        try :
            sites=vehicles[0].get_nearby_charging_sites()
            for site in sites['superchargers']:
                output.append( site['name'].split(", ")[0] )
                output.append( str(site['available_stalls']) )
                output.append( str(site['total_stalls']) )
        except teslapy.HTTPError as e:
            print( "Tesla Timeout, wait 3 minutes\n", str(e).split("}")[0], "}" )
            sleep(180)
            continue # back to the top of the order
        
        try:
            if exists(LogFile):
                output_file = open(LogFile, "at")
            else:
                output_file = open(LogFile, "wt")
                print("\nOpened New Superchargers Log File on", LogFile, "\n")
                output_file.write("\"Date\",\"Site 1\",\"Free\",\"Total\",\"Site 2\",\"Free\",\"Total\",\"Site 3\",\"Free\",\"Total\",\"Site 4\",\"Free\",\"Total\"\n""")
                output_file.flush()
        except:
            print("Unable to open or create:", LogFile)
            exit(1)
        else:
            print("Local Superchargers:\n", output)
            # Output the detailed data to a file
            for items in output:
                output_file.write(items)
                output_file.write(",")
            output_file.write("\n")
            # Ensure this latest entry is saved to the file system
            output_file.flush()
            output_file.close()
        sleep( 300 )
