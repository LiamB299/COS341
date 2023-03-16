from parser import *
from lexer import *
from minimizer import *


def gen_final_dfa(expression="10(0|1)*ab?", comp_expression="1.0.(0|1)*.a.b?"):
    nfa = parser(expression, comp_expression)
    power_closures, x = generate_power_closures(nfa)
    dfa = build_dfa(nfa, power_closures)
    reduce_dfa_states(dfa)
    dfa = relabel_dfa(dfa)
    print_dfa(dfa)
    DFA = minimize(dfa)
    print_dfa(DFA)


# gen_final_dfa("EEE", "E.E.E")
# gen_final_dfa("a?b?c?", "a?.b?.c?")
# gen_final_dfa("(a+)*", "(a+)*")
# gen_final_dfa("(a*)+", "(a*)+")
gen_final_dfa("ab*(1|e)+e?", "a.b*.(1|e)+.e?")
