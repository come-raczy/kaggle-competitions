from typing import Dict


class TrainingData:
    def __init__(self, targets: list[str]) -> None:
        self.targets = targets
        self.x : Dict[str, list[list[float]]] = {}
        self.y : Dict[str, list[int]] = {}
        for target in targets:
            self.x[target] = []
            self.y[target] = []

    def add(self, protein_name: str, buildingblock1_smiles: str, buildingblock2_smiles: str, buildingblock3_smiles: str, molecule_smiles: str, binds: str) -> None:
        target = protein_name
        if target not in self.targets:
            self.targets.append(target)
            self.x[target] = []
            self.y[target] = []
        self.x[target].append([0., 0., 0., 0.])
        self.y[target].append(1 if binds == '1' else 0)

