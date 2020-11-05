from get_au_energies_v4 import ScanToEnergies
import matplotlib.pyplot as plt

filename = input('Hi Claire! Welcome to S2E. Type "quit" at any time to quit.\n Please enter .out file name: ')
if filename != 'quit':
    scan = ScanToEnergies(filename)
    print(f'Total number of atoms: {scan.number_of_atoms}')

    plt.plot(scan.scan_number(), scan.energies(), color='purple')
    plt.ylabel('Total Energy (Hartree)')
    plt.xlabel('Scan number')
    filename = input('Save details as: ')
    plt.savefig(f'plot_{filename}')
    print(f'Plot saved in the current directory as plot_{filename}.')

    print(f'In case it is unclear, the maximum energy of {scan.max_energy()[0]} Hartrees'
          f'can be found at {scan.max_energy()[1] + 1}')

    retreive_xyz = input('Would you like to retrieve coordinates? y/n\n')
    if retreive_xyz != 'n':
        scan.xyz_of_one_scan(filename)
        print(f'.xyz file saved in the current directory as {filename}.xyz')
    print('Exiting module...')
    print('Module exited. Goodbye')
