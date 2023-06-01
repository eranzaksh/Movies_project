import pytest

from storage_json import StorageJson


def test_add_movie():
    storage = StorageJson('data.json')
    with pytest.raises(Exception):
        storage.add_movie("dfgjdfgj", "imdbRating", 'Year', 'Poster', 'imdbID')
