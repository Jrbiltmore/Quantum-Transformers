# src/utility_frameworks/quantum_development_kit.py

from qiskit import QuantumCircuit, transpile, Aer, IBMQ, execute
from qiskit.compiler import assemble
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram, plot_state_qsphere
from qiskit.providers.aer.noise import NoiseModel

class QuantumDevelopmentKit:
    def __init__(self, backend_name='aer_simulator', use_real_device=False, api_token=None, provider_hub=None, provider_group=None, provider_project=None):
        if use_real_device:
            if not api_token:
                raise ValueError("API token is required to use real quantum devices.")
            IBMQ.save_account(api_token, overwrite=True)
            IBMQ.load_account()
            provider = IBMQ.get_provider(hub=provider_hub, group=provider_group, project=provider_project)
            self.backend = provider.get_backend(backend_name)
        else:
            self.backend = Aer.get_backend(backend_name)

    def create_quantum_circuit(self, num_qubits):
        circuit = QuantumCircuit(num_qubits)
        return circuit

    def run_circuit(self, circuit, shots=1024, optimization_level=3):
        transpiled_circuit = transpile(circuit, self.backend, optimization_level=optimization_level)
        qobj = assemble(transpiled_circuit, shots=shots)
        job = self.backend.run(qobj)
        job_monitor(job)
        return job.result()

    def visualize_results(self, result, method='histogram'):
        if method == 'histogram':
            plot_histogram(result.get_counts())
        elif method == 'qsphere':
            statevector_backend = Aer.get_backend('statevector_simulator')
            circuit = result.to_dict()['results'][0]['header']['compiled_circuit_qasm']
            qc = QuantumCircuit.from_qasm_str(circuit)
            statevector = execute(qc, statevector_backend).result().get_statevector()
            plot_state_qsphere(statevector)

    def get_noise_model(self):
        if not isinstance(self.backend, Aer.get_backend('qasm_simulator').__class__):
            raise ValueError("Noise models can only be retrieved for Aer qasm_simulator backend.")
        noise_model = NoiseModel.from_backend(self.backend)
        return noise_model

def main():
    qdk = QuantumDevelopmentKit(use_real_device=False)
    qc = qdk.create_quantum_circuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    result = qdk.run_circuit(qc)
    qdk.visualize_results(result, method='histogram')

if __name__ == "__main__":
    main()
