class Event(object):
    """
    Event作为基类，为其他Event类（子类）提供接口。
    """
    pass


class MarketEvent(Event):
    """
    接收市场价格信息的更新。
    """
    def __init__(self):
        """
        初始化MarketEvent.
        """
        self.type = 'MARKET'


class SignalEvent(Event):
    """
    通过Strategy对象发出信号事件。Portfolio对象接收该事件，并基于此做出决策。
    """
    def __init__(self, strategy_id, symbol, datetime, signal_type, strength):
        """
        :param strategy_id: 唯一标示发出信号的Strategy对象
        :param symbol: 股票代码标识，如'AAPL'
        :param datetime: 信号产生的时间戳
        :param signal_type: 'LONG'或'SHORT'
        :param strength: 调仓的权重系数，在投资组合中建议买入或卖出的数量.
        """
        self.type = 'SIGNAL'
        self.strategy = strategy_id
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type
        self.strength = strength


class OrderEvent(Event):
    """
    向交易系统发送OrderEvent。Order包含标识(e.g. 'AAPL')，类型(market or limit)，
    数量和方向。
    """
    def __init__(self, symbol, order_type, quantity, direction):
        """
        初始化order类型，确定是Market order('MKT')还是Limit order('LMT')，还包含数量和
        买卖的方向('BUY' or 'SELL')。

        :param symbol: 交易的对象
        :param order_type: 'MKT' or 'LMT' for Market or Limit.
        :param quantity: 非负整数表示的数量
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

        :return: value in number
        """
        full_cost = 1.3
        if self.quantity <= 500:
            full_cost = max(full_cost, 0.0013 * self.quantity)
        else:
            full_cost = max(full_cost, 0.0008 * self.quantity)
        return full_cost
