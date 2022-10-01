import pathlib

path_file = pathlib.Path("file.txt")

route = pathlib.Path(__file__).parents[1]
db_route = route.joinpath("database", "dbproject.sqlite")
