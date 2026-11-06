from pgmpy.models import DiscreteBayesianNetwork 
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import BeliefPropagation
import matplotlib.pyplot as plt
import networkx as nx
from src.preprocess import DIFFICULTY_STATES, LEVEL_STATES, DAYS_STATES, CONCEPTS

DIFFICULTY_PRIOR = [[0.5], [0.5]]

def build_model(): 
    model = DiscreteBayesianNetwork([
        ('Difficulty_C1', 'Mastery_C1'), 
        ('Difficulty_C2', 'Mastery_C2'), 
        ('Difficulty_C3', 'Mastery_C3'), 
        ('Mastery_C1', 'QuizScore_C1'),
        ('Mastery_C2', 'QuizScore_C2'),
        ('Mastery_C3', 'QuizScore_C3'),
        ('Mastery_C1', 'Readiness'),
        ('Mastery_C2', 'Readiness'),
        ('Mastery_C3', 'Readiness'),
        ('Readiness', 'Stress'), 
        ('DaysRemaining', 'Stress')
    ])

    cpds =[] 

    for i in CONCEPTS:
        name = f'Difficulty_C{i}'
        cpds.append(
            TabularCPD(
                variable=name,
                variable_card=len(DIFFICULTY_STATES),
                values=DIFFICULTY_PRIOR,
                state_names={name: DIFFICULTY_STATES}
            )
        )

    for i in CONCEPTS: 
        name = f'QuizScore_C{i}'
        cpds.append(
            TabularCPD(
                variable=name,
                variable_card=len(LEVEL_STATES),
                values=[
                    [0.75, 0.15],  
                    [0.25, 0.85]   
                ],
                evidence=[f'Mastery_C{i}'],
                evidence_card=[len(LEVEL_STATES)],
                state_names={name: LEVEL_STATES, f'Mastery_C{i}': LEVEL_STATES}
            )
        )

    for i in CONCEPTS:
        name = f'Mastery_C{i}'
        cpds.append(
            TabularCPD(
                variable=name,
                variable_card=len(LEVEL_STATES),
                values=[
                    [0.3, 0.65],  
                    [0.7, 0.35]   
                ],
                evidence=[f'Difficulty_C{i}'],
                evidence_card=[len(DIFFICULTY_STATES)],
                state_names={name: LEVEL_STATES, f'Difficulty_C{i}': DIFFICULTY_STATES}
            )
        )

    cpds.append(
        TabularCPD(
            variable='Readiness',
            variable_card=len(LEVEL_STATES),
            values=[
                [0.95, 0.75, 0.75, 0.35, 0.75, 0.35, 0.35, 0.08], 
                [0.05, 0.25, 0.25, 0.65, 0.25, 0.65, 0.65, 0.92]  
            ],
            evidence=[f'Mastery_C{i}' for i in CONCEPTS],
            evidence_card=[len(LEVEL_STATES)] * len(CONCEPTS),
            state_names={'Readiness': LEVEL_STATES, **{f'Mastery_C{i}': LEVEL_STATES for i in CONCEPTS}}
        )
    )

    cpds.append(
        TabularCPD(
            variable='DaysRemaining',
            variable_card=len(DAYS_STATES),
            values=[[0.3], [0.5], [0.2]],  
            state_names={'DaysRemaining': DAYS_STATES}
        )
    )

    cpds.append(
        TabularCPD(
            variable='Stress',
            variable_card=len(LEVEL_STATES),
            values=[
                [0.1, 0.35, 0.65, 0.7, 0.85, 0.92], 
                [0.9, 0.65, 0.35, 0.3, 0.15, 0.08]
            ],
            evidence=['Readiness', 'DaysRemaining'],
            evidence_card=[len(LEVEL_STATES), len(DAYS_STATES)],
            state_names={'Stress': LEVEL_STATES, 'Readiness': LEVEL_STATES, 'DaysRemaining': DAYS_STATES}
        )
    )

    model.add_cpds(*cpds)

    return model

def main(): 
    model = build_model()
    assert model.check_model()

if __name__ == "__main__":
    main()
    



