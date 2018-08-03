from .encounter import Encounter
from dictionaries import xp_values


class DirectedEncounter(Encounter):
    def __init__(self, encounter_level, style=None):
        super().__init__(encounter_level)
        styles_dict = {'boss': {'roles': self.boss_roles, 'xp_budget_multiplier': 1.6},
                'basic': {'roles': self.basic_roles, 'xp_budget_multiplier': 0.8}
        }
        self.style = style
        self.right_role = styles_dict[self.style]['roles']
        self.xp_budget = xp_values[encounter_level] * styles_dict[self.style]['xp_budget_multiplier']
        self.occurrence = 'rare'

    def boss_roles(self, monster):
        if self.role_counts['leader'] == 0:
            return monster['role'] == 'leader'
        else:
            return super(DirectedEncounter, self).right_role(monster)

    def basic_roles(self, monster):
        if monster['role'] in ['leader', 'pet']:
            return False
        else:
            return super(DirectedEncounter, self).right_role(monster)
