from pathlib import Path

import click
from prettytable import PrettyTable
from tinydb import Query, TinyDB


@click.group()
def main():
    """A command line Elo rating tool"""
    pass


@main.command("create")
@click.argument("name")
@click.option(
    "--p",
    default=Path().cwd(),
    type=click.Path(exists=True, path_type=Path),
    help="default location for table database",
)
def create(name: str, p):
    """create a new Elo rating table"""
    db = TinyDB(p / f"{name}.json")
    if db.all():
        click.echo(
            f"Table with name {name} already exists, either choose a new name or delete current table"
        )
    else:
        click.echo(f"New table created called {name}")


@main.command("show")
@click.argument("table")
@click.option(
    "--p",
    default=Path().cwd(),
    type=click.Path(exists=True, path_type=Path),
    help="default location for table database",
)
def show(table: str, p):
    """display an Elo rating table"""
    db_path = p / f"{table}.json"
    if db_path.exists():
        db = TinyDB(db_path)
        print_table(db)
    else:
        click.echo(f"Table called {name} not found")


@main.command("log")
@click.argument("table")
@click.argument("game")
@click.option("--s", default=400, type=int, help="scale factor for distribution")
@click.option("--k", default=32, type=int, help="k factor for updates")
@click.option("--i", default=400, type=int, help="initial rating for new players")
@click.option(
    "--p",
    default=Path().cwd(),
    type=click.Path(exists=True, path_type=Path),
    help="default location for table database",
)
def log(table: str, game: str, s, k, i, p):
    """log a new game result into a table"""
    db_path = p / f"{table}.json"
    if db_path.exists():
        db = TinyDB(db_path)
        valid_game = split_game_format(game)
        if valid_game:
            update_table(valid_game, db, s, k, i)
        else:
            click.echo(
                f"Game result incorrect format. It must be in the form winner-loser"
            )
    else:
        click.echo(f"Table called {name} not found")


def split_game_format(game: str):
    obj = tuple(game.split("-"))
    if (
        (isinstance(obj, tuple))
        and (len(obj) == 2)
        and (all(isinstance(x, str) for x in obj))
    ):
        return obj
    else:
        return False


def update_table(game: tuple, database: TinyDB, scale: int, kfactor: int, initial: int):
    winner, loser = game
    player = Query()
    if not database.contains(player.name == winner):
        database.insert(
            {"name": winner, "n_played": 0, "n_won": 0, "n_lost": 0, "rating": initial}
        )
    if not database.contains(player.name == loser):
        database.insert(
            {"name": loser, "n_played": 0, "n_won": 0, "n_lost": 0, "rating": initial}
        )
    winner_entry = database.get(player.name == winner)
    loser_entry = database.get(player.name == loser)
    Ra = winner_entry["rating"]
    Rb = loser_entry["rating"]
    winner_played = winner_entry["n_played"] + 1
    loser_played = loser_entry["n_played"] + 1
    winner_won = winner_entry["n_won"] + 1
    loser_lost = loser_entry["n_lost"] + 1
    Ea = 1.0 / (1.0 + 10 ** ((Rb - Ra) / scale))
    Eb = 1.0 / (1.0 + 10 ** ((Ra - Rb) / scale))
    Ra += kfactor * (1 - Ea)
    Rb += kfactor * (0 - Eb)
    database.update(
        {"n_played": winner_played, "n_won": winner_won, "rating": Ra},
        player.name == winner,
    )
    database.update(
        {"n_played": loser_played, "n_lost": loser_lost, "rating": Rb},
        player.name == loser,
    )


def print_table(database: TinyDB):
    table = PrettyTable()
    headers = ["name", "n_played", "n_won", "n_lost", "rating"]
    table.field_names = headers
    for row in database:
        table.add_row([row[h] for h in headers])
    table.sortby = "rating"
    table.reversesort = True
    table.align = "r"
    table.float_format = ".2"
    print(table)
