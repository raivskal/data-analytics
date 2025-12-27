#Program uses themoviedb.org API to get movie info and export to Excel

import tkinter as tk
import requests
import pandas as pd #for Excel export
import config as cf #api key keeping
import openpyxl #for Excel export
from PIL import ImageTk, Image #for image resizing

api_key = cf.api_key #api key for themoviedb.org API

def get_movie_results(movie): #connecting to online database of movies
    api_version = 3
    api_base_url = f"https://api.themoviedb.org/{api_version}"
    endpoint_path = f"/search/movie"
    endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&query={movie}"
    r = requests.get(endpoint)
    try:
        if r.status_code in range(200,299): #check if connected
            data = r.json()
            results = data['results'] #find key 'results'
            if len(results) >0:
                movie_names = set() #set is for unique values
                movie_ids = set()
                for result in results:
                    _names = f"{result['title']}. Released: {result['release_date']}"
                    _id = result['id']
                    movie_names.add(_names)
                    movie_ids.add(_id)
                result=""
                for j in sorted(movie_names):
                    result+=j + ","
                    result = result.rstrip(",")
                    result +="\n"
            label['text']=result
            return movie_ids 
    except:
        label['text']="Did not find movie"


def export_data(movie_ids): #exports to Excel all data of search results
    output = 'movies.xlsx'
    movie_data = []
    for movie_id in movie_ids:
        api_version = 3
        api_base_url = f"https://api.themoviedb.org/{api_version}"
        endpoint_path = f"/movie/{movie_id}"
        endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
        r = requests.get(endpoint)
        if r.status_code in range(200,299):
            data = r.json()
            movie_data.append(data) #makes list of movie data from api
    df = pd.DataFrame(movie_data) #makes Pandas dataframe from movie data list
    df.to_excel(output, index=False) #creates Excel file from data

#image resizing function, got from StackOverflow
def resizer(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    bg = ImageTk.PhotoImage(image)
    background_label.config(image=bg)
    background_label.image = bg

#GUI with TkInter package
root = tk.Tk()
root.geometry('600x700')

image = Image.open('img2.jpg')
copy_of_image = image.copy()
bg = ImageTk.PhotoImage(image)
background_label = tk.Label(root, image=bg)
background_label.bind('<Configure>', resizer) #uses image resize function according to window size
background_label.pack(fill= "both", expand=True)

frame = tk.Frame(root, bg="#ff9900", bd=5)
frame.place( relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry = tk.Entry(frame, font=('Segoe UI',15))
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text = "Get movie\n names", font=('Segoe UI',12),bg="white", command=lambda: get_movie_results(entry.get())) # temporarly storing at memory, gets current state of textbox
button.place(relx=0.7, relwidth=0.3, relheight=1)

lower_frame = tk.Frame(root, bg="#ff9900", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font=('Segoe UI',12), anchor = 'nw', justify = 'left')
label.place(relwidth=1, relheight=1)

button2 = tk.Button(root, text = "Export data to Excel", bg="white",font=('Segoe UI',12),command=lambda: export_data(get_movie_results(entry.get())))
button2.place(relx = 0.35, rely=0.9)

root.mainloop()