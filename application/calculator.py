def calculate_production_plan(load, fuels, powerplants):
    for plant in powerplants:
        if plant['type'] == 'gasfired':
            co2_cost = fuels['co2_euro_per_ton'] * 0.3
            plant['cost_per_mwh'] = (fuels['gas_euro_per_mwh'] / plant['efficiency']) + co2_cost
        elif plant['type'] == 'turbojet':
            plant['cost_per_mwh'] = fuels['kerosine_euro_per_mwh'] / plant['efficiency']
        elif plant['type'] == 'windturbine':
            plant['cost_per_mwh'] = 0
            plant['pmax'] *= fuels['wind_percentage'] / 100
        plant['used'] = False

    sorted_plants = sorted(powerplants, key=lambda x: (x['cost_per_mwh'], -x['pmax']))

    production_plan = []
    total_production = 0

    for plant in sorted_plants:
        if plant['type'] == 'gasfired' and 'pmin' in plant:
            if load - total_production >= plant['pmin']:
                production = min(plant['pmax'], load - total_production)
                plant['used'] = True
            else:
                production = 0
        else:
            production = min(plant['pmax'], load - total_production)
            plant['used'] = True

        total_production += production
        production_plan.append({'name': plant['name'], 'p': round(production, 1)})

        if total_production >= load:
            break

    if total_production < load:
        for plant in sorted_plants:
            if not plant['used']:
                additional_production = min(plant['pmax'], load - total_production)
                if plant['type'] == 'gasfired' and 'pmin' in plant and additional_production < plant['pmin']:
                    continue
                total_production += additional_production
                production_plan.append({'name': plant['name'], 'p': round(additional_production, 1)})
                if total_production >= load:
                    break

    return production_plan