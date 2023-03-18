from parser import *
from lexer import *
from minimizer import *
from gen_output import output_to_xml
from regex_validation import *


def gen_final_dfa(expression="10(0|1)*ab?", comp_expr=""):
    valid, reduced = validate_expression(expression)
    print('Expression valid? ' + str(valid) + '\nReduced expression to: ' + reduced + '\n\n')
    if not valid:
        print("Closing")
        return
    print("Parsing to NFA...")
    nfa = parser(expression, "", debug=False)

    print("Convert to DFA...")
    print("Powerset of closures...")
    power_closures, x = generate_power_closures(nfa)
    dfa = build_dfa(nfa, power_closures)
    print("Remove unreachable states for readability")
    reduce_dfa_states(dfa)
    print('Relabel states\n')
    dfa = relabel_dfa(dfa)
    print_dfa(dfa)

    print("Minimize DFA...")
    DFA = minimize(dfa)
    print_dfa(DFA)



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
# gen_final_dfa('a|(b?)', 'a|(b?)')
# gen_final_dfa('a|(b)*', 'a|(b)*')
# gen_final_dfa('a|(b*)', 'a|(b*)')
# gen_final_dfa('(a|(b))*', '(a|(b))*')
# gen_final_dfa('(a?|(b?))', '(a?|(b?))')
# gen_final_dfa('(a?(b?))', '(a?.(b?))')
# gen_final_dfa('(a?(b?)cd)', '(a?.(b?).c.d)')
# gen_final_dfa('(a?(b?)c*d*)', '(a?.(b?).c*.d*)')
# gen_final_dfa('(a+(b?)c*d*)', '(a+.(b?).c*.d*)')
# gen_final_dfa('a(a+(b?)c*d*)', 'a.(a+.(b?).c*.d*)')
# gen_final_dfa('a*|b*')
# gen_final_dfa('(a*b)|(b*c?)')
# gen_final_dfa('')
# gen_final_dfa('a?b?c?d*')

# -> bug in mergin states.. fixed?
# gen_final_dfa('a|(a+)')
# gen_final_dfa('a|a+')
