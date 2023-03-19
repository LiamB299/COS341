import regex_validation
from parser import *
from dfa_gen import *
from minimizer import *
from gen_output import *


# build with: python -m PyInstaller runner.py
def entry_point():
    try:
        expression = input("please enter regex:\n")
        print("You entered: " + expression)
        print("Validating using tutor grammar rules...")
        valid, reduced = regex_validation.validate_expression(expression)
        print('Expression valid? ' + str(valid) + '\nReduced expression to: ' + reduced + '\n\n')
        if not valid:
            print("Closing")
            return
        print("Parsing to NFA...")
        nfa = parser(expression, "", debug=False)

        print("Convert to DFA...")
        print("Powerset of closures...")
        print("This may take O(n^3) long...")
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

        print("Print to file...")
        output_to_xml(DFA)
        print("Generation finished successfully\n\n\n")
        input("")

    except:
        print('Erroneous Regex')


if __name__ == '__main__':
    entry_point()
