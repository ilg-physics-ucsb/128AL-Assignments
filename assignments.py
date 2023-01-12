from ortools.sat.python import cp_model
import numpy as np
import pprint
model = cp_model.CpModel()
costs = [
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100],
]
num_students_per_group = 2
num_workers = len(costs)
# num_workers = len(costs)
num_tasks = num_students_per_group * len(costs[0])

costs = np.concatenate((costs,)*num_students_per_group, axis=1)
pprint.pprint(costs)
x = []
for i in range(num_workers):
    t = []
    for j in range(num_tasks):
        t.append(model.NewBoolVar(f'x[{i},{j}]'))
    x.append(t)
# pprint.pprint(f'X=\n {x}')
for i in range(num_workers):
    model.Add(sum(x[i][j] for j in range(num_tasks)) <= 1)

for j in range(num_tasks):
    model.Add(sum(x[i][j] for i in range(num_workers)) == num_students_per_group )

objective_terms = []
for i in range(num_workers):
    for j in range(num_tasks):
        objective_terms.append(costs[i][j] * x[i][j])

model.Minimize(sum(objective_terms))
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(f'Total cost = {solver.ObjectiveValue()}')
    print()
    for i in range(num_workers):
        for j in range(num_tasks):
            if solver.BooleanValue(x[i][j]):
                print(
                    f"Worker {i} assigned to task {j}. Cost = {costs[i][j]}"
                )
else:
    print('No solution found')
