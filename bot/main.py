import api1 as ap
import time
import os

def clear():
    os.system('cls')
    # os.system('clear')

def sleep():
    time.sleep(2)

def main():
    clear()
    print('\n\nWitamy w kantorze 5MONET.')
    sleep()
    print('To jest test matchowania')
    sleep()
    print('Mamy 3 użytkowników, którzy będą testować różne scenariusze')
    sleep()
    clear()
    print('\nScenariusz 1')
    sleep()
    print('opis')
    clear()
    scene1()

def scene1():
    sleep()



def print_offers():
    print('Dostępne oferty:')
    sleep()
    offers = ap.get_uncompleted_offers()
    for offer in offers:
        print(offer)
        sleep()

def wallet():
    print('Stan portfeli:')
    sleep()
    for i in range(1, 4):
        pass


if __name__ == "__main__":
    main()