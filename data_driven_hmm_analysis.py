import pandas as pd
import numpy as np
import collections
import json
import os

# 1. Improved Keyword to State Mapping (Comprehensive)
STATE_MAP = {
    # UTILIZATION
    'UTILIZATION': 'STATE_UTIL', 'RESOURCE': 'STATE_UTIL', 'ACCEPTANCE': 'STATE_UTIL', 'ALLIANCE': 'STATE_UTIL',
    'UTILIZING': 'STATE_UTIL', 'OWNERSHIP': 'STATE_UTIL', 'RESOURCES': 'STATE_UTIL',
    
    # PACING & VALIDATION
    'TRUISM': 'STATE_PACE', 'PACING': 'STATE_PACE', 'VALIDATION': 'STATE_PACE', 'YES': 'STATE_PACE', 
    'SET': 'STATE_PACE', 'RATIFICATION': 'STATE_PACE', 'MATCHING': 'STATE_PACE', 'REINFORCEMENT': 'STATE_PACE', 
    'LEARNING': 'STATE_PACE', 'REASSURANCE': 'STATE_PACE', 'AFFIRMATION': 'STATE_PACE', 'YESSET': 'STATE_PACE',
    'CALIBRATION': 'STATE_PACE', 'RAPPORT': 'STATE_PACE', 'NORMALIZATION': 'STATE_PACE', 'CONFIRMATION': 'STATE_PACE',
    
    # SUGGESTION & DIRECTIVE
    'SUGGESTION': 'STATE_SUGG', 'DIRECT': 'STATE_SUGG', 'INDIRECT': 'STATE_SUGG', 'COMMAND': 'STATE_SUGG', 
    'INSTRUCTION': 'STATE_SUGG', 'DIRECTIVE': 'STATE_SUGG', 'PRESCRIPTION': 'STATE_SUGG', 'INJUNCTION': 'STATE_SUGG', 
    'TASKING': 'STATE_SUGG', 'TASK': 'STATE_SUGG', 'DIRECTING': 'STATE_SUGG', 'DIRECTS': 'STATE_SUGG',
    
    # REFRAMING & LOGIC
    'REFRAMING': 'STATE_REFRAME', 'PARADOX': 'STATE_REFRAME', 'REDEFINITION': 'STATE_REFRAME', 'REFRAME': 'STATE_REFRAME', 
    'LOGIC': 'STATE_REFRAME', 'PARADOXICAL': 'STATE_REFRAME', 'REDEFINING': 'STATE_REFRAME', 'REDIRECTION': 'STATE_REFRAME',
    'REDEFINITION': 'STATE_REFRAME', 'LOGICAL': 'STATE_REFRAME', 'REDEFINITION': 'STATE_REFRAME',
    
    # BINDING & PRESUPPOSITION
    'PRESUPPOSITION': 'STATE_BIND', 'BIND': 'STATE_BIND', 'DOUBLE': 'STATE_BIND', 'CHOICE': 'STATE_BIND', 
    'ILLUSION': 'STATE_BIND', 'IMPLICATION': 'STATE_BIND', 'BINDING': 'STATE_BIND', 'PRESUPPOSE': 'STATE_BIND',
    
    # DISSOCIATION & TRANCE (Temporal/Spatial)
    'DISSOCIATION': 'STATE_DISSOC', 'UNCONSCIOUS': 'STATE_DISSOC', 'AMNESIA': 'STATE_DISSOC', 'TRANCE': 'STATE_DISSOC', 
    'REGRESSION': 'STATE_DISSOC', 'AGE': 'STATE_DISSOC', 'TEMPORAL': 'STATE_DISSOC', 'TIME': 'STATE_DISSOC', 
    'FUTURE': 'STATE_DISSOC', 'DISTORTION': 'STATE_DISSOC', 'POSTHYPNOTIC': 'STATE_DISSOC', 'POST': 'STATE_DISSOC', 
    'DEEPENING': 'STATE_DISSOC', 'INDUCTION': 'STATE_DISSOC', 'HYPNOTIC': 'STATE_DISSOC', 'DISSOCIATIVE': 'STATE_DISSOC',
    'AMNESIC': 'STATE_DISSOC', 'REVIVIFICATION': 'STATE_DISSOC', 'CATALEPSY': 'STATE_DISSOC', 'LEVITATION': 'STATE_DISSOC',
    
    # INQUIRY & SEARCH
    'INQUIRY': 'STATE_INQUIRY', 'QUESTION': 'STATE_INQUIRY', 'PROBE': 'STATE_INQUIRY', 'SEARCH': 'STATE_INQUIRY', 
    'ELICITATION': 'STATE_INQUIRY', 'ENGAGEMENT': 'STATE_INQUIRY', 'EXPLORE': 'STATE_INQUIRY', 'INTERROGATIVE': 'STATE_INQUIRY',
    'QUERY': 'STATE_INQUIRY', 'SEARCHING': 'STATE_INQUIRY', 'PROBING': 'STATE_INQUIRY',
    
    # METAPHOR & NARRATIVE
    'METAPHOR': 'STATE_METAPHOR', 'ANECDOTE': 'STATE_METAPHOR', 'STORY': 'STATE_METAPHOR', 'ANALOGY': 'STATE_METAPHOR', 
    'SYMBOL': 'STATE_METAPHOR', 'NARRATIVE': 'STATE_METAPHOR', 'TALE': 'STATE_METAPHOR', 'ANALOGICAL': 'STATE_METAPHOR',
    'CASE': 'STATE_METAPHOR', 'SYMBOLIC': 'STATE_METAPHOR', 'ANECDOTAL': 'STATE_METAPHOR',
    
    # INTERRUPTION & INTERVENTION (Strategic Challenge)
    'RESISTANCE': 'STATE_INTERRUPT', 'INTERRUPT': 'STATE_INTERRUPT', 'INTERRUPTION': 'STATE_INTERRUPT', 'SHOCK': 'STATE_INTERRUPT', 
    'CHALLENGE': 'STATE_INTERRUPT', 'CONFUSION': 'STATE_INTERRUPT', 'AMBIGUITY': 'STATE_INTERRUPT', 'PROVOCATION': 'STATE_INTERRUPT', 
    'CONFRONTATION': 'STATE_INTERRUPT', 'STRATEGIC': 'STATE_INTERRUPT', 'SHIFT': 'STATE_INTERRUPT', 'PATTERN': 'STATE_INTERRUPT'
}

def get_state_from_pattern(pattern_id):
    if not isinstance(pattern_id, str): return 'STATE_UNKNOWN'
    
    parts = pattern_id.upper().split('_')
    state_counts = collections.Counter()
    
    for p in parts:
        if p in STATE_MAP:
            state_counts[STATE_MAP[p]] += 1
            
    if not state_counts:
        return 'STATE_UNKNOWN'
    
    return state_counts.most_common(1)[0][0]

def run_analysis():
    print("Loading data...")
    df = pd.read_csv('erickson_sequences_with_submacros.csv')
    df = df.sort_values(['script_id', 'turn_no'])
    
    print("Mapping keywords to states...")
    df['data_state'] = df['pattern_id'].apply(get_state_from_pattern)
    
    states = ['STATE_UTIL', 'STATE_PACE', 'STATE_SUGG', 'STATE_REFRAME', 'STATE_BIND', 
              'STATE_DISSOC', 'STATE_INQUIRY', 'STATE_METAPHOR', 'STATE_INTERRUPT', 'STATE_UNKNOWN']
    state_to_idx = {s: i for i, s in enumerate(states)}
    
    n = len(states)
    transition_counts = np.zeros((n, n))
    
    print("Calculating transitions...")
    for script_id, group in df.groupby('script_id'):
        sequence = group['data_state'].tolist()
        for i in range(len(sequence) - 1):
            s_curr = sequence[i]
            s_next = sequence[i+1]
            transition_counts[state_to_idx[s_curr]][state_to_idx[s_next]] += 1
            
    transition_probs = np.zeros((n, n))
    for i in range(n):
        row_sum = np.sum(transition_counts[i])
        if row_sum > 0:
            transition_probs[i] = transition_counts[i] / row_sum
            
    result_df = pd.DataFrame(transition_probs, index=states, columns=states)
    result_df.to_csv('data_driven_transition_matrix_v2.csv')
    
    print("\n--- Data-Driven HMM Transition Matrix V2 (%) ---")
    print((result_df * 100).round(2))
    
    top_chains = []
    for i, start_state in enumerate(states):
        for j, end_state in enumerate(states):
            if transition_probs[i, j] > 0.12: # Threshold
                top_chains.append({
                    'From': start_state,
                    'To': end_state,
                    'Prob': transition_probs[i, j]
                })
                
    top_chains_df = pd.DataFrame(top_chains).sort_values('Prob', ascending=False)
    top_chains_df.to_csv('top_strategic_chains_data_v2.csv', index=False)
    
    print("\n--- Top Strategic Chains V2 (Prob > 12%) ---")
    print(top_chains_df.head(25))
    
    # Coverage Report
    coverage = df['data_state'].value_counts(normalize=True) * 100
    print("\n--- State Coverage (%) ---")
    print(coverage)

if __name__ == "__main__":
    run_analysis()
