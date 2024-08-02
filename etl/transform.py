from etl.models import Film, PersonData, GenreData


def transform_data_from_db_to_pydantic_models(index_name, data_from_db):
    transformed_data = []
    if index_name == "movies":
        transformed_data = [{"_index": index_name,
                             "_id": str(entry["id"]),
                             "_source": Film(
                                 id=str(entry["id"]),
                                 title=entry["title"],
                                 description=entry["description"],
                                 imdb_rating=entry["rating"],
                                 genres=entry["genres"],
                                 actors=entry["actors"],
                                 directors=entry["directors"],
                                 writers=entry["writers"]
                             ).dict()
                             }
                            for entry in data_from_db]
    elif index_name == "genres":
        transformed_data = [{"_index": index_name,
                             "_id": str(entry["id"]),
                             "_source": GenreData(
                                 id=str(entry["id"]),
                                 name=entry["name"],
                                 description=entry["description"],
                             ).dict()
                             }
                            for entry in data_from_db]
    elif index_name == "persons":
        transformed_data = [{"_index": index_name,
                             "_id": str(entry["id"]),
                             "_source": PersonData(
                                 id=str(entry["id"]),
                                 name=entry["name"],
                             ).dict()
                             }
                            for entry in data_from_db]
    return transformed_data


