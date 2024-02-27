import numpy as np

def divdend_discount_model(edps, cce, dgr):
    '''
    Computes a stock's intrinsic value using the
    dividend discount model.

    Pros:
        - Computes the 'present value' of stock for a certain return (decided by the investor)
          the (expected) dividend growth rate
    Cons:
        - Divideds are difficut to predict
        - Difficult to predict dividends' growth rates
        - Not suitable for companies that don't pay dividends

    Parameters
    ----------
    edps: float
        Expected dividend per share
    cce: float
        Cost of capital equity
    dgr: float
        Dividend growth rate

    Returns
    ----------
    stock_value: float
        Intrinsic stock value

    References
    ----------
    [1] https://www.investopedia.com/articles/basics/12/intrinsic-value.asp
    [2] https://www.investopedia.com/terms/d/ddm.asp
    
    '''

    stock_value = edps/(cce - dgr)

    return stock_value


def gordon_growth_model(one_yr_div, return_rate, growth):
    '''
    Computes a stock's intrinsic value using the
    Gordon Growth  model (GGM).

    Pros:
        - Quite accurate for blue-chip companies (can be compared with DDM)
    
    Cons:
        - Assumes dividends grow etarnally
        - Difficult to predict dividends' growth rates
        - Ignores factors like: new products, competition or investor's sentiment

    
    Parameters
    ----------
    one_yr_div: float
        Expected dividends one year from the present
    return_rate: float
        Required rate for equity investors
    growth: float
        Annual growth rate in dividends in perpetuity

    Returns
    ----------
    stock_value: float
        Intrinsic stock value

    References
    ----------
    [1] https://www.investopedia.com/articles/basics/12/intrinsic-value.asp
    [2] https://www.investopedia.com/terms/g/gordongrowthmodel.asp
    
    '''

    stock_value = one_yr_div/(return_rate - growth)

    return stock_value


def residual_income_model(bv, res_inc, coe):
    '''
    Computes a stock's intrinsic value using the
    Residual Income model (RIM).

    Residual Income is the leftover income after paying the bills.
    It is thus a good indicator of a company's (or inivdual's!) stability.
    
    The key feature of this formula lies in how its valuation method derives
    the value of the stock based on the difference in earnings per share and
    per-share book value (in this case, the security's residual income) to
    arrive at the intrinsic value of the stock.

    Essentially, the model seeks to find the intrinsic value of the stock by
    adding its current per-share book value with its discounted residual income
    (which can either lessen the book value or increase it). 

    Pros:
        - It's probably good to decide on Bonds, since
          it is a factor used in loan approvals (check this...)
    
    Cons:

    
    Parameters
    ----------
    bv: float
        Current book value of the company's equity
    res_inc: float array
        Residual income of a company at time period t
    coe: float array
        Cost of equity at time period t

    Returns
    ----------
    stock_value: float
        Intrinsic stock value

    References
    ----------
    [1] https://www.investopedia.com/articles/basics/12/intrinsic-value.asp
    [2] https://www.investopedia.com/terms/r/residualincome.asp
    
    '''

    discounted_residual_income = 0

    for tt, cost in enumerate(coe):
        discounted_residual_income += res_inc[tt]/( np.power(1 + cost, tt+1) )
    
    stock_value = bv + discounted_residual_income

    return stock_value


def discounted_cash_flows_model(cf, disc_rate, nperiods = 4):
    '''
    Computes a stock's intrinsic value using the
    Discounted Cash Flows model (DCF).

    te length of cf should be at least nperidos
    (4 by default, since that's how many years of cashflows
    yahoo finance provides.)

    Pros:
        
    Cons:
        - WACC is usually difficult to determine

    
    Parameters
    ----------
    cf: float array
        Cashflows in different periods
    disc_rate: float 
        discount rate (e.g. WACC) in different periods
    nperiods: int
        number of periods 

    Returns
    ----------
    stock_value: float
        Intrinsic stock value

    References
    ----------
    [1] https://www.investopedia.com/articles/basics/12/intrinsic-value.asp
    [2] https://www.investopedia.com/terms/d/dcf.asp
    
    '''

    if len(cf) < nperiods:
        print("Not enough cash flows!")
        return None
    
    DCF = 0

    
    for ii in range(0, nperiods):
       DCF += cf[ii]/np.power(1 + disc_rate[ii], ii+1 ) 


    return DCF

def wacc_calculator(equity, debt, Ke, Kd, tax_rate):
    '''
    WACC stands for weighted Average Cost of Capital
    and indicates the company's average after-tax cost of
    capital from all sources, be it bonds or other forms
    of debt. In other words, it is the average rate that
    a company expects to pay to finance its business.

    The higher the WACC, the less likely it is that the
    company is creating value.

    In 2021, the ighest values were recorded for the
    Tech (8.9%), Automotive (7.6%), and Industrial
    Manufacturing (7.5%) sectors.
    
    Parameters
    ----------
    equity: float 
        Market value of equity
    debt: float 
        Market value of equity
    Ke: float
        Cost of equity
    Kd: float
        Cost of debt
    tax_rate: float
        Corporate tax rate

    Returns
    ----------
    stock_value: float
        Intrinsic stock value

    References
    ----------
    [1] https://www.wallstreetmojo.com/weighted-average-cost-capital-wacc/
    [2] https://www.investopedia.com/terms/w/wacc.asp
    
    '''
    V = np.abs(equity) + np.abs(debt)

    wacc = E/V*Ke + D/V*Kd*(1 - tax_rate)
