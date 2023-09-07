from bs4 import BeautifulSoup
import requests

# ⬇ Code for making .csv file

# response = requests.get('https://pokemondb.net/pokedex/national')
#
# response.raise_for_status()
#
# website = response.text
#
# soup = BeautifulSoup(website, 'html.parser')
#
# pokemon = soup.select('.infocard-list > .infocard')
#
# pokemon_names = [name.get_text() for name in soup.select('.infocard-list > .infocard > .infocard-lg-data > a.ent-name')]
#
# pokemon_numbers = [number.get_text() for number in soup.select('.infocard-list > .infocard > .infocard-lg-data > small:first-of-type')]
#
# pokemon_links = ['https://pokemondb.net' + link['href'] for link in soup.select('.infocard-list > .infocard > .infocard-lg-data > a.ent-name')]
#
# with open('pokemon.csv', mode='w', encoding="utf-8") as file:
#     file.write('name,number,link\n')
#
# with open('pokemon.csv', mode='a', encoding="utf-8") as file:
#     for i in range(len(pokemon)):
#         file.write(f'{pokemon_names[i]},{pokemon_numbers[i]},{pokemon_links[i]}\n')

# ⬇ Code for Pokedex

import pandas

data = pandas.read_csv('pokemon.csv')

print('Welcome to the Pokedex!')

pokedex_is_on = True
while pokedex_is_on:
    pokemon_input = input('Enter Pokemon Name or a Number between 1 and 1010\n')

    try:
        pokemon_input = int(pokemon_input)
    except ValueError:
        pass
    else:
        if pokemon_input < 1 or pokemon_input > 1010:
            print('Invalid Input')
            continue
        if pokemon_input < 10:
            pokemon_input = f'#000{pokemon_input}'
        elif pokemon_input < 100:
            pokemon_input = f'#00{pokemon_input}'
        elif pokemon_input < 1000:
            pokemon_input = f'#0{pokemon_input}'
        else:
            pokemon_input = f'#{pokemon_input}'

    if pokemon_input.startswith('#'):
        pokemon = data[data.number == pokemon_input]
    else:
        pokemon_input = pokemon_input.title()
        pokemon = data[data.name == pokemon_input]
        if pokemon.empty:
            print('Invalid Input!')
            continue
    print(f'Name: {pokemon["name"].values[0]}\nNumber in National Dex: {pokemon["number"].values[0]}')

    response = requests.get(pokemon['link'].values[0])

    response.raise_for_status()

    website = response.text

    soup = BeautifulSoup(website, 'html.parser')

    species = soup.find('th', string='Species').find_next('td').get_text()

    print(f'Species: {species}')

    pokemon_type = [t.get_text() for t in soup.select('th + td > a.type-icon')]

    # try:
    #     print(f'Types: {pokemon_type[0]} & {pokemon_type[1]}')
    # except IndexError:
    #     print(f'Type: {pokemon_type[0]}')
    if pokemon_type[0] != pokemon_type[1]:
        t = ', '.join(pokemon_type)
    else:
        t = pokemon_type[0]

    print(f'Type(s): {t}')

    ability = [a.get_text() for a in soup.find('th', string='Abilities').find_next('td').select('a')]

    # try:
    #     print(f'Abilities: {ability[0]} & {ability[1]}')
    # except IndexError:
    #     print(f'Ability: {ability[0]}')

    a = ', '.join(ability)

    print(f'Abilities(s): {a}')

    evolution = soup.select('.infocard-list-evo > .infocard')

    if evolution:
        evolution_chain = []

        for e in evolution:
            p_name = e.select_one('span.infocard-lg-data > a.ent-name')
            if p_name is not None:
                evolution_chain.append(p_name.get_text())
            else:
                p_level = e.find('small').get_text()
                evolution_chain.append(p_level)

        e = ' ➡ '.join(evolution_chain)
        print(f'Evolution Chain:\n{e}')
    else:
        print(f'{pokemon["name"].values[0]} does not evolve.')

