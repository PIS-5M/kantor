import api1 as ap
import time
import os


bots = {
    1 : 'bot 1',
    2 : 'bot 2',
    3 : 'bot 3'
    }

currency = {
    1: 'USD',
    2: 'EUR'
}


def clear():
    os.system('cls')
    # os.system('clear')

def sleep():
    time.sleep(2)

def main():
    # introduction()
    # scene1()
    # scene2()
    scene3()
    scene4()

def introduction():
    clear()
    print('\n\nWitamy w kantorze 5MONET.')
    sleep()
    print('To jest test matchowania')
    sleep()
    print('Mamy 3 użytkowników, którzy będą testować różne scenariusze')
    sleep()

def scene1():
    clear()
    print('\nScenariusz 1')
    sleep()
    print('opis')
    sleep()
    print_offers()
    wallet()
    print('Bot 1 wystawia ofertę na 50 dolarów za euro w cenie 2.0')
    sleep()
    add_offer(1, 1, 50.0, 2, 2.0)
    print('Bot 2 wystawia ofertę na 100 euro za dolary w cenie 0.5')
    sleep()
    add_offer(2, 2, 100.0, 1, 0.5)

def scene2():
    clear()
    print('\nScenariusz 2')
    sleep()
    print('opis')
    sleep()
    print_offers()
    wallet()
    print('Bot 1 wystawia ofertę na 50 dolarów za euro w cenie 20')
    sleep()
    add_offer(1, 1, 50.0, 2, 20.0)
    print('Bot 2 wystawia ofertę na 100 euro za dolary w cenie 20')
    sleep()
    add_offer(2, 2, 100.0, 1, 20)


def scene3():
    clear()
    print('\nScenariusz 3')
    sleep()
    print('opis')
    sleep()
    print_offers()
    wallet()
    print('Bot 1 wystawia ofertę na 50 dolarów za euro w cenie 2.0')
    sleep()
    add_offer(1, 1, 50.0, 2, 2.0)
    print('Bot 2 wystawia ofertę na 40 dolarów za euro w cenie 1.98')
    sleep()
    add_offer(2, 1, 40.0, 2, 1.98)
    print('Bot 3 wystawia ofertę na 200 euro za dolary w cenie 0.5')
    sleep()
    add_offer(3, 2, 200.0, 1, 0.5)

def scene4():
    clear()
    print('\nScenariusz 4')
    sleep()
    print('opis')
    sleep()
    print_offers()
    wallet()
    print('Bot 1 wystawia ofertę na 50 dolarów za euro w cenie 1.97')
    sleep()
    add_offer(1, 1, 50.0, 2, 1.97)
    print('Bot 2 wystawia ofertę na 40.67 dolarów za euro w cenie 1.97')
    sleep()
    add_offer(2, 1, 40.67, 2, 1.97)
    print('Bot 3 wystawia ofertę na 200 euro za dolary w cenie 0.5')
    sleep()
    add_offer(3, 2, 200.0, 1, 0.5)




def print_offers():
    print('Dostępne oferty:')
    sleep()
    offers = ap.get_uncompleted_offers()
    print('sprzedawane\tposzukiwane\tkurs')
    if offers:
        for offer in offers:
            print(f'{offer[8]} {currency[offer[4]]}\t{currency[offer[6]]}\t\t{offer[7]}')
            sleep()
    else:
        print('Brak dostępnych ofert.')
        sleep()

def wallet():
    print('Stan portfeli:')
    sleep()
    print('Waluta\t\t\tbot\tdostępne w portfelu\tw ofertach')
    for i in range(1, 4):
        wallets = ap.show_wallet(i)
        print(f'{wallets[0][0]}\t{bots[wallets[0][2]]}\t{wallets[0][3]}\t\t\t{wallets[0][4]}')
        print(f'{wallets[1][0]}\t\t\t{bots[wallets[1][2]]}\t{wallets[1][3]}\t\t\t{wallets[1][4]}')
        sleep()


def add_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate):
    match_list = ap.add_offer(user_id, selled_currency_id, value, wanted_currency_id, exchange_rate)
    if not match_list:
        print('Brak pasujących offert.')
    for matching in match_list:
        print(f'{bots[user_id]} za {matching[0]} {currency[selled_currency_id]} dostał {matching[1]} {currency[wanted_currency_id]}')
        sleep()
    print_offers()
    wallet()



if __name__ == "__main__":
    main()