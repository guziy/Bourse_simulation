import helper

__author__ = 'huziy'

cash_word = "Liquidite"
item_word = "Titre"
broker_dump = "broker.bin"

import pickle
import os
import numpy as np

import matplotlib.pyplot as plt





class Item:
    name = ""
    current_price = None
    current_quantity = 0
    transaction_number = 0
    rank = 0
    invested = 0
    def __init__(self, name = "", current_price = None, current_quantity = 0, broker = None):
        self.name = name
        self.current_price = current_price
        self.current_quantity = current_quantity #quantity available for purchase today
        self.broker = broker
        self.price_history = []
        self.operations_volume_history = []
        self.transaction_cost = 2000


    def sell_all(self):
        gain = self.current_price * self.current_quantity - self.transaction_cost
        if gain >= 0:
            self.invested -= gain
            self.current_quantity = 0
            return gain
        else:
            return 0

    def has_previous_history(self):
        """
        returns True if the previous history has already been read
        """
        return len(self.price_history) != 0

    def deal(self, available_money):
        """
        1. fit using 3 prev points => predict next
        2. fit using 4 prev points => predict next

        if next > current => buy

        return gain (can be negative if buying)
        """
        gain = 0
        #sell if gaining
        if self.current_price * self.current_quantity > self.invested + self.transaction_cost:
            gain = self.current_price * self.current_quantity - self.transaction_cost
            self.invested = 0
            self.current_quantity = 0
            return gain


        polyn = np.poly1d( np.polyfit( xrange(-20,1) , self.price_history[-21:], 20) )
        predicted_price = np.inf

        #buy if income predicted
        if predicted_price > self.current_price:
            additional_qty = (available_money - self.transaction_cost) // self.current_price
            if additional_qty > 10:
                self.current_quantity += additional_qty
                gain -= (self.transaction_cost + additional_qty * self.current_price)
                self.invested += self.transaction_cost + additional_qty * self.current_price
                return gain
        return gain



        pass


class Broker:

    def __init__(self, firstName = "Oleksandr", lastName = "Huziy"):
        self.state_path = "%s%s.csv" % (lastName, firstName)
        self.items = []
        self.day_of_year = 0
        self._read_previous_state()
        print "initial cash: {:.2f}".format(self.cash / 100.0)
        self.days_per_year = 260


    def _read_previous_state(self):
        """
        Is read only after the first time step
        """
        f = open(self.state_path)
        for line in f:
            line = line.strip()
            if line.startswith(cash_word):
                self.cash = np.round(float(line.split(",")[-1]) * 100) #convert to cents
            elif line.startswith(item_word):
                fields = line.split(",")
                self.items.append(Item(name = fields[0], current_quantity = int(fields[-1].strip()), broker=self))

        f.close()


    def get_current_balance(self):
        res = self.cash
        for item in self.items:
            res += item.current_quantity * item.current_price - item.transaction_cost
        return res

    def _get_price_from_line(self, line):
        """
        parse price data from the line and return median
        """
        fields = line.split(",")[1:-1]
        return int(100 * np.median(map( lambda x: float(x.strip()), fields)))


    def _get_volume_from_line(self, line):
        return int(line.split(",")[-1])


    def _read_current_prices(self):
        """
        Read current quantity and prices from the file
        """
        for theItem in self.items:
            f = open("%s.csv" % theItem.name)
            if theItem.has_previous_history():
                f.readline() #skip header
                line = f.readline()
                price = self._get_price_from_line(line)
                volume = self._get_volume_from_line(line)
                theItem.price_history = [price] + theItem.price_history
                theItem.operations_volume_history = [volume] + theItem.operations_volume_history
            else:
                lines = f.readlines()
                lines = lines[1:]
                prices = map( self._get_price_from_line, lines)
                volumes = map(self._get_volume_from_line, lines)
                theItem.price_history = prices
                theItem.operations_volume_history = volumes
            f.close()
            theItem.current_price = theItem.price_history[0]

        self.items_sorted_by_price = sorted(self.items, key = lambda x: x.current_price)






    def make_deals(self):
        self._read_current_prices()

        if self.day_of_year % self.days_per_year == self.days_per_year - 1:
            self.sell_all()
        else:
            for the_item in self.items_sorted_by_price:
                if the_item.operations_volume_history[-1] > np.median(the_item.operations_volume_history):
                    gain = the_item.deal(self.cash // len(self.items))
                    self.cash += gain


        self._save_current_state()
        pass


    def plot_price_histories(self):

        for anItem in self.items:
            plt.plot(anItem.price_history, label = anItem.name)

        plt.show()



    def _save_current_state(self):
        f = open(self.state_path, "w")
        f.write("%s,%.2f\n" % (cash_word, self.cash / 100.0)) # convert back to dollars
        itemFormat = "%s,%d\n"
        for index, theItem in enumerate(self.items):
            f.write(itemFormat % (theItem.name, theItem.current_quantity))
        f.close()

        self.day_of_year += 1
        pickle.dump(self, open(broker_dump, mode="w"))
        pass

    def sell_all(self):
        for theItem in self.items:
            self.cash += theItem.sell_all()


def main():
    if os.path.isfile(broker_dump):
        b = pickle.load(open(broker_dump))
    else:
        b = Broker()
    #print "current day is %d" % b.day_of_year
    b.make_deals()
    print b.get_current_balance()
    assert b.cash >= 0, "cash cannot be %g" % b.cash
    pass


def test():
    """
    For testing
    """
    if os.path.isfile(broker_dump):
        os.remove(broker_dump)

    for i in xrange(0,260):
        helper.create_input_file_for_the_day(simulation_day = i)
        main()


if __name__ == "__main__":
    #main()
    test()