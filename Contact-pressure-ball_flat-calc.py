import pandas as pd
import numpy as np
import math

#Request user for input for calculation
force_mN = float(input("Enter the force applied (in mN): "))
elastic_modulus_counter_GPa = float(input("Enter the elastic modulus of the material (in GPa): "))
poisson_ratio_counter = float(input("Enter the Poisson's ratio of the counterface: "))
radius_um = float(input("Enter the radius of the counterface (in microns): "))
elastic_modulus_plane_GPa = float(input("Enter the elastic modulus of the plane (in GPa): "))
poissons_ratio_plane = float(input("Enter the Poisson's ratio of the plane: "))

#Calculations
force = force_mN * 1e-3  # Convert mN to N
elastic_modulus_counter = elastic_modulus_counter_GPa * 1e9  # Convert GPa to Pa
radius_m = radius_um * 1e-6  # Convert microns to meters
elastic_modulus_plane = elastic_modulus_plane_GPa * 1e9  # Convert GPa to Pa
equivalent_elastic_modulus = 1 / ((1 - poisson_ratio_counter**2) / elastic_modulus_counter + (1 - poissons_ratio_plane**2) / elastic_modulus_plane)
curvature_sum = ((1 / radius_m) + (1 / radius_m)**-1) 
contact_radius = (3 * force * radius_m / (4 * equivalent_elastic_modulus))**(1/3)
contact_pressure = (3 * force) / (2 * math.pi * contact_radius**2)

#Output results
print(f"curvature_sum: {curvature_sum:.2e} m^-1")
print(f"Equivalent Elastic Modulus: {equivalent_elastic_modulus:.2e} Pa")
print(f"Contact Radius: {contact_radius:.2e} m")
print(f"Contact Pressure: {contact_pressure / 1e9:.2f} GPa")