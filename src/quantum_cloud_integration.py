# src/scalable_integration/quantum_cloud_integration.py

import numpy as np
from qiskit import IBMQ, transpile, assemble
from qiskit.providers.ibmq import least_busy
from qiskit.circuit import QuantumCircuit

class QuantumCloudIntegration:
    def __init__(self, api_token, provider_hub, provider_group, provider_project):
        IBMQ.save_account(api_token, overwrite=True)
        self.provider = IBMQ.load_account().get_provider(hub=provider_hub, group=provider_group, project=provider_project)
        self.backend = None

    def select_least_busy_backend(self, min_qubits):
        large_enough_devices = self.provider.backends(filters=lambda x: x.configuration().n_qubits >= min_qubits and not x.configuration().simulator)
        self.backend = least_busy(large_enough_devices)
        print(f"Least busy backend: {self.backend}")

    def execute_quantum_circuit(self, circuit: QuantumCircuit, shots=1024):
        transpiled_circuit = transpile(circuit, self.backend)
        qobj = assemble(transpiled_circuit, shots=shots)
        job = self.backend.run(qobj)
        print(f"Executing job {job.job_id()} on backend {self.backend.name()}")
        result = job.result()
        counts = result.get_counts(circuit)
        return counts

def create_simple_circuit():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    return qc

def main():
    API_TOKEN = 'YOUR_IBM_Q_API_TOKEN'
    PROVIDER_HUB = 'ibm-q'
    PROVIDER_GROUP = 'open'
    PROVIDER_PROJECT = 'main'
    
    quantum_integration = QuantumCloudIntegration(API_TOKEN, PROVIDER_HUB, PROVIDER_GROUP, PROVIDER_PROJECT)
    quantum_integration.select_least_busy_backend(min_qubits=5)

    simple_circuit = create_simple_circuit()
    execution_result = quantum_integration.execute_quantum_circuit(simple_circuit)
    print(f"Execution Result: {execution_result}")

if __name__ == "__main__":
    main()
