
import click


DEFAULT_AUSGABEVERZEICHNIS = 'pdfs/'


@click.command()
@click.argument('transaktionsdatei', type=click.File('r'))
@click.option('-a', '--ausgabeverzeichnis',
              help='Ausgabeverzeichnis für die fertigen Abrechnungen',
              default=DEFAULT_AUSGABEVERZEICHNIS, type=click.Path(exists=True, writable=True))
@click.version_option()
def cli(transaktionsdatei, ausgabeverzeichnis):
    '''
    Werkzeuge zur Erleichterung der Kassenverwaltung

    (c) Jan-Peer Grunwald, pekh@eufrutki.net
    '''
    click.echo(transaktionsdatei)
    click.echo(ausgabeverzeichnis)
