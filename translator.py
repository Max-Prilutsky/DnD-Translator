import json
import re

def handle_special_damage(damage_name, damage_variable):
    return [damage_type if not isinstance(damage_type, dict) else ", ".join(damage_type[damage_name]) + damage_type['note'] for damage_type in damage_variable]

def handle_character_options(option_var):
    char_opt = [{"Name": entry['name'], "Content": ", ".join(entry['entries'])} for entry in option_var]
    for each in char_opt:
        each['Content'] = at_rules(each['Content'])
    return char_opt

def at_rules(string):
    string = re.sub('@dc', 'DC', string)
    string = re.sub('@hit ', '+', string)
    string = re.sub('{|}|@h', '', string)
    string = re.sub(r'@[a-zA-Z]* ', '', string)
    return string

def handle_bonuses(bonus_var):
    return [{"Name": stat.capitalize(), "Modifier": int(val)} for stat, val in bonus_var.items()]
     
with open('input.json') as json_file:
    fiveE = json.load(json_file)

    type = fiveE['type']
    hp = fiveE['hp']
    ac = fiveE['ac'][0]

    vulnerable = fiveE.get("vulnerable", [])
    resist = fiveE.get("resist", [])
    immune = fiveE.get("immune", [])
    condImmune = fiveE.get("conditionImmune", [])

    save = fiveE.get('save', {})
    skills = fiveE.get('skill', {})
    senses = fiveE.get("senses", [])
    senses.append(f"passive Perception {fiveE['passive']}")
    languages = fiveE.get('languages', [])
    cr = fiveE.get('cr', "?")
    traits = fiveE.get('trait',[])
    actions = fiveE.get('action', [])
    bonus_actions = fiveE.get('bonus', [])
    leg_actions = fiveE.get("legendary", [])
    reactions = fiveE.get('reaction', [])

    improvedInit = {
        "Type": f"{fiveE['size']}, {type['type']} ({type['tags']})",
        "HP": {
            "Value": hp['average'],
            "Notes": hp['formula']
        },
        "AC": {
            "Value": ac if isinstance(ac, int) else ac['ac'],
            "Notes": ac['from'] if not isinstance(ac, int) else ''
        },
        "InitiativeModifier": (fiveE['dex'] - 10)//2,
        "InitiativeAdvantage": False,
        "Speed": [f'{key} {val} ft' for key, val in fiveE['speed'].items()],
        "Abilities": {
            "Str": fiveE['str'],
            "Dex": fiveE['dex'],
            "Con": fiveE['con'],
            "Int": fiveE['int'],
            "Wis": fiveE['wis'],
            "Cha": fiveE['cha']
        },
        "DamageVulnerabilities": handle_special_damage('vulnerable', vulnerable), 
        "DamageResistances": handle_special_damage('resist', resist), 
        "DamageImmunities": handle_special_damage('immune', immune), 
        "ConditionImmunities": handle_special_damage('conditionImmune', condImmune),
        "Saves": handle_bonuses(save), 
        "Skills": handle_bonuses(skills),
        "Senses": senses,
        "Languages": languages,
        "Challenge": str(cr),
        "Traits": handle_character_options(traits),
        "Actions": handle_character_options(actions),
        "BonusActions": handle_character_options(bonus_actions),
        "Reactions": handle_character_options(reactions),
        "LegendaryActions": handle_character_options(leg_actions),
        "MythicActions": [],
        "Description": "",
        "Player": "",
        "Version": "3.9.0",
        "ImageURL": ""
    }
with open('output.json', 'w') as outfile:
    json.dump(improvedInit, outfile, indent=4)

