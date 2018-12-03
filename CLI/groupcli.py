import click
import requests




@click.command()
@click.argument('input')
@click.option(
    '--input', '-a',
    help='Put in your extension to API',
)

def cli(input):
    url = 'localhost:5000/md5'
    params= {input}
    response = requests.get('http://localhost:5000/md5/get',params=input)

    return response.json()
	
def main(input):
  
    output = cli(input)
    print(output)


if __name__ == "__main__":
    main()
