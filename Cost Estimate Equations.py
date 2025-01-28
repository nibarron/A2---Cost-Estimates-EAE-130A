import math

##### RDT&E and production costs coding - Nickole #####

# Necessary Parameters for equations {fps}
W_e = 3000  # Empty weight in pounds (lb) ---------- change
V = 200     # Maximum velocity in knots (kt)
Q = 10      # Lesser of production quantity
FTA = 3     # Number of flight-test aircraft (typically 2 to 6)
N_eng = 2   # Total production quantity times number of engines per aircraft
SHP_TO = 1500  # Takeoff shaft horsepower for turboprop engines
C_avionics = 50000  # Avionics cost in dollars ($)
CEF = 1.7   # Cost escalation factor (inflation for engine cost) ----------- Write code to calculate this
MTOW = 8000 # Maximum Take-Off Weight (lbs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
t_b = 1 # Block time (hours) ----- Guessed
AF = 0.8 # Airline Factor found using regression analysis
K = 2.75 # Route Factor for regional routes 
W_f = 30 # Fuel Weight (lbs) ---- change using 100 UL fuel for turboprops
rho_f = 1.02 # fuel density (lbs/gallon) ------change!!!!
P_f = 3.25 # Price per gallon of jet fuel (USD$/gal) ------change 
W_b = 30 # Weight of the battery (kg) -----change units
P_elec = 0.52 # Price of electricity in ($/kWh)
e_elec_spec = 0.23 # Specific energy of the battery in (Wh/kg) ----change units
P_oil = 0.12 # Cost per gallon of oil (USD$/gal) -------change
rho_oil = 0.1 # Density of oil (lbs/gallon) ----change
W_empty = 1000 # Empty weight (lbs) -----change
W_eng = 100 # Weight of the engine (lbs) ----change
T_0 = 12 # Engine maximum thrust (lbs) ----change
n_engines = 2 # number of engines -----change
IR_a = 0.02 # hull insurance rate (ussually assumed to be 2%)
K_depreciation = 0.1 # aircraft residual value factor ---change
n = 10 # number of years the aircraft is used

# Hourly rates for labor (adjusted to 2012)
hourly_rate_engineering = 115  # $ per hour
hourly_rate_tooling = 118       # $ per hour
hourly_rate_manufacturing = 98 # $ per hour
hourly_rate_qc = 108            # $ per hour
hourly_rate_maintenence = 120 # $ per hour

# Engineering costs
H_E = 4.86 * (W_e ** 0.777) * (V ** 0.894) * (Q ** 0.163)
C_E = H_E * hourly_rate_engineering

# Tooling costs
H_T = 5.99 * (W_e ** 0.777) * (V ** 0.696) * (Q ** 0.263)
C_T = H_T * hourly_rate_tooling

# Manufacturing costs
H_M = 7.37 * (W_e ** 0.82) * (V ** 0.484) * (Q ** 0.641)
C_Mfg = H_M * hourly_rate_manufacturing

# Quality control costs (assuming non-cargo aircraft)
H_Q = 0.133 * H_M
C_Q = H_Q * hourly_rate_qc

# Development support costs (adjusted for inflation)
C_D = (91.3 * (W_e ** 0.63) * (V ** 1.3)) * CEF

# Flight test operations costs (adjusted for inflation)
C_F = (2498 * (W_e ** 0.325) * (V ** 0.822) * (FTA ** 1.21)) * CEF

# Manufacturing materials cost (adjusted for inflation)
C_Mat = (22.1 * (W_e ** 0.921) * (V ** 0.621) * (Q ** 0.799)) * CEF

# Turboprop engine production cost (adjusted for inflation)
C_eng = (10 ** (2.5262 + 0.9465 * math.log10(SHP_TO)) * CEF)

# Turboprop commuter aircraft price
C_aircraft = (10 ** (1.1846 + 1.2625 * math.log10(MTOW)) * CEF)

# Airframe Price
C_airframe = C_aircraft - C_eng

# Flyaway costs (Airframe + Engine + Avionics)
Flyaway_cost = C_airframe + C_eng + C_avionics

# Total RDT&E and flyaway cost (price of just the aircraft itself)
RDT_E_flyaway = (
    C_E + C_T + C_Mfg + C_Q +
    C_D + C_F + C_Mat + (C_eng * N_eng) + Flyaway_cost 
)

# Display results
print(f"Engineering cost (C_E): ${C_E:,.2f}")
print(f"Tooling cost (C_T): ${C_T:,.2f}")
print(f"Manufacturing cost (C_Mfg): ${C_Mfg:,.2f}")
print(f"Quality Control cost (C_Q): ${C_Q:,.2f}")
print(f"Development support cost (C_D): ${C_D:,.2f}")
print(f"Flight test cost (C_F): ${C_F:,.2f}")
print(f"Manufacturing materials cost (C_Mat): ${C_Mat:,.2f}")
print(f"Turboprop engine production cost per engine (C_eng): ${C_eng:,.2f}")
print(f"Total RDT&E and flyaway cost: ${RDT_E_flyaway:,.2f}")





##### Direct Operating Costs coding - Nickole #####

## Cash Operating Costs Equations (COC)
# Crew Costs (1999 Base year)
C_crew = AF * (K * (MTOW ** 0.40) * t_b) * CEF  ### Need new CEF from 1999-2025

# Attendants cost not needed
# Fuel costs 
C_fuel = 1.02 * W_f * (P_f / rho_f)

# Battery Costs
C_elec = 1.05 * W_b * P_elec * e_elec_spec

# Oil costs and lubricants
W_oil = 0.0125 * W_f * (t_b / 100)
C_oil = 1.02 * W_oil * (P_oil / rho_oil)

# Landing fees ??????? Do we need?

# Navigation fees??? Do we need?

# Airframe maintenence
W_A = W_empty - W_eng 
C_ML = 1.03 * (3 + (0.067 * W_A /1000) * hourly_rate_maintenence)
C_MM = 1.03 * (30 * CEF) + 0.79e-5 * C_airframe
C_airframe_main = (C_ML + C_MM) * t_b

# Engine maintenence (base year is 1993)
C_ML_eng = (0.645 + (0.05 * T_0 / 1e4)) * (0.566 + (0.434 / t_b)) * hourly_rate_maintenence
C_MM_eng = (25 + (18 * T_0 / 1e4)) * (0.62 + (0.38 / t_b)) * CEF    # Change CEF for 1993-2024
C_engine_main = n_engines * (C_ML_eng + C_MM_eng) * t_b

# Add price of electric aircraft????

# Total Cash Operating Costs
COC = C_crew + C_fuel + C_elec + C_oil + C_airframe_main + C_engine_main

## Fixed Operating Costs
# Insurance Costs (annual cost)
U_annual = 1.5e3 * ((3.4546 * t_b) + 2.994 - ((12.289 * (t_b ** 2)) - (5.6626 * t_b) + 8.964) ** 0.5)
C_insurance = (IR_a * C_aircraft / U_annual) * t_b

# Financing -- Interest applied to initial loan used to buy the aircraft
# About 7% of the DOC, so add later 

# Depreciation Costs ----- Confused, need to revisit 
C_unit = 10000 # ----------Change bc idk what this is
C_depreciation = ((C_unit * t_b * (1 - K_depreciation)) / (n * U_annual))

# Registration taxes
DOC = COC + C_insurance + C_depreciation
C_registration = (0.001 + (1e-6 * MTOW)) * DOC 

# Total Fixed Operating Costs
FOC = C_insurance + C_depreciation + C_registration 

# Total DOC
DOC_total = COC + FOC # USD$/cargo ton nmi) ----- Check units 
print(f"Direct Operating Cost (DOC): ${DOC_total:,.2f}")