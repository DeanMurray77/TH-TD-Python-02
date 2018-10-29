import operator
import os


def import_players(file_name):
    # keeping height so that I can sort by height as secondary key later

    # I considered using a dictionary rather than a list,
    # but by defauld dictionaries are unsorted.
    # It appears from what I'm reading online, that there may be a way
    # to sort dictionaries, but I didn't
    # want to get in trouble for using something that hasn't been covered
    # yet it the course, so I used a list of lists.
    players = []
    with open(file_name, "r") as file:
        file_contents = file.read()
    raw_players = file_contents.split(sep='\n')
    for player in raw_players:
        players.append(player.split(sep=','))
    del players[0]
    return players


def sort_players(players):
    # using height as a secondary key (with really
    # young kids, a few inches of height can make a
    # big difference in their athletic ability.
    # This should help make the teams even more even.
    sorted_players = sorted(players,
                            key=operator.itemgetter(2, 1),
                            reverse=True)
    return sorted_players


def split_players(players):
    sharks = []
    dragons = []
    raptors = []

    count_of_players = len(players)
    itterations = count_of_players / 3
    counter = 0
    while counter < itterations:
        index = counter * 3
        sharks.append(players[index])
        dragons.append(players[index + 1])
        raptors.append(players[index + 2])
        counter += 1

    players_dict = {"Sharks": sharks, "Dragons": dragons, "Raptors": raptors}
    return players_dict


def export_team(players_dict):
    with open(TEAM_FILE, "a") as file:
        for team in players_dict:
            file.write(team + "\n")
            for player in players_dict[team]:
                file.write(", ".join(player) + "\n")
            file.write("\n")


def create_welcome_letters(players_dict):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)
        
    for team in players_dict:
        for players in players_dict[team]:
            childs_name_as_file_name = format_childs_name(players[0])
            full_path_file_name = OUTPUT_DIRECTORY + "/" + childs_name_as_file_name
            with open(full_path_file_name, 'w') as file:
                file.write('Dear ' + players[2] + ',\n\n')
                file.write("We're happy to announce that your child," +
                           players[0] +
                           ', has been assigned to a team (the ' + team +
                           ") for this year's youth soccer league.\n\n")
                file.write("Your child's first practice will be held Nov."
                           " 1st at 5:30 pm at Central Park.\n\n")
                file.write("Sincerely,\n\n\nThe Organizing Committee")


def format_childs_name(childs_name):
    return "_".join(childs_name.split()) + ".txt"


def reset_output_file():
    # empty out file from any previous attempts
    file = open(TEAM_FILE, "w")
    file.close()


def remove_heights(players_dict):
    for teams in players_dict:
        for players in players_dict[teams]:
            del players[1]
    return players_dict


if __name__ == '__main__':
    PLAYER_FILE = "soccer_players.csv"
    TEAM_FILE = 'teams.txt'
    OUTPUT_DIRECTORY = 'outputs'

    roster = import_players(PLAYER_FILE)

    roster = sort_players(roster)
    players_dict = split_players(roster)

    # sorting done, height no longer needed. Discarding
    players_dict = remove_heights(players_dict)

    # empty out file from any previous attempts
    reset_output_file()

    export_team(players_dict)
    create_welcome_letters(players_dict)
