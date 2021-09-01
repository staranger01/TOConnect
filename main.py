import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pylab as plt
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import seaborn as sns
from PIL import Image



try:
    with st.echo(code_location='below'):
        st.title("Discover GTA")
        
        st.title("Discover 222")
        #DATA CLEANING/PROCESSING
        province = ["Ontario"]
        areas = ["Oshawa", "Ajax", "Brampton", "Markham", "Pickering", "Mississsauga", "Toronto"]
        topics = ["Community", "Crime", "Education", "Healthcare"]
        cities= ['Toronto','Durham', 'Etobicoke','Pickering','Brampton','North York', 'Oshawa', 'Mississauga',
                'East York','TORONTO','Ajax','Markham', 'MISSISSAUGA','AJAX', 'PICKERING', 'OSHAWA',
                'York','BRAMPTON', 'SCARBOROUGH', 'Agincourt', 'Rexdale','UNIONVILLE','MARKHAM']

        file_path = 'data/neighbourhood-crime-rates.csv'
        file_path_two = 'data/health_services.csv'
        file_path_3 = 'data/ontbuilds-all-20210604.csv '
        df = pd.read_csv('data/education.csv')
    
        canada = gpd.read_file("./data/gfsa000b11a_e.shp")
        crime_data = pd.read_csv(file_path)
        health_services_data = pd.read_csv(file_path_two)
        df = df.drop(['Region', 'Board Number', 'Board Name','School Number','School Special Conditions Code', 'Suite', 'PO Box',
                    'Phone', 'Fax','School Email', 'School Website',
            'Board Website'], axis = 1)




        health_services_data_cities = health_services_data[health_services_data.COMMUNITY.isin(areas)]



        health_services_data_cities['Post'] = health_services_data_cities['POSTALCODE'].str[:3]
        ontario = canada[canada['PRUID'] == '35']
        health_ontario=ontario.join(health_services_data_cities.set_index('Post'), on='CFSAUID',how='inner', )


        dffilt = df[df['City'].isin(cities)]
        newdff = dffilt.replace({'City' : { 'OSHAWA' : 'Oshawa', 'AJAX' : 'Ajax', 'PICKERING' : 'Pickering', 'UNIONVILLE': 'MARKHAM',
                                        'MISSISSAUGA': 'Mississauga', 'BRAMPTON':'Brampton', 'East York': 'Toronto',
                                        'Agincourt': 'Toronto', 'Etobicoke': 'Toronto', "Rexdale" : "Brampton",
                                        'North York': 'Toronto', 'SCARBOROUGH': 'Toronto', 'TORONTO': 'Toronto',
                                        'MARKHAM':'Markham', "York": 'Toronto','Missisauga':'Mississauga'}})


        pop = pd.read_csv('data/population.csv')

        newdff["Population 0 to 14"] = 0
        newdff["Population 14 to 19"] = 0
        newdff["Population 0 to 14"][newdff['City'].str.contains("Ajax")] = 23660
        newdff["Population 14 to 19"][newdff['City'].str.contains("Ajax")] = 8535

        newdff["Population 0 to 14"][newdff['City'].str.contains("Brampton")] = 120245
        newdff["Population 14 to 19"][newdff['City'].str.contains("Brampton")] = 42820

        newdff["Population 0 to 14"][newdff['City'].str.contains("Markham")] = 55390
        newdff["Population 14 to 19"][newdff['City'].str.contains("Markham")] = 21095

        newdff["Population 0 to 14"][newdff['City'].str.contains("Mississauga")] = 120925
        newdff["Population 14 to 19"][newdff['City'].str.contains("Mississauga")] = 49205

        newdff["Population 0 to 14"][newdff['City'].str.contains("Oshawa")] = 26575
        newdff["Population 14 to 19"][newdff['City'].str.contains("Oshawa")] = 9220

        newdff["Population 0 to 14"][newdff['City'].str.contains("Pickering")] = 14915
        newdff["Population 14 to 19"][newdff['City'].str.contains("Pickering")] = 6290

        newdff["Population 0 to 14"][newdff['City'].str.contains("Toronto")] = 398135
        newdff["Population 14 to 19"][newdff['City'].str.contains("Toronto")] = 145525
        city_count = newdff['City'].value_counts()
        newdff["total schools"] = 0
        newdff["total schools"][newdff['City'].str.contains("Ajax")] = 760

        newdff["total schools"][newdff['City'].str.contains("Brampton")] = 281

        newdff["total schools"][newdff['City'].str.contains("Markham")] = 204

        newdff["total schools"][newdff['City'].str.contains("Mississauga")] = 88

        newdff["total schools"][newdff['City'].str.contains("Oshawa")] = 71

        newdff["total schools"][newdff['City'].str.contains("Pickering")] = 48

        newdff["total schools"][newdff['City'].str.contains("Toronto")] = 28

        newdff['total child population'] = newdff['Population 0 to 14'] + newdff['Population 14 to 19']
        newdff['percapita ratio'] = newdff['total schools'] / newdff['total child population']

        newdff['Elementary counts'] = 0
        newdff['Secondary counts'] = 0
        newdff['Elem/Sec counts'] = 0

        newdff['Elementary counts'][newdff['City'].str.contains("Ajax")] = 36
        newdff['Secondary counts'][newdff['City'].str.contains("Ajax")] = 11
        newdff['Elem/Sec counts'][newdff['City'].str.contains("Ajax")] =1

        newdff['Elementary counts'][newdff['City'].str.contains("Brampton")] = 155
        newdff['Secondary counts'][newdff['City'].str.contains("Brampton")] = 49

        newdff['Elementary counts'][newdff['City'].str.contains("Markham")] = 51
        newdff['Secondary counts'][newdff['City'].str.contains("Markham")] = 17
        newdff['Elem/Sec counts'][newdff['City'].str.contains("Markham")] =3

        newdff['Elementary counts'][newdff['City'].str.contains("Mississauga")] = 212
        newdff['Secondary counts'][newdff['City'].str.contains("Mississauga")] = 63
        newdff['Elem/Sec counts'][newdff['City'].str.contains("Mississauga")] =6

        newdff['Elementary counts'][newdff['City'].str.contains("Oshawa")] = 54
        newdff['Secondary counts'][newdff['City'].str.contains("Oshawa")] = 28
        newdff['Elem/Sec counts'][newdff['City'].str.contains("Oshawa")] =6

        newdff['Elementary counts'][newdff['City'].str.contains("Pickering")] = 22
        newdff['Secondary counts'][newdff['City'].str.contains("Pickering")] = 6

        newdff['Elementary counts'][newdff['City'].str.contains("Toronto")] = 559
        newdff['Secondary counts'][newdff['City'].str.contains("Toronto")] = 194
        newdff['Elem/Sec counts'][newdff['City'].str.contains("Toronto")] =7

        newdff['ratio of elementary schools to kids 0-14'] = (newdff['Elementary counts']+newdff['Elem/Sec counts']) / newdff['Population 0 to 14']
        newdff['ratio of secondary schools to kids 15-19'] = (newdff['Secondary counts']+newdff['Elem/Sec counts']) / newdff['Population 14 to 19']
        newdff['ratio of secondary schools to kids 15-19'] = newdff['ratio of secondary schools to kids 15-19'] *1000
        newdff['ratio of elementary schools to kids 0-14'] = newdff['ratio of elementary schools to kids 0-14'] *1000
        canada = gpd.read_file("data/gfsa000b11a_e.shp")
        ontario_new = canada[canada['PRUID'] == '35']


        newdff['Post'] = newdff['Postal Code'].str[:3]

        new_dff=ontario_new.join(newdff.set_index('Post'), on='CFSAUID', how='inner')

        newdff= new_dff[new_dff.CFSAUID != 'N0A']
        newdff= newdff[newdff.CFSAUID != 'N0G']
        newdff= newdff[newdff.CFSAUID !=  'L4N']


        #communityinvestments data cleaning
        com = pd.read_csv(file_path_3)
        postal =[ 'L1G', 'L1H', 'L1J', 'L1K', 'L1L', 'L1S', 'L1T', 'L1V', 'L1W',
            'L1X', 'L1Z', 'L3P', 'L3R', 'L3S', 'L4B', 'L4T', 'L4W', 'L4X',
            'L4Y', 'L4Z', 'L5A', 'L5B', 'L5C', 'L5E', 'L5G', 'L5H', 'L5J',
            'L5K', 'L5L', 'L5M', 'L5N', 'L5R', 'L5V', 'L5W', 'L6B', 'L6C',
            'L6E', 'L6P', 'L6R', 'L6S', 'L6T', 'L6V', 'L6W', 'L6X', 'L6Y',
            'L6Z', 'L7A', 'L7C', 'M1B', 'M1C', 'M1E', 'M1G', 'M1H', 'M1J',
            'M1K', 'M1L', 'M1M', 'M1N', 'M1P', 'M1R', 'M1S', 'M1T', 'M1V',
            'M1W', 'M2H', 'M2J', 'M2K', 'M2L', 'M2M', 'M2N', 'M2P', 'M2R',
            'M3A', 'M3B', 'M3C', 'M3H', 'M3J', 'M3K', 'M3L', 'M3M', 'M3N',
            'M4A', 'M4B', 'M4C', 'M4E', 'M4G', 'M4H', 'M4J', 'M4K', 'M4L',
            'M4M', 'M4N', 'M4P', 'M4R', 'M4S', 'M4T', 'M4V', 'M4W', 'M4X',
            'M4Y', 'M5A', 'M5B', 'M5E', 'M5G', 'M5J', 'M5M', 'M5N', 'M5P',
            'M5R', 'M5S', 'M5T', 'M5V', 'M6A', 'M6B', 'M6C', 'M6E', 'M6G',
            'M6H', 'M6J', 'M6K', 'M6L', 'M6M', 'M6N', 'M6P', 'M6R', 'M6S',
            'M8V', 'M8W', 'M8X', 'M8Y', 'M8Z', 'M9A', 'M9B', 'M9C', 'M9L',
            'M9M', 'M9N', 'M9P', 'M9R', 'M9V', 'M9W']

        com['Post'] = com['Postal Code'].str[:3]
        comfilt = com[com['Post'].isin(postal)] 
        com_df=ontario.join(comfilt.set_index('Post'), on='CFSAUID')
        com_df['esttotal'] = com_df['Estimated Total Budget'].str.replace(',', '').str.replace('$', '')
        com_df= com_df[com_df.Community != 'Sault Ste. Marie']
        com_df= com_df[com_df.Community != 'Minden Hills']
        com_df= com_df[com_df.Community !=  'York']

        cc= com_df[com_df.Category == 'Child care']
        hc= com_df[com_df.Category == 'Health care']
        c= com_df[com_df.Category == 'Communities']
        rc= com_df[com_df.Category == 'Recreation']
        edu= com_df[com_df.Category == 'Education']
        trans= com_df[com_df.Category == 'Transit']



    

        #UX
        st.sidebar.header("Select Region")
        st.sidebar.subheader("Relevant maps will show once region is selected")

        AREAS_SELECTED = st.sidebar.multiselect('', areas)

        # Mask to filter dataframe
        #Education
        mask_cities = newdff['City'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        newdff = newdff[mask_cities]
        #HealthCare
        mask_cities = health_ontario['COMMUNITY'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        health_ontario = health_ontario[mask_cities]
        
        mask_cities = com_df['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        com_df = com_df[mask_cities]

        mask_cities = cc['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        cc = cc[mask_cities]

        mask_cities = hc['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        hc = hc[mask_cities]

        mask_cities = c['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        c = c[mask_cities]

        mask_cities = rc['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        rc = rc[mask_cities]

        mask_cities = edu['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        edu = edu[mask_cities]

        mask_cities = trans['Community'].isin(AREAS_SELECTED )
        st.set_option('deprecation.showPyplotGlobalUse', False)
        trans = trans[mask_cities]








        # Mask to filter dataframe
        #MAP BREAKDOWN OF TYPES OF SCHOOLS ACROSS GTA
        st.sidebar.header("Select Topic")
    
        choice = st.sidebar.radio("Topic", ["Healthcare", "Education", "Community Investment", "Crime"])

        st.set_option('deprecation.showPyplotGlobalUse', False)
        #ontario
        if choice == "Healthcare":
            st.subheader("Healthcare")
            st.write("Key Healthcare services across the GTA. ")
        #HEALTHCARE
            bx = health_ontario.plot(column='SERV_TYPE', categorical=True, cmap = 'OrRd', legend=True, \
                        legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,1),
                                    'fmt': "{:.0f}"}) 

            plt.show()

            st.pyplot()

            st.text("")
            st.text("")
        if choice == "Education":
            st.subheader("Education")

            st.write("Breakdown of Grade ranges of schools across GTA.")
            cx = newdff.plot(column='Grade Range', categorical=True, legend=True, \
                        legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,0.5),
                                    'fmt': "{:.0f}"})

            plt.show()

            st.pyplot()


            st.write("Breakdown of School levels across the GTA.")
            dx = newdff.plot(column='School Level', categorical=True, legend=True, \
                        legend_kwds={'loc': 'center left', 'bbox_to_anchor':(1,0.5),
                                    'fmt': "{:.0f}"})
            plt.show()
            st.pyplot()


            ex = newdff.plot(column='percapita ratio', categorical=False, cmap = 'viridis', legend = True)
            plt.title("Per capita ratio of schools")

            plt.show()
            st.pyplot()
            st.write("We calculated the ratio of schools per number of students present.  A higher number implies that there are more schools available based on the population")
            fx = newdff.plot(column='ratio of elementary schools to kids 0-14', categorical=False, cmap = 'cool', legend = True)
            plt.title("Elementary schools per 1000 kids ages 0-14")
            plt.show()
            st.pyplot()
            st.write("We did a similar calculation for high schools.")
            gx = newdff.plot(column='ratio of secondary schools to kids 15-19', categorical=False, cmap = 'cool', legend = True)
            plt.title("Secondary schools per 1000 kids ages 15-19")
            plt.show()
            st.pyplot()

            st.text("")
            st.text("")
        if choice == "Community Investment":
            st.subheader("Community Investment")
            st.write("Community Projects currently being invested in (as of 2021).")

            category = ['Child care, Health care', 'Education, Communities, Recreation, Transit']

            st.write("As of 2021, here's what different Regions are investing in.  The darker the colour implies that there is more money being invested in that area.")
            hx = com_df.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'OrRd' )
            plt.title("Total amount of money spent on development projects per region")
            plt.show()
            st.pyplot()

            st.write("Spending breakdown by category.  This allows you to see what types of projects communities are invesing in.")
        
            ix = cc.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'GnBu' )
            plt.title("Investments into Child care projects")
            plt.show()
            st.pyplot()



            
            jx = hc.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'Purples' )
            plt.title("Investments into Health care projects")
            plt.show()
            st.pyplot()

            
            kx = c.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'Blues' )
            plt.title("Investments into Community projects")
            plt.show()
            st.pyplot()

            
            lx = rc.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'OrRd' )
            plt.title("Investments into Recreation projects")
            plt.show()
            st.pyplot()


            
            mx = edu.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'Reds' )
            plt.title("Investments into Education projects")
            plt.show()
            st.pyplot()


            
            nx = trans.plot(column='Estimated Total Budget', categorical=False, legend=False,cmap = 'Greens' )
            plt.title("Investments into Transit projects")
            plt.show()
            st.pyplot()

        
        if choice == "Crime":
            st.subheader("Crime Rates in Toronto")
            st.write("Open crime data per region was only available for Toronto")

            autotheft = Image.open('data/autotheft.png')
            st.image(autotheft)

            assault = Image.open('data/assault.png')
            st.image(assault)

            breakin = Image.open('data/breakin.png')
            st.image(breakin)

            homicide = Image.open('data/homicidepic.png')
            st.image(homicide)

            robbery = Image.open('data/robbery.png')
            st.image(robbery)

            shooting = Image.open('data/shooting.png')
            st.image(shooting)
            

except:
    
    st.title("Discover error")