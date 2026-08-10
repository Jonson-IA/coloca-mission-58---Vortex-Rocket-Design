from rocketpy import Environment, SolidMotor, Rocket, Flight
import datetime
import matplotlib.pyplot as plt


# AMBIENTE
env = Environment(
    latitude=-21.89,
    longitude=-49.03,
    elevation=422
)

env.set_atmospheric_model(
    type="custom_atmosphere",
    pressure=101325,
    temperature=300,
    wind_u=[(0, 4.73), (5000, 4.73)],
    wind_v=[(0, -4.73), (5000, -4.73)],
)

# MOTOR
K783 = SolidMotor(
    thrust_source="VOID2.csv",
    dry_mass=2,
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
    mass=7.652,
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
    root_chord=0.1189,
    tip_chord=0.060,
    span=0.1237,
    sweep_length=0.0297,
    position=0.12,
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
#VOIDI.all_info()
# SIMULAÇÃO
test_flight = Flight(
    rocket=VOIDI,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=0,
)

print(f"Apogeu: {test_flight.apogee:.2f} m")
print(f"Velocidade máxima: {test_flight.max_speed:.2f} m/s")
print(f"Aceleração máxima: {test_flight.max_acceleration:.2f} m/s²")

test_flight.plots.all()


