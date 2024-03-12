# src/quantum_innovations/photonic_quantum_systems.py

import numpy as np
from strawberryfields.apps import data, sample, plot
import strawberryfields as sf
from strawberryfields.ops import *
from thewalrus.quantum import photon_number_mean, photon_number_covmat

class PhotonicQuantumSystem:
    def __init__(self, num_modes, mean_photon_number):
        self.num_modes = num_modes
        self.mean_photon_number = mean_photon_number
        self.eng = sf.Engine(backend="gaussian")
        self.program = sf.Program(num_modes)

    def setup_system(self):
        with self.program.context as q:
            for i in range(self.num_modes):
                Squeezed(r=np.sqrt(self.mean_photon_number)) | q[i]
            for i in range(self.num_modes - 1):
                BSgate(phi=np.pi/4) | (q[i], q[i+1])

    def run_simulation(self):
        state = self.eng.run(self.program).state
        return state

    def calculate_statistics(self, state):
        cov_matrix = state.cov()
        mean_photon = photon_number_mean(cov_matrix, hbar=sf.hbar)
        cov_photon = photon_number_covmat(cov_matrix, hbar=sf.hbar)
        return mean_photon, cov_photon

    def generate_samples(self, shots=1000):
        with self.program.context as q:
            MeasureFock() | q

        result = self.eng.run(self.program, shots=shots)
        samples = result.samples
        return samples

def main():
    num_modes = 4
    mean_photon_number = 1.0

    photonic_system = PhotonicQuantumSystem(num_modes, mean_photon_number)
    photonic_system.setup_system()
    state = photonic_system.run_simulation()

    mean_photon, cov_photon = photonic_system.calculate_statistics(state)
    print(f"Mean photon number per mode: {mean_photon}")
    print(f"Covariance matrix of photon numbers: \n{cov_photon}")

    # Generating samples
    shots = 1000
    samples = photonic_system.generate_samples(shots=shots)
    print(f"Generated {len(samples)} samples from measuring in the Fock basis.")

    # Example: plotting the histogram of the total photon number distribution
    total_photons = np.sum(samples, axis=1)
    plot.histogram(total_photons, xlabel="Total Photon Number", ylabel="Frequency")

if __name__ == "__main__":
    main()
