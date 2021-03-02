import numpy as np
# import matplotlib as plt
import pyomo.environ as pyo


payload1 = {
    "load": 480,
    "fuels":
        {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
        },
    "powerplants": [
        {
            "name": "gasfiredbig1",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "gasfiredbig2",
            "type": "gasfired",
            "efficiency": 0.53,
            "pmin": 100,
            "pmax": 460
        },
        {
            "name": "gasfiredsomewhatsmaller",
            "type": "gasfired",
            "efficiency": 0.37,
            "pmin": 40,
            "pmax": 210
        },
        {
            "name": "tj1",
            "type": "turbojet",
            "efficiency": 0.3,
            "pmin": 0,
            "pmax": 16
        },
        {
            "name": "windpark1",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 150
        },
        {
            "name": "windpark2",
            "type": "windturbine",
            "efficiency": 1,
            "pmin": 0,
            "pmax": 36
        }
    ]
}




def unit_commitment(load, powerplants, fuels):
    # demand
    d = load

    N = len(powerplants)
    pp_ids = np.array([pp['id'] for pp in powerplants])
    efficiencies = np.array([pp['efficiency'] for pp in powerplants])

    pp_ids_sorted_for_efficiency = np.array([n for _, n in sorted(zip(efficiencies, pp_ids), reverse=True)])

    pmins = np.zeros(N)
    pmaxs = np.zeros(N)
    costs = np.zeros(N)
    co2s = np.zeros(N)

    for pp in powerplants:
        pmins[pp['id']-1] = pp['pmin']
        pmaxs[pp['id']-1] = pp['pmax']

        if pp['fuel'] == 'wind':
            costs[pp['id']-1] = 0
        else:
            if pp['fuel'] in fuels.keys():
                costs[pp['id']-1] = fuels[pp['fuel']]
            else:
                # throw error
                pass

        co2s[pp['id']-1] = pp['co2']

    minpmin = min(pmins)
    maxpmax = max(pmaxs)

    m = pyo.ConcreteModel()

    m.N = pyo.Set(ordered=True, initialize=pp_ids_sorted_for_efficiency)

    m.x = pyo.Var(m.N, bounds=(minpmin, maxpmax))
    m.u = pyo.Var(m.N, domain=pyo.Binary)

    # objective
    m.cost = pyo.Objective(expr=sum(m.x[n] * costs[n-1] + m.u[n] * pmins[n-1] * costs[n-1] + m.x[n] * 0.3 * co2s[n-1] for n in m.N), sense=pyo.minimize)

    # demand
    m.demand = pyo.Constraint(m.N, rule=lambda m, n: sum(m.x[n] for n in m.N) == load)

    # semi-continuous
    m.lb = pyo.Constraint(m.N, rule=lambda m, n: (pmins[n-1] * m.u[n] <= m.x[n]))
    m.ub = pyo.Constraint(m.N, rule=lambda m, n: (pmaxs[n-1] * m.u[n] >= m.x[n]))

    pyo.SolverFactory('cbc').solve(m).write()

    # TODO: make extra template and use matplotlib and plotly to output a graph with the solution
    #
    # fig, ax = plt.subplots(max(m.N) + 1, 1, figsize=(8, 1.5 * max(m.N) + 1))
    # for n in range(1, max(m.N)+1):
    #     ax[n].bar(1, m.x[n]())
    #     ax[n].set_xlim(0, 2)
    #     ax[n].set_ylim(0, 1.1 * pmaxs[n-1])
    #     ax[n].plot(ax[n].get_xlim(), np.array([pmaxs[n-1], pmaxs[n-1]]), 'r--')
    #     ax[n].plot(ax[n].get_xlim(), np.array([pmins[n-1], pmins[n-1]]), 'r--')
    #     ax[n].set_title('Unit ' + str(n))
    # fig.tight_layout()
    #
    # plt.show()

    return m


def calculate(payload):
    fuels = {}

    for fuel_name, fuel_cost in payload['fuels'].items():
        if 'wind' in fuel_name:
            fuels['wind'] = fuel_cost
        elif 'gas' in fuel_name:
            fuels['gas'] = fuel_cost
        elif 'kerosine' in fuel_name:
            fuels['kerosine'] = fuel_cost
        elif 'co2' in fuel_name:
            fuels['co2'] = fuel_cost

    powerplants = []
    for pp_id, pp in enumerate(payload['powerplants'], 1):
        powerplant = {'id': pp_id}

        for k, v in pp.items():
            if k == 'name':
                powerplant['name'] = v
            if k == 'type':
                if 'wind' in v:
                    powerplant['fuel'] = 'wind'
                    powerplant['co2'] = 0
                elif 'gas' in v:
                    powerplant['fuel'] = 'gas'
                    powerplant['co2'] = fuels['co2']
                elif 'turbojet' in v:
                    powerplant['fuel'] = 'kerosine'
                    powerplant['co2'] = 0
            if 'efficiency' in k:
                powerplant['efficiency'] = v
            if 'pmin' in k:
                powerplant['pmin'] = v
            if 'pmax' in k:
                powerplant['pmax'] = v

        powerplants.append(powerplant)

    m = unit_commitment(payload['load'], powerplants, fuels)

    # TODO: check if m is feasible

    # if (m.solver.status == SolverStatus.ok) and (
    #         m.solver.termination_condition == TerminationCondition.optimal):
    #     pass
    # elif (m.solver.termination_condition == TerminationCondition.infeasible):
    #     pass
    # else:
    #     # Something else is wrong
    #     print("SolverStatus: " + m.solver.status)

    results = []
    for n in range(1, len(powerplants)+1):
        result_pp = {}
        pp = list(filter(lambda p: p['id'] == n, powerplants))[0]
        result_pp['name'] = pp['name']
        result_pp['p'] = int(m.x[n]())
        results.append(result_pp)

    return results

# for testing purposes

if __name__ == '__main__':
    print(calculate(payload1))
