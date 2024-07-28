
def group_data_from_db(data_from_db: list) -> dict:
    """
    Function for grouping data from db.
    Raw data from db has a lot of doubles of entries(
    for each genre, for each person).
    :param data_from_db: list
    :return: dict of grouped data
    """

    films = {}
    for entry in data_from_db:
        if str(entry['fw_id']) not in films:
            films[str(entry['fw_id'])] = {'title': entry.get('title'), 'genres_set': set(),
                                          'description': entry.get('description'),
                                          'imdb_rating': entry.get('rating'),
                                          'directors_names': [], 'actors_names': [], 'writers_names': [],
                                          'directors_id': set(), 'actors_id': set(), 'writers_id': set(),
                                          'directors': [], 'actors': [], 'writers': [], 'genres': []}

        film = films[str(entry['fw_id'])]

        if entry['person_id'] and (str(entry['person_id']) not in film[entry['person_role'] + "s_id"]):
            # Add person to set to exclude duplicates.
            film[entry['person_role'] + "s_id"].add(str(entry['person_id']))

            # Add person to the list of directors or actors or writers data.
            person_dict = {'id': str(entry['person_id']), 'name': entry['person_full_name']}
            film[entry['person_role'] + "s"].append(person_dict)

            # Add person to the list of directors or actors or writers names.
            film[entry['person_role'] + "s_names"].append(entry['person_full_name'])

        # Add genre to set for checking existence and to the list for ES.
        if entry['genre_name'] not in film['genres_set']:
            film['genres_set'].add(entry['genre_name'])
            film['genres'].append(entry['genre_name'])

    return films


def transform_data_for_elasticsearch(data_from_db):
    grouped_data_from_db = group_data_from_db(data_from_db)

    data_for_bulk_load_elasticsearch = [
        {"_index": "movies",
         "_id": id,
         "_source": {
            "id": id,
            "imdb_rating": filmwork["imdb_rating"],
            "genres": filmwork["genres"],
            "title": filmwork["title"],
            "description": filmwork["description"],
            "directors_names": filmwork["directors_names"],
            "actors_names": filmwork["actors_names"],
            "writers_names": filmwork["writers_names"],
            "directors": filmwork["directors"],
            "actors": filmwork["actors"],
            "writers": filmwork["writers"]}
         }
        for id, filmwork in grouped_data_from_db.items()
    ]
    return data_for_bulk_load_elasticsearch
