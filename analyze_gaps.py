import json

with open('election_data_scan.json', 'r') as f:
    data = json.load(f)

races_by_state = {}
candidates_by_state = {}

for race in data['races']:
    state = race.get('state', 'Unknown')
    races_by_state[state] = races_by_state.get(state, 0) + 1

for candidate in data['candidates']:
    state = candidate.get('state', 'Unknown')
    candidates_by_state[state] = candidates_by_state.get(state, 0) + 1

print("=" * 80)
print("STATES NEEDING COMPREHENSIVE CANDIDATE DATA")
print("=" * 80)

states_with_work = []
for state in sorted(races_by_state.keys()):
    races = races_by_state[state]
    candidates = candidates_by_state.get(state, 0)
    gap = races - candidates
    
    if gap > 0:
        states_with_work.append({
            'state': state,
            'races': races,
            'candidates': candidates,
            'gap': gap,
            'priority': 'HIGH' if races >= 10 else 'MEDIUM' if races >= 5 else 'LOW'
        })

# Sort by gap size
states_with_work.sort(key=lambda x: x['gap'], reverse=True)

print("\nPRIORITY ORDER (by candidate gap):\n")
for i, state_info in enumerate(states_with_work, 1):
    print(f"{i}. {state_info['state']:20} - {state_info['races']:3} races, {state_info['candidates']:3} candidates, GAP: {state_info['gap']:3} [{state_info['priority']}]")

print("\n" + "=" * 80)
print("TOP 10 STATES TO COMPLETE:")
print("=" * 80)
for state_info in states_with_work[:10]:
    print(f"\n{state_info['state']} ({state_info['priority']} PRIORITY)")
    print(f"  Races: {state_info['races']}")
    print(f"  Candidates: {state_info['candidates']}")
    print(f"  Missing: {state_info['gap']} candidates needed")
