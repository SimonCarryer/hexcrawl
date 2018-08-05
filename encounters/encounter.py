import numpy as np
import yaml
import bisect
from collections import defaultdict
from dictionaries import xp_values

class Encounter:
    def __init__(self, encounter_level):
        self.level = encounter_level
        self.xp_budget = xp_values[encounter_level] * np.random.normal(loc=1.1, scale=0.6)
        self.xp_value = 0
        self.adjusted_xp_value = 0
        self.monster_counts = defaultdict(int)
        self.role_counts = defaultdict(int)
        self.occurrence_counts = defaultdict(int)
        self.probabilities_dict = {'common': 0.6, 'uncommon': 0.3, 'rare': 0.1}
        self.occurrence = np.random.choice(['common', 'uncommon', 'rare'], p=[0.5, 0.3, 0.2])

    def choose_with_probabilities(self, list_of_monsters):
        occurrences = [monster['occurrence'] for monster in list_of_monsters]
        counts = defaultdict(int)
        for occurrence in occurrences:
            counts[occurrence] += 1
        probabilities = [self.probabilities_dict[occurrence] for occurrence in occurrences]
        probabilities = [probability/sum(probabilities) for probability in probabilities]
        return np.random.choice(list_of_monsters, p=probabilities)

    def right_occurrence(self, monster):
        return self.probabilities_dict[monster['occurrence']] >= self.probabilities_dict[self.occurrence]

    def acceptable_challenge(self, monster):
        projected_count = sum(self.monster_counts.values()) + 1
        projected_xp = self.adjust_xp_for_monster_counts(monster['XP'], monster_count=projected_count)
        projected_value = self.adjust_xp_for_monster_counts(self.xp_value, monster_count=projected_count)
        within_budget = projected_xp <= (self.xp_budget - projected_value)
        too_weak = monster['role'] == 'natural hazard' and (monster['XP'] * monster['appearing'][1]) < (self.xp_budget * 0.75)
        return within_budget and not too_weak

    def number_appearing(self, monster):
        return self.monster_counts[monster['Name']] < monster['appearing'][1]

    def right_role(self, monster):
        if monster['role'] == 'environmental hazard':
            return True
        if monster['role'] == 'troops':
            return True
        if monster['role'] == 'elite':
            return (self.role_counts['elite'] == 0 or self.monster_counts[monster['Name']] > 0) and self.role_counts['elite'] < self.role_counts['troops']
        if monster['role'] == 'natural hazard':
            return sum(self.monster_counts.values()) == 0 or self.monster_counts[monster['Name']] > 0
        if monster['role'] == 'leader':
            return self.role_counts['leader'] == 0 and self.role_counts['troops'] > 0
        if monster['role'] == 'pet':
            return self.role_counts['pet'] < (self.role_counts['troops'] / 2)

    def possible_monsters(self, monster_list):
        return [monster for monster in monster_list if self.acceptable_challenge(monster) 
                                                    and self.number_appearing(monster)
                                                    and self.right_role(monster)
                                                    and self.right_occurrence(monster)]

    def add_monster(self, monster):
        self.monster_counts[monster['Name']] += 1
        self.role_counts[monster['role']] += 1
        self.xp_value += monster['XP']
        self.adjusted_xp_value = self.adjust_xp_for_monster_counts(self.xp_value)
        self.occurrence_counts[monster['occurrence']] += 1

    def adjust_xp_for_monster_counts(self, monster_xp, monster_count=None):
        adjustments = [(1, 1), (2, 1.5), (6, 2), (10, 2.5), (14, 3), (1000, 4)]
        if monster_count is None:
            monster_count = sum(self.monster_counts.values())
        adjustment = adjustments[bisect.bisect_left([i[0] for i in adjustments], monster_count)][1]
        return adjustment * monster_xp

    def pick_monsters(self, monster_list):
        monster_min = 0
        possibles = self.possible_monsters(monster_list)
        if len(possibles) == 0:
            print('No appropriate monsters available')
        while self.adjusted_xp_value + monster_min <= self.xp_budget and len(possibles) > 0:
            monster = self.choose_with_probabilities(possibles)
            self.add_monster(monster)
            monster_min = self.adjust_xp_for_monster_counts(min([monster['XP'] for monster in possibles]))
            possibles = self.possible_monsters(monster_list)

    def display(self):
        values = {}
        values['monsters'] = [{'name': key, 'number': value} for key, value in self.monster_counts.items() if value > 0]
        values['xp_value'] = self.xp_value
        return values

