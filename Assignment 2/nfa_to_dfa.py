from classes import NfaState


def df_search(current: NfaState, visited: []):
    visited.append(current.state_label)
    for state in current.epsilon_transitions:
        if state.state_label not in visited:
            df_search(state, visited)