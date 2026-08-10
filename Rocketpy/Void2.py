from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime
import matplotlib.pyplot as plt


# AMBIENTE
env = Environment(
    latitude=-21.90795,
    longitude=-48.96156,
    elevation=495
)

env.set_atmospheric_model(
    type="standard_atmosphere"
)

# MOTOR
K783 = SolidMotor(
    thrust_source="VOID2.csv",
    dry_mass=2.5,
    dry_inertia=(0.03, 0.03, 0.001),
    nozzle_radius=15/1000,
    throat_radius=6.5/1000,
    grain_number=3,
    grain_density=1841,
    grain_outer_radius=30/1000,
    grain_initial_inner_radius=11.5/1000,
    grain_initial_height=110/1000,
    grain_separation=5/1000,
    grains_center_of_mass_position=0.195,
    center_of_dry_mass_position=0.195,
    nozzle_position=0,
    burn_time=2.43,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# K783.all_info()

# FOGUETE VOIDI
VOIDI = Rocket(
    radius=0.052,
    mass=8,
    inertia=(2.8, 2.8, 0.08),
    center_of_mass_without_motor=0.87,  
    power_off_drag="Power-off_colunas_trocadas.csv",
    power_on_drag="Power_swapped.csv",
    coordinate_system_orientation="tail_to_nose",
)


# MOTOR — posicionado na cauda
VOIDI.add_motor(K783, position=-0.06)

# GUIAS
VOIDI.set_rail_buttons(
    upper_button_position=1.05,
    lower_button_position=0.15,
    angular_position=45,
)

# COIFA — base em 1.39 m, ponta em 1.74 m (length=0.35)
nose_cone = VOIDI.add_nose(
    length=0.35,
    kind="ogive",
    position=1.74,
)

# ALETAS — próximas à cauda
fin_set = VOIDI.add_trapezoidal_fins(
    n=4,
    root_chord=0.189,
    tip_chord=0.0594,
    span=0.112,
    sweep_length=0.0473,
    position=0.24,
    cant_angle=0.0,
)

# BOATTAIL
tail = VOIDI.add_tail(
    top_radius=0.052,
    bottom_radius=0.049,
    length=0.05,
    position=-0.01,
)

# PARAQUEDA PRINCIPAL
main = VOIDI.add_parachute(
    name="main",
    cd_s=2.95,
    trigger=426,
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
    radius=0.97,
    height=1.94,
    porosity=0.0432,
)

# DROGUE
drogue = VOIDI.add_parachute(
    name="drogue",
    cd_s=0.28,
    trigger="apogee",
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
    radius=0.27,
    height=0.54,
    porosity=0.0432,
)

# DESENHO
#VOIDI.draw()
#VOIDI.all_info()

# SIMULAÇÃO
test_flight = Flight(
    rocket=VOIDI,
    environment=env,
    rail_length=4.0,
    inclination=80,
    heading=90,
)

test_flight.plots.all()

print(f"Apogeu ASL: {test_flight.apogee:.2f} m")
print(
    f"Apogeu AGL: "
    f"{test_flight.apogee - env.elevation:.2f} m"
)

print(f"Tempo de apogeu: {test_flight.apogee_time:.2f} s")

#test_flight.prints.apogee_conditions()

print(f"Velocidade de impacto: {test_flight.impact_velocity:.2f} m/s")