import os
import requests
import mysql.connector
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta
from IPython.display import display

# connect to the database
load_dotenv()

connect = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# set up the cursor
cr = connect.cursor()


query_create = '''
CREATE TABLE IF NOT EXISTS matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    team_A VARCHAR(50),
    team_B VARCHAR(50),
    score_A INT,
    score_B INT,
    status VARCHAR(25),
    date DATE,
    time TIME,
    period VARCHAR(2),
    championship_title VARCHAR(50),
    round_number VARCHAR(25),
    channel VARCHAR(50)
);
'''
cr.execute(query_create)
connect.commit()






def insert(team_A, team_B, score_A, score_B, status, date, time, period, championship_title, round_number, channel):
        query_insert = '''
        INSERT INTO matches (team_A, team_B, score_A, score_B, status, date, time, period, championship_title, round_number, channel)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        cr.execute(query_insert, (team_A, team_B, score_A, score_B, status, date, time, period, championship_title, round_number, channel))
        connect.commit()



# defining the main function
def get_matches_info(start_date, end_date):

    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    current_date = start_date

    while current_date <= end_date:

        # put the date in the suitable format
        formatted_date = current_date.strftime('%m/%d/%Y')

        # getting the page by "requests"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"}
        page = requests.get(f"https://www.yallakora.com/match-center?date={formatted_date}", headers=headers)

        # organise the data from the website by BeautifulSoup
        src = page.content
        soup = BeautifulSoup(src, "lxml")   # put the code in HTML form

        # searching for all the data
        championships = soup.find_all('div', {'class': 'matchCard'})

        # extracitng each championship info on its own
        for championship in championships:

                championship_title_div = championship.find("div", {'class': 'title'}).find('h2')
                championship_title = championship_title_div.text.strip() if championship_title_div else None

                rounds = championship.find_all("div", {'class': 'allData'})

                # extracitng each championship rounds
                for round in rounds:
                        
                        try:

                                team_A_div = round.find('div', {'class': 'teamA'})
                                team_B_div = round.find('div', {'class': 'teamB'})
                                team_A = team_A_div.text.strip() if team_A_div else None
                                team_B = team_B_div.text.strip() if team_B_div else None

                                scores = round.find_all('span', {'class': 'score'})
                                if len(scores) == 2:
                                        score_A = scores[0].text.strip()
                                        score_B = scores[1].text.strip()
                                        score_A = int(score_A) if score_A.isdigit() else None
                                        score_B = int(score_B) if score_B.isdigit() else None
                                else:
                                        score_A = None
                                        score_B = None
                                
                                date = current_date.date()
                                time_span = round.find('span', {'class': 'time'})
                                time_str = time_span.text if time_span else None
                                hour_12_str = '12:00'
                                time_as_datetime = datetime.strptime(f"{formatted_date} {time_str}", '%m/%d/%Y %H:%M')
                                hour_12_as_datetime = datetime.strptime(f"{formatted_date} {hour_12_str}", '%m/%d/%Y %H:%M')
                                
                                if time_as_datetime < hour_12_as_datetime:
                                        time = time_as_datetime.strftime('%H:%M')
                                        period = "AM"

                                elif time_as_datetime >= hour_12_as_datetime:
                                        delta = time_as_datetime - hour_12_as_datetime
                                        delta_as_time = (datetime.min + delta).time()
                                        time = delta_as_time.strftime('%H:%M')
                                        period = "PM"

                                round_num_div = round.find('div', {'class': 'date'})
                                round_number = round_num_div.text if round_num_div else None
                                
                                channel_div = round.find('div', {'class': 'channel icon-channel'})
                                channel = channel_div.text if channel_div else None

                                status_div = round.find('div', {'class': 'matchStatus'})
                                status = status_div.text if status_div else None

                                insert (team_A, team_B, score_A, score_B, status, date, time, period, championship_title, round_number, channel)

                        
                        except Exception as e:
                                print("="*100)
                                print(f"- Error on {current_date.strftime('%m/%d/%Y')}")
                                print(f"- Skipped match due to: {e}")
                                print("="*100)


        # increasing current_date by 1 day
        current_date += timedelta(days=1)












get_matches_info("6/16/2025", "6/17/2025")