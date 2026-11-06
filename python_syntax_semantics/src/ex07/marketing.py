import sys


def convert_to_sets(clients, participants, recipients):
    return set(clients), set(participants), set(recipients)

def get_address_list(task_name, clients, participants, recipients):
    if task_name == 'call_center':
        return clients - recipients
    elif task_name == 'potential_clients':
        return participants - clients
    elif task_name == 'loyalty_program':
        return clients - participants
    else:
        raise ValueError("Unknown task name: " + task_name)


def main(argc, argv):
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                     'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                     'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    if argc == 2:
        clients, participants, recipients = convert_to_sets(clients, participants, recipients)
        task_name = argv[1]
        result = get_address_list(task_name, clients, participants, recipients)
        for address in result:
            print(address)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)