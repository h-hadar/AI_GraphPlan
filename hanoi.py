import itertools
import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    disks_on_pole = [disc + '_on_' + pole for disc in disks for pole in pegs]  # d_6_on_p_0
    disks_not_on_pole = [disc + '_not_on_' + pole for disc in disks for pole in pegs]  # d_6_not_on_p_0
    domain_file.write("Propositions:\n")
    for p in disks_on_pole + disks_not_on_pole:
        domain_file.write(p + " ")
    domain_file.write('\nActions:\n')
    # action - pick up disc from pole with another disc below it to another pole where a disc below it
    for disc_index, p1 in itertools.product(range(n_), pegs):
        disc = disks[disc_index]
        for p2 in pegs:
            if p2 != p1:
                name = 'pick_' + disc + '_from_' + p1 + '_to_' + p2
                preconds = [disc + '_on_' + p1, disc + '_not_on_' + p2]
                add_list = [disc + '_on_' + p2, disc + '_not_on_' + p1]
                del_list = [disc + '_on_' + p1, disc + '_not_on_' + p2]
                for d in disks[:disc_index]:
                    preconds.append(d + '_not_on_' + p1)
                    preconds.append(d + '_not_on_' + p2)
                write_actions(add_list, del_list, domain_file, name, preconds)
    domain_file.close()


def write_actions(add_list, del_list, domain_file, name, preconds):
    domain_file.write("Name: " + name + '\n')
    domain_file.write("pre:")
    domain_file.writelines([' %s' % s for s in preconds])
    domain_file.write("\nadd:")
    domain_file.writelines([' %s' % s for s in add_list])
    domain_file.write("\ndelete:")
    domain_file.writelines([' %s' % s for s in del_list])
    domain_file.write('\n')


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file
    all_poles_on_disc(disks, m_, n_, pegs, problem_file, 0, "Initial state:")
    all_poles_on_disc(disks, m_, n_, pegs, problem_file, m_-1, "Goal state:")

    problem_file.close()


def all_poles_on_disc(disks, m_, n_, pegs, problem_file, desired_pole, title):
    initial_state = []
    for disc_index in range(n_):
        for pole_index in range(m_):
            if pole_index != desired_pole:
                initial_state.append(disks[disc_index] + '_not_on_' + pegs[pole_index])
    for disc_index in range(n_):
        initial_state.append(disks[disc_index] + '_on_' + pegs[desired_pole])
    problem_file.write(title)
    problem_file.writelines([' %s' % s for s in initial_state])
    problem_file.write("\n")



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
