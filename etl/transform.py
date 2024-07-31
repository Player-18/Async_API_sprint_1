from typing import Any


def group_movies_data(data_from_db: dict):
    """
    Function for grouping data from db.
    Raw data from db has a lot of doubles of entries(
    for each genre, for each person).
    :param data_from_db:- list
    :return: dict of grouped data
    """

    films = {}
    for entry in data_from_db:
        if str(entry['fw_id']) not in films:
            films[str(entry['fw_id'])] = {'id': entry.get('fw_id'), 'title': entry.get('title'), 'genres_set': set(),
                                          'description': entry.get('description'),
                                          'imdb_rating': entry.get('rating'),
                                          'directors_id': set(), 'actors_id': set(), 'writers_id': set(),
                                          'directors': [], 'actors': [], 'writers': [], 'genres': []}

        film = films[str(entry['fw_id'])]

        if entry['person_id'] and (str(entry['person_id']) not in film[entry['person_role'] + "s_id"]):
            # Add person to set to exclude duplicates.
            film[entry['person_role'] + "s_id"].add(str(entry['person_id']))

            # Add person to the list of directors or actors or writers data.
            person_data = {'id': str(entry['person_id']), 'name': entry['person_full_name']}
            film[entry['person_role'] + "s"].append(person_data)

        # Add genre to set for checking existence and to the list for ES.
        if entry['genre_name'] not in film['genres_set']:
            # Add genre to set to exclude duplicates.
            film['genres_set'].add(entry['genre_name'])

            genre_data = {'id': str(entry['genre_id']), 'name': entry['genre_name']}
            film['genres'].append(genre_data)

    return films.values()


def get_source_for_index(index_name: str, entry: dict) -> dict:
    source = {}

    if index_name == "movies":
        source = {
            "id": entry["id"],
            "imdb_rating": entry["imdb_rating"],
            "genres": entry["genres"],
            "title": entry["title"],
            "description": entry["description"],
            "directors": entry["directors"],
            "actors": entry["actors"],
            "writers": entry["writers"]}
    elif index_name == "genres":
        source = {
            "id": entry["id"],
            "name": entry["name"],
            "description": entry["description"]}
    elif index_name == "persons":
        source = {
            "id": entry["id"],
            "full_name": entry["full_name"]}
    return source


def transform_data_for_elasticsearch(index_name: str, data_from_db: dict):
    if index_name == "movies":
        data_from_db = group_movies_data(data_from_db)
    transformed_data = [
        {"_index": index_name,
         "_id": entry["id"],
         "_source": get_source_for_index(index_name, entry)
         }
        for entry in data_from_db
    ]

    return transformed_data
