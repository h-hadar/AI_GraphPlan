import itertools
import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    disc_on_disc = []
    for i in range(n_):
        for j in range(i+1, n_):
            disc_on_disc.append(disks[i] + '_on_disc_' + disks[j])
    disc_on_table = [d + '_on_table' for d in disks]
    is_arm_free = ['arm_free']
    is_disc_in_arm = ['in_arm_' + d for d in disks]
    top_of_poles = ['top_' + pole + '_' + disc for disc in disks for pole in pegs]  # top_p_3_d_6
    is_pole_free = ['free_' + pole for pole in pegs]
    domain_file.write("Propositions:\n")
    for p in is_arm_free + top_of_poles + is_disc_in_arm + disc_on_table + disc_on_disc + is_pole_free:
        domain_file.write(p + " ")
    domain_file.write('\nActions:\n')

    # action - pick up disc from pole with another disc below it
    for disc_index, pole in itertools.product(range(n_), pegs):
        disc = disks[disc_index]
        for below in disks[disc_index+1:]:
            name = 'pick_' + disc + '_from_' + pole + '_above_' + below
            preconds = ['top_' + pole + '_' + disc, 'arm_free', disc + '_on_disc_' + below]
            add_list = ['top_' + pole + '_' + below, 'in_arm_' + disc]
            del_list = ['arm_free', 'top_' + pole + '_' + disc, disc + '_on_disc_' + below]
            write_actions(add_list, del_list, domain_file, name, preconds)

    # pick up disc from pole on floor
    for disc, pole in itertools.product(disks, pegs):
        name = 'pick_' + disc + '_from_' + pole + '_from_floor'
        preconds = ['top_' + pole + '_' + disc, 'arm_free', disc + '_on_table']
        add_list = ['free_' + pole, 'in_arm_' + disc]
        del_list = preconds
        write_actions(add_list, del_list, domain_file, name, preconds)

    # put disc down on floor
    for disc, pole in itertools.product(disks, pegs):
        name = 'put_' + disc + '_on_' + pole + '_on_floor'
        preconds = ['free_' + pole, 'in_arm_' + disc]
        add_list = [disc + '_on_table', 'top_' + pole + '_' + disc, 'arm_free']
        del_list = preconds
        write_actions(add_list, del_list, domain_file, name, preconds)

    # put disc down on another disc on pole
    for i in range(n_):
        for j in range(i + 1, n_):
            for pole in pegs:
                d1, d2 = disks[i], disks[j]
                name = 'put_' + d1 + '_on_' + pole + '_on_top_of_' + d2
                preconds = ['in_arm_' + d1, 'top_' + pole + '_' + d2]
                add_list = ['arm_free', 'top_' + pole + '_' + d1, d1 + '_on_disc_' + d2]
                del_list = preconds
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
    initial_state = ['arm_free']
    for i in range(0, m_):
        if i != desired_pole:
            initial_state.append('free_' + pegs[i])
    initial_state.append('top_' + pegs[desired_pole] + '_' + disks[0])
    initial_state.append(disks[-1] + '_on_table')
    for i in range(n_ - 1):
        initial_state.append(disks[i] + '_on_disc_' + disks[i + 1])
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
