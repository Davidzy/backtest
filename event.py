class Event(object):
    """
    Event is base class providing an interface of all subsequent (inherited)
    events, that will trigger further events in the trading infrastructure.
    """
    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with corresponding bars.
    """
    def __init__(self):
        """
        Initializes the MarketEvent.
        """
        self.type = 'MARKET'


class SignalEvent(Event):
    """
    Handles the event of sending a Signal from Strategy object. This is received
    by a Portfolio object and acted upon.
    """
    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        :param strategy_id: The unique identifier for the strategy that
            generated the signal.
        :param symbol: The ticker symbol, e.g. 'AAPL'.
        :param datetime: The timestamp at which the signal was generated.
        :param signal_type: 'LONG' OR 'SHORT'.
        :param strength: an adjustment factor "suggestion" used to scale
            quantity at the portfolio level. Useful for pairs strategies.
        """
        self.type = 'SIGNAL'
        self.strategy = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength


class OrderEvent(Event):
    """
    Handles the event of sending an order to an execution system. The order
    contains a symbol (e.g. 'AAPL'), a type (market or limit), quantity and
    a direction.
    """
    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initializes the order type, setting whether it is a Market order ('MKT')
        or Limit order ('LMT'), has a quantity (integral) and its direction (
        'BUY' or 'SELL').

        :param symbol: The instrument to trade.
        :param order_type: 'MKT' or 'LMT' for Market or Limit.
        :param quantity: Non-negative integer for quantity.
        :param direction: 'BUY' or 'SELL' for long or short.
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self):
        """
        Outputs the values within the order.
        :return: a string that print on screen.
        """
        print("Order: Symbol={}, Type={}, Quantity={}, Direction={}".format(
            self.symbol, self.order_type, self.quantity, self.direction))


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned from a brokerage.
    Stores the quantity of an instrument actually filled and at what price. In
    addition, stores the commission of the trade from the brokerage.
    """
    def __init__(self, timeindex, symbol, exchange, quantity, direction,
                 fill_cost, commission=None):
        """
        Initializes the FillEvent object. Sets the symbol, exchange, quantity,
        direction, cost of fill and an optional commission.
        If commission is not provided, the Fill object will calculate it based
        on the trade size and Interactive Brokers fees.

        :param timeindex: The bar-resolution when the order was filled.
        :param symbol: The instrument which was filled.
        :param exchange: The exchange where the order was filled.
        :param quantity: The filled quantity.
        :param direction: The direction of fill ('BUY' or 'SELL').
        :param fill_cost: The holdings value in dollars.
        :param commission: an optional commission sent from IB.
        """

        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculate commission
        if commission is None:
            self.commission = self.calculate_commission()
        else:
            self.commission = commission

    def calculate_commission(self):
        """
        Calculates the fees of trading based on

        This does not include exchange or ECN fees.
        :return: value in number
        """
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(1.3, 0.0013 * self.quantity)
        else:
            full_cost = max(1.3, 0.0008 * self.quantity)
        return full_cost


