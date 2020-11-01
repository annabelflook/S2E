from mendeleev import element


class ScanToEnergies:
    def __init__(self, filename):
        self.filename = filename
        self.number_of_atoms = self.no_of_atoms()
        self.initial_geometry = 'Not Found'

    def __str__(self):
        pass

    def read_file(self):
        for line in open(self.filename, 'r'):
            yield line

    def finder(self, pointer: str):
        for line_number, line in enumerate(self.read_file()):
            if pointer in line:
                yield line_number, line

    def no_of_atoms(self):
        atom_line = self.finder('NAtoms=')
        for line_number, line in atom_line:
            start = line.find('NAtoms=') + 7
            end = line.find('NQM')
            return int(line[start:end])

    def max_step(self):
        line_max_step = []
        step_number = [(line_number, int(step[12:17].strip())) for line_number, step in self.finder('scan point')]

        for x in range(len(step_number) - 1):
            line_number, step = step_number[x]
            if step > (step_number[x + 1])[1]:
                line_max_step.append((line_number, step))
        line_max_step.append(step_number.pop())

        return line_max_step

    def energies(self):
        line_number_energies = []
        for line_number, line in self.finder('SCF Done'):
            number_start = line.find('=') + 1
            number_end = line.find('A.U')

            line_number_energies.append((line_number, float(line[number_start:number_end].strip())))

        energies = []
        for line_number, max_step in self.max_step():
            for energy_number, energy in reversed(line_number_energies):
                if line_number > energy_number:
                    energies.append(energy)
                    break

        return energies

    def scan_number(self):
        return list(range(1, len(self.energies()) + 1))

    def xyzs(self):
        xyz_line_number = []
        for line_number, line in self.finder('Coordinates'):
            xyz_line_number.append((line_number + 3, 'line'))

        self.initial_geometry = xyz_line_number.pop(0)

        xyzs = []
        for line_number, max_step in self.max_step():
            for xyz_number, xyz in xyz_line_number:
                if line_number < xyz_number:
                    xyzs.append((xyz_number, 'xyzs'))
                    break

        return xyzs

    def xyzs_per_scan(self):
        scan_xyzs = []

        with open(self.filename, 'r') as file:
            lines = file.readlines()

        for coord_lines in self.xyzs():
            scan_n = []
            line_number, coord = coord_lines
            x = 0
            while x < self.number_of_atoms:

                scan_n.append(lines[line_number + x].split())
                scan_xyzs.append(scan_n)
                x += 1

        return scan_xyzs

    def xyz_of_one_scan(self, filename):
        scan_number = input('Enter Scan Number: ')
        # filename = input('What would you like to save this scan as? ')
        with open(f'{filename}.xyz', 'a') as xyz_file:
            xyz_file.write(f'{self.number_of_atoms}\n')
            xyz_file.write(f'{filename}\n')
            for atom in self.xyzs_per_scan()[int(scan_number) - 1]:
                centre, atomic_number, other, x, y, z = atom
                xyz_file.write(f'{element(int(atomic_number)).symbol}    {x}    {y}    {z}\n')

        return f'{filename}.xyz created'
