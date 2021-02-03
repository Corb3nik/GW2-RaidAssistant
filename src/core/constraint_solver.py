#!/usr/bin/env python3

from functools import reduce
import z3

class ConstraintSolver:

    def gen_primes(self):
        """ Generate an infinite sequence of prime numbers.
            Taken from https://stackoverflow.com/questions/567222/simple-prime-number-generator-in-python
        """
        D = {}
        q = 2

        while True:
            if q not in D:
                yield q
                D[q * q] = [q]
            else:
                for p in D[q]:
                    D.setdefault(p + q, []).append(p)
                del D[q]

            q += 1

    def __init__(self, keys, player_constraints):
        g = self.gen_primes()
        self.values_by_role = { key : next(g) for key in keys }
        self.roles_by_value = { v: k for k, v in self.values_by_role.items() }
        self.players = player_constraints
        self.solution = reduce(lambda x, y: x * y, self.values_by_role.values())


    def get_solutions(self):
        solver = z3.Solver()
        player_vars = []

        # Set a constraint where each player can only play roles they've specified
        for player, roles in self.players.items():

            player_var = z3.Int(player)
            player_vars.append(player_var)
            solver.add(z3.Or([player_var == self.values_by_role[role] for role in roles]))

        # Set a constraint where each role must be used exactly once
        solver.add(reduce(lambda x, y: x * y, player_vars) == self.solution)

        # Iterate over all solutions
        while True:

            if solver.check() == z3.unsat:
                print("Could not find any more valid solutions for these constraints")
                return

            model = solver.model()

            yield { self.roles_by_value[model[d].as_long()] : str(d) for d in model.decls() }

            # Add the previous solution to the list of constraints
            solver.add(z3.Or([var != model[var] for var in player_vars]))
