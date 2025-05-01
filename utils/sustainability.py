def calculate_carbon_footprint(distance_km, mode='flight'):
    emission_factors = {'flight': 0.21, 'train': 0.05}
    return distance_km * emission_factors.get(mode, 0.21)
