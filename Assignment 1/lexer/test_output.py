from parser import *
from lexer import *
from minimizer import *
from gen_output import output_to_xml


def gen_final_dfa(expression="10(0|1)*ab?", comp_expression="1.0.(0|1)*.a.b?"):
    nfa = parser(expression, comp_expression)
    power_closures, x = generate_power_closures(nfa)
    dfa = build_dfa(nfa, power_closures)
    reduce_dfa_states(dfa)
    dfa = relabel_dfa(dfa)
    print_dfa(dfa)
    DFA = minimize(dfa)
    print_dfa(DFA)
    # output_to_xml(dfa)



# gen_final_dfa("EEE", "E.E.E")
# gen_final_dfa("a?b?c?", "a?.b?.c?")
# gen_final_dfa("(a+)*", "(a+)*")
# gen_final_dfa("(a*)+", "(a*)+")

# bug in merging -> virtually same state merging issue
# gen_final_dfa("(1|e)e?", "(1|e).e?")

# gen_final_dfa("a|(1|e)*e?", "a|(1|e)*.e?")

#####################################
# gen_final_dfa('a', 'a')
# gen_final_dfa('a*', 'a*')
# gen_final_dfa('a+', 'a+')
# gen_final_dfa('aa', 'a.a')
# gen_final_dfa('a|b', 'a|b')
# gen_final_dfa('a|b|c', 'a|b|c')
# gen_final_dfa('a?', 'a?')
# gen_final_dfa('a?', 'a?')
gen_final_dfa('a|(b?)', 'a|(b?)')

