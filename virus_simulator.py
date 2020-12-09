import numpy as np
from matplotlib import pyplot as plt

infectious_time = 20
symptome_time = infectious_time/2

class Person:
    def __init__(self):
        self.position = np.array([np.random.rand()*2, np.random.rand()*2])
        self.immune = False
        self.infectious_counter = 0
        self.symptom_counter = 0
        self.quarantine_counter = 0
        self.positions = []
        self.group = None
        self.next_positions_idx = 0
        self.next_position = np.array([np.random.rand()*2, np.random.rand()*2])
        self.speed = 0.03
        self.color = 'b'
        self.get_infection = np.random.normal(0.5, 0.2)
        self.give_infection = np.random.normal(0.5, 0.2)

    def move(self):
        vec = (self.next_position - self.position)
        vec_len = np.linalg.norm(vec)
        if self.quarantine_counter == 0:
            if vec_len < self.speed:
                if len(self.positions) == 0:
                    while True:
                        self.next_position = np.array([np.random.rand()*2, np.random.rand()*2])
                        vec = (self.next_position - self.position)
                        vec_len = np.linalg.norm(vec)
                        if vec_len > 0.2:
                            break
                else:
                    self.next_positions_idx += 1
                    if self.next_positions_idx >= len(self.positions):
                        self.next_positions_idx = 0
                    self.next_position = self.positions[self.next_positions_idx][:]
                vec = (self.next_position - self.position)
                vec_len = np.linalg.norm(vec)
            vec_normed = vec/vec_len
            self.position += vec_normed*self.speed

        if self.quarantine_counter > 0:
            self.quarantine_counter -= 1
        if self.infectious_counter > 0:
            self.symptom_counter += 1
            self.infectious_counter -= 1
            if self.infectious_counter == 0:
                self.immune = True
                self.symptom_counter = 0


class People:
    def __init__(self, n_people=500, work=True):
        self.persons = [Person() for i in range(n_people)]
        self.persons[0].infectious_counter = 10
        if work:
            work_positions = [np.array([np.random.rand()*2, np.random.rand()*2]) for i in range(50)]
            #home_positions = [np.array([np.random.rand(), np.random.rand()]) for i in range(10)]
            n_per_position = int(len(self.persons)/len(work_positions))
            for i in range(len(self.persons)):
                self.persons[i].positions.append(work_positions[int(i / n_per_position)])
                self.persons[i].positions.append(np.array([np.random.rand()*2, np.random.rand()*2]))

                self.persons[i].group = int(i / n_per_position)
                self.persons[i].next_positions_idx = 0
                self.persons[i].position = np.array([self.persons[i].positions[0][0], self.persons[i].positions[0][1]])
                self.persons[i].next_position = self.persons[i].positions[self.persons[i].next_positions_idx]

    def move(self):
        for p in self.persons:
            p.move()

    def infect(self):
        for i in range(len(self.persons)):
            p1 = self.persons[i]
            if p1.infectious_counter == 0 or p1.quarantine_counter > 0:
                continue
            if p1.symptom_counter > symptome_time:
                if np.random.rand() < 0.8:
                    p1.quarantine_counter = int(symptome_time*1.25)
                if p1.group is not None:
                    #quarantine for all of same group
                    for p in self.persons:
                        if p.group == p1.group and np.random.rand() < 0.8:
                            p.quarantine_counter = int(symptome_time*1.25)
                continue

            for k in range(len(self.persons)):
                p2 = self.persons[k]
                if k == i or p2.infectious_counter > 0 or p2.immune or p2.quarantine_counter > 0:
                    continue
                if p1.get_infection*p2.get_infection > 0.25:
                    if np.linalg.norm(p1.position - p2.position) < 0.05:
                        p2.infectious_counter = infectious_time


def simulate(steps=250):
    fig, axes = plt.subplots(2)
    peeps = People()
    ax0 = axes[0]
    ax1 = axes[1]
    infected_max = 0
    for s in range(steps):
        peeps.move()
        peeps.infect()
        ax0.clear()
        count_infected = 0
        count_immune = 0
        count_healty = 0
        n_peep_cnt = 0
        for p in peeps.persons:
            if p.infectious_counter > 0:
                color = 'r'
                count_infected += 1
                if infected_max < count_infected:
                    infected_max = count_infected
            else:
                if p.immune:
                    color = 'g'
                    count_healty += 1
                else:
                    color = 'b'
                    count_immune += 1
            if p.quarantine_counter > 0:
                color = 'y'
            if n_peep_cnt == 0:
                marker = '+'
            else:
                marker = 'o'
            ax0.plot(p.position[0], p.position[1], marker + color)
            ax0.set_xlim([0, 2])
            ax0.set_ylim([0, 2])
            n_peep_cnt += 1
        ax1.plot(s, count_infected, '-or')
        ax1.plot(s, count_healty + count_immune, '-og')
        plt.pause(0.05)
        print(infected_max)
    plt.show()



simulate()