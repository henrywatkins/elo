import click
from tinydb import TinyDB, Query

@click.group()
def main():
    """A command line Elo rating tool"""
    pass

@main.command('create')
@click.argument('name')
@click.option('--s', default=400,type=int,help='scale factor for distribution')
@click.option('--k', default=32,type=int,help='k factor for updates')
@click.option('--i', default=400,type=int,help='initial rating for new players')
@click.option('--p', default='db.json', type=click.Path(exists=True), help='default file path for table database')
def create(name: str, s,k,i,p):
    """create a new Elo rating table"""
    #check for existence of db.json, if not, create new tiny db
    db = TinyDB(p)
    #check for table in db, if not create, else show error
    click.echo(f'New table created called {name}')

@main.command('show')
@click.argument('table')
@click.option('--p', default='db.json', type=click.Path(exists=True), help='default file path for table database')
def show(table:str ,p):
    """display an Elo rating table"""
    pass

@main.command('log')
@click.argument('table')
@click.argument('game')
@click.option('--p', default='db.json', type=click.Path(exists=True), help='default file path for table database')
def log(table: str, game: str):
    """log a new game result into a table"""
    pass

@main.command('delete')
@click.argument('table')
@click.option('--p', default='db.json', type=click.Path(exists=True), help='default file path for table database')
def delete(table:str, p):
    """delete a rating table"""
    pass
