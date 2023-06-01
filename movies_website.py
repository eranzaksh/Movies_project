
MOVIE_URL = f"https://www.imdb.com/title/"
def writing_webpage(output):
    """
    Writing the html files needed for the website, replacing the templates htmls
    """
    with open("index_template.html", 'r') as fileobj:
        template = fileobj.read()
    new_template = template.replace("__TEMPLATE_MOVIE_GRID__", output)
    with open("movies.html", 'w') as fileobj:
        fileobj.write(new_template)

    with open("movies.html", 'r') as fileobj:
        template = fileobj.read()
    new_template = template.replace("__TEMPLATE_TITLE__", "My movie app")
    with open("movies.html", 'w') as fileobj:
        fileobj.write(new_template)


def serialize_movies(movie, stats):
    """
    Getting a movie name and a dict of stats. Creating an html <li> using the movie name and all
    the stats parameters, saving it to the output then return it
    """
    output = ""
    title = movie
    rating = stats['Ratings']
    year = stats['Year']
    poster = stats['Poster']
    imdb_page = stats['Page']
    if 'Notes' not in stats:
        notes = ""
    else:
        notes = stats['Notes']
    output += """<li>                                            
                <div class="movie">
                    <a href={}>
                    <span class="hovertext" data-hover="{}">                          
                    <img class="movie-poster" src={}></a>
                     </span>                             
                    <div class="movie-title">{}</div>            
                    <div class="movie-year">{}</div>             
                    <div class="movie-year">IMDB score: {}</div> 
                </div>                                           
            </li>                                                
            """.format(MOVIE_URL+imdb_page, notes, poster, title, year, rating)
    return output
