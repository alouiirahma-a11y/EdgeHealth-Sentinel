def analyze_community_context(
    population,
    area_km2,
    settlements,
    health_facilities,
    health_workers,
    underserved_rate,
    transport_access,
    connectivity,
):
    if area_km2 > 0:
        population_density = population / area_km2
    else:
        population_density = 0

    if population > 0:
        health_worker_density = (
            health_workers / population
        ) * 1000
    else:
        health_worker_density = 0

    if health_facilities > 0:
        population_per_facility = (
            population / health_facilities
        )
    else:
        population_per_facility = population

    if population_density >= 500:
        density_class = "HIGH_DENSITY"
    elif population_density >= 100:
        density_class = "MODERATE_DENSITY"
    else:
        density_class = "LOW_DENSITY"

    geographic_access_risk = 0

    if transport_access == "LIMITED":
        geographic_access_risk += 1

    if connectivity == "POOR":
        geographic_access_risk += 1

    if settlements >= 10:
        geographic_access_risk += 1

    if population_per_facility > 5000:
        geographic_access_risk += 1

    if geographic_access_risk >= 3:
        access_risk = "HIGH"
    elif geographic_access_risk >= 1:
        access_risk = "MODERATE"
    else:
        access_risk = "LOW"

    underserved_population = (
        population * underserved_rate
    )

    return {
        "population": population,
        "area_km2": area_km2,
        "population_density": population_density,
        "density_class": density_class,
        "settlements": settlements,
        "health_facilities": health_facilities,
        "population_per_facility": population_per_facility,
        "health_workers": health_workers,
        "health_worker_density_per_1000": health_worker_density,
        "underserved_population": underserved_population,
        "underserved_rate": underserved_rate,
        "transport_access": transport_access,
        "connectivity": connectivity,
        "geographic_access_risk": access_risk,
    }


if __name__ == "__main__":
    result = analyze_community_context(
        population=8000,
        area_km2=250,
        settlements=12,
        health_facilities=1,
        health_workers=2,
        underserved_rate=0.40,
        transport_access="LIMITED",
        connectivity="POOR",
    )

    for key, value in result.items():
        print(f"{key}: {value}")
