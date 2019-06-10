import sys
import matplotlib.pyplot as plt

def vizualize_data(lines):
    line_0 = lines[0].split()

    obj = float(line_0[0])
    title = 'obj: {}'.format(obj)
    error = []
    speed = []
    position = []
    integral = []
    derivative = []

    for line in lines[1:]:
        line = line.split()
        speed.append(float(line[0]))
        position.append(float(line[1]))
        error.append(float(line[2]))
        integral.append(float(line[3]))
        derivative.append(float(line[4]))

    fig, ax = plt.subplots(3)
    fig.suptitle(title)
    ax[0].plot(position, label='position', color='black')
    ax[0].hlines(obj, 0, len(lines), label='objetivo', color='magenta')
    ax[1].plot(error, label='error', color='red')
    ax[2].plot(speed, label='speed', color='green')
    fig.legend()
    fig, ax = plt.subplots(2)
    ax[0].plot(integral, label='integral', color='blue')
    ax[1].plot(derivative, label='derivative', color='orange')
    fig.legend()
    plt.show()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            lines = input_data_file.readlines()
        vizualize_data(lines)
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
    