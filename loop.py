"""Definition Loop. Ulanzi->Solaranzeige Connector V0.43"""

import funktionen

def loop(
    datenbank,
    measurement,
    datenpunkt,
    solaranzeige_url,
    ulanzi_url,
    app_life_time,
    app_scroll_duration,
    app_show_time
):
    """Definition der Loop Funktion! """
    wert = funktionen.db_abfrage(datenbank, measurement, datenpunkt, solaranzeige_url)

    # Ab hier können(müssen) Änderungen/Anpassungen an den jeweiligen "Auswertungen" gemacht werden!
    #
    #

    ################################# Beginn Block Auswertung #################################
    ################################ "solaranzeige,PV,Leistung" ###############################

    if ((wert[0]) + "," + (wert[1]) + "," + (wert[2])) == "solaranzeige,PV,Leistung":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])

        data = {
            "text": str(int(float(wert[3]))) + " W",  # darzustellender Wert/Text
            "lifetime": app_life_time,
            "icon": 27283,  # darzustellendes Icon
            "rainbow": bool(1)
        }

        if 'data' in locals():
            funktionen.ulanzi_senden(url,data,app_scroll_duration,app_show_time)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ########################### solaranzeige,Summen,Wh_GesamtHeute ############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Summen,Wh_GesamtHeute":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])
        data = {
            "text": str(round((float((wert[3])) / 1000), 2)) + " kWh",
            "lifetime": app_life_time,
            "icon": 51301,
            "pushIcon": 2,
            # "blinkText":500,
            "gradient": [[255, 0, 0], [0, 255, 0]]
            # "color": [252, 186, 3]
        }
        if 'data' in locals():
            funktionen.ulanzi_senden(url,data,app_scroll_duration,app_show_time)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ######################### solaranzeige,aktuellesWetter,Temperatur #########################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,aktuellesWetter,Temperatur":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])

        data = {
            "text": "Aussentemp.: " + str(round(float(wert[3]))) + "°C",
            "lifetime": app_life_time,
            "rainbow": bool(1)
        }

        if 'data' in locals():
            funktionen.ulanzi_senden(url,data,app_scroll_duration,app_show_time)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################# "solaranzeige,Service,RaspiTemp" ############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Service,RaspiTemp":
        print(" ** Wert aus DB: "+wert[3])
            
        url = ulanzi_url + "/api/indicator2"
            
        if wert[3] <= str(35):
            data = {"color": [0, 255, 0], "fade": 7000}
        elif wert[3] >= str(36) and wert[3] <= str(50):
            data = {"color": [252, 186, 3], "fade": 3000}
        elif wert[3] >= str(51):
            data = {"color": [255, 0, 0], "blink": 200}

        if 'data' in locals():
            funktionen.ulanzi_senden_raw(url,data)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")

    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################## "solaranzeige,Batterie,Strom" ##############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Batterie,Strom":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/indicator1"

        if round(float(wert[3])) == 0:
            data = {"color": [0, 0, 0]}

        else:
            data = {
                "color": [0, 255, 0],
                # "blink": 1200
                "fade": 5000
            }

        if 'data' in locals():
            funktionen.ulanzi_senden_raw(url,data)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")


    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ############################# "solaranzeige,Service,IntModus" #############################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Service,IntModus":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/indicator3"

        if (wert[3]) == "3":  # Batteriemodus
            data = {"color": [0, 255, 0]}
            funktionen.ulanzi_senden_raw(url, data)

        elif (wert[3]) == "4":  # Line(Netz)modus
            data = {"color": [0, 0, 255]}
            funktionen.ulanzi_senden_raw(url, data)

        elif (wert[3]) == "5":  # Error(Fehler)modus
            data = {"color": [255, 0, 0], "blink": 100}
            funktionen.ulanzi_senden_raw(url, data)

            url = ulanzi_url + "/api/notify"
            data = {
                "text": "Achtung! Wechselrichter befindet sich im Fehlermodus! Bitte überprüfen! ",
                "color": [255, 0, 0],
                "hold": bool(1)
            }

            if 'data' in locals():
                funktionen.ulanzi_senden_raw(url, data)
            else:
                print(" ** -> 'data' wurde nicht korrekt definiert.")


    ################################## Ende Block Auswertung ##################################

    ################################# Beginn Block Auswertung #################################
    ################################ "solaranzeige,Batterie,SOC" #################################

    elif (wert[0]) + "," + (wert[1]) + "," + (wert[2]) == "solaranzeige,Batterie,SOC":
        print(" ** Wert aus DB: "+wert[3])

        url = ulanzi_url + "/api/custom?name=" + (wert[1]) + (wert[2])

        if int(wert[3]) >= 0 and int(wert[3]) <= 10:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 12832,
                "color": [154, 250, 10]
            }

        elif int(wert[3]) >= 11 and int(wert[3]) <= 30:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 6359,
                "color": [154, 250, 10]
            }

        elif int(wert[3]) >= 31 and int(wert[3]) <= 50:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 6360,
                "color": [154, 250, 10]
            }

        elif int(wert[3]) >= 51 and int(wert[3]) <= 70:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 6361,
                "color": [154, 250, 10]
            }

        elif int(wert[3]) >= 71 and int(wert[3]) <= 90:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 6362,
                "color": [154, 250, 10]
            }

        elif int(wert[3]) >= 91 and int(wert[3]) <= 100:
            data = {
                "text": (wert[3]) + " %",
                "progress": (wert[3]),
                "progressc": [0, 255, 0],
                "lifetime": app_life_time,
                "icon": 6363,
                "color": [154, 250, 10]
            }

        if 'data' in locals():
            funktionen.ulanzi_senden(url,data,app_scroll_duration,app_show_time)
        else:
            print(" ** -> 'data' wurde nicht korrekt definiert.")




    ################################## Ende Block Auswertung ##################################

    # ab hier bitte nichts mehr ändern !!!

    else:
        print(
            "Nope, keine Auswertung verfügbar für "
            + str(wert[0])
            + ","
            + str(wert[1])
            + ","
            + (wert[2])
        )


# Ende Loop
